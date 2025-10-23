"""
Testing Your MCP Tools with Streamlit
Run with: uv run streamlit run mcp_client_interface.py
Uses OpenAI models
"""

import asyncio
import json
import os

import streamlit as st
from openai import OpenAI
from fastmcp import Client


# Configuration
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:5125/sse")
OPENAI_API_KEY = os.getenv("LLM_API_KEY")


def init_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "tools" not in st.session_state:
        st.session_state.tools = []
    if "mcp_client" not in st.session_state:
        st.session_state.mcp_client = None


async def get_mcp_tools():
    """Fetch available tools from MCP server."""
    try:
        async with Client(MCP_SERVER_URL) as client:
            tools = await client.list_tools()
            # Convert to tool format
            tool_list = []
            for tool in tools:
                tool_list.append({
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                })
            return tool_list, client
    except Exception as e:
        st.error(f"Failed to connect to MCP server: {e}")
        return [], None


async def call_mcp_tool(tool_name: str, tool_input: dict):
    """Call an MCP tool and return the result."""
    try:
        async with Client(MCP_SERVER_URL) as client:
            result = await client.call_tool(tool_name, tool_input)
            if hasattr(result, 'content') and len(result.content) > 0:
                return result.content[0].text
            return str(result)
    except Exception as e:
        return f"Error calling tool: {e}"


def format_tool_use(tool_name: str, tool_input: dict) -> str:
    """Format tool use for display."""
    return f"Using tool: `{tool_name}`\n```json\n{json.dumps(tool_input, indent=2)}\n```"


def main():
    st.set_page_config(
        page_title="MCP Client Interface",
        page_icon="robot",
        layout="wide"
    )

    st.title("MCP Client Interface")
    st.caption("Testing Your MCP Tools with Streamlit")

    init_session_state()

    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")

        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=OPENAI_API_KEY or "",
            help="Get your API key from https://platform.openai.com/api-keys"
        )

        model = st.selectbox(
            "Model",
            ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
            help="Choose which OpenAI model to use"
        )

        # MCP Server URL
        server_url = st.text_input(
            "MCP Server URL",
            value=MCP_SERVER_URL,
            help="Your MCP server URL (e.g., http://localhost:5125/sse)"
        )

        # Load tools button
        if st.button("Load MCP Tools"):
            with st.spinner("Loading tools from MCP server..."):
                tools, _ = asyncio.run(get_mcp_tools())
                st.session_state.tools = tools
                if tools:
                    st.success(f"Loaded {len(tools)} tools")
                else:
                    st.error("No tools found")

        # Display available tools
        if st.session_state.tools:
            st.subheader("Available Tools")
            for tool in st.session_state.tools:
                with st.expander(f"{tool['name']}"):
                    st.write(tool['description'])
                    st.json(tool['input_schema'])

        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    # Main chat interface
    if not api_key:
        st.warning("Please enter your API Key in the sidebar")
        st.info("""
        **To use this interface:**
        1. Get an OpenAI API key
        2. Enter it in the sidebar
        3. Click "Load MCP Tools" to connect to your MCP server
        4. Start chatting!
        """)
        return

    if not st.session_state.tools:
        st.info("Click 'Load MCP Tools' in the sidebar to get started")
        return

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about your MCP tools..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process with OpenAI
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_placeholder = st.empty()
                full_response = process_chat_openai(api_key, prompt, model)
                response_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})


def process_chat_openai(api_key: str, user_message: str, model: str) -> str:
    """Process chat with OpenAI."""
    try:
        client = OpenAI(api_key=api_key)

        # Build conversation history
        messages = [{"role": msg["role"], "content": msg["content"]}
                   for msg in st.session_state.messages]
        messages.append({"role": "user", "content": user_message})

        # Convert MCP tools to OpenAI format
        openai_tools = []
        for tool in st.session_state.tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["input_schema"]
                }
            })

        # Call OpenAI with tools
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=openai_tools,
            tool_choice="auto"
        )

        # Handle tool calls
        response_message = response.choices[0].message

        # Check if there are tool calls
        if response_message.tool_calls:
            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                tool_name = tool_call.function.name
                tool_input = json.loads(tool_call.function.arguments)

                # Display tool use
                st.info(format_tool_use(tool_name, tool_input))

                # Call the MCP tool
                with st.spinner(f"Calling {tool_name}..."):
                    tool_result = asyncio.run(call_mcp_tool(tool_name, tool_input))

                # Add tool response to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": tool_result
                })

            # Get final response
            final_response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            return final_response.choices[0].message.content

        return response_message.content

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    main()
