# Durable MCP Workshop with Temporal

This repository contains a hands-on workshop demonstrating how to build durable MCP tools with Temporal.

## Workshop Overview

This workshop demonstrates two key concepts:

1. **Explore how to create durable MCP tools with Temporal** - How to create MCP tools that can withstand against distributed system challenges like network outages
2. **Build long-running MCP tools** - How to build MCP tools that include durable timers, Signals, and Queries

## Repository Structure

```
├── notebooks/          # Interactive Jupyter notebooks for the workshop
│   ├── Solution        # Solutions for the code-alongs during the workshop
│   ├── Content         # Jupyter notebooks to run during workshop
├── exercises/          # Hands-on exercises for the workshop
│   ├── Practice        # Every chapter will have a Practice dir where students do their work in
│   ├── Solution        # Every chapter will have a Solution dir where students can refer
└── mcp_servers         # Where you will define your MCP servers needed for the Workshop
```

## Prerequisites

- Python 3.13+
- [Claude Desktop](https://claude.ai/download) installed
- [Node v20+](https://nodejs.org/en/download) installed

## Access to Other Repositories

For the demos, you also need these repositories cloned on your local machine.
- [Durable MCP](https://github.com/temporal-community/durable-mcp) for chapter 1
- [Temporal Invoice MCP](https://github.com/Aslan11/temporal-invoice-mcp/) for chapter 2

## Running the Workshop: Codespaces

You can run this workshop on Codespaces as an Exercise Environment.

You can launch an exercise environment for this course using GitHub Codespaces by following [this](codespaces.md) walkthrough.

Before presenting, make sure you have cleared all outputs if you've experiemented with this workshop prior to presenting.
![Clear all outputs](https://i.postimg.cc/RZvQmxLP/clear-all-outputs.png)

## Key Learning Outcomes

By completing this workshop, you'll learn:

1. **Build long-running MCP tools that survive crashes, restarts, and infrastructure failures** which also include durable Timers, Signals, and Queries

2. **Durability and Fault Tolerance** - Build durability and persistence to your MCP tools with Temporal Workflows and test the integration between Claude Desktop, MCP servers, and Temporal workflows

## Contributing

This workshop is designed for educational purposes. Feel free to:
- Submit issues for bugs or unclear instructions
- Propose improvements to the examples
- Share your own AI agent implementations