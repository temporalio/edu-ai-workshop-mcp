# Durable MCP Workshop with Temporal

This repository contains a hands-on workshop demonstrating how to build durable MCP tools with Temporal.

## How to Use this Repository

1. To present this workshop, present in Codespace so that students don't need to download any software on their machines. To do so, refer to [this document](./codespaces.md).
2. This repository contains the Jupyter notebooks under [the notebooks directory](./notebooks). The notebooks are used as an educational tool for students to get practice with being hands-on with Temporal. 
3. The slides that accompany the Jupyter notebooks are [here](https://docs.google.com/presentation/d/1MF9Rm-Ii5QjI1BVnRmuSZtHuV0NAA-besDfcongG6VU/edit?usp=drive_link).
4. The instructor goes through the slides. When there is a a little icon of a person at a keyboard on the bottom right of the slides, this lets students know that it's time to get hands-on and move to the notebooks.
5. There will also be time for students to practice working independently with the material in the [exercises directory](./exercises/). The Jupyter notebooks will reference when it's time to do work on an exercise directory.
6. For the self-serve version of this workshop (no need for slides), refer to the `self-serve-version` branch on this repository.

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
- [OpenAI API Key](https://platform.openai.com/api-keys)

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

2. **Durability and Fault Tolerance** - Build durability and persistence to your MCP tools with Temporal Workflows and test the integration between MCP Clients, MCP servers, and Temporal workflows

## Contributing

This workshop is designed for educational purposes. Feel free to:
- Submit issues for bugs or unclear instructions
- Propose improvements to the examples
- Share your own AI agent implementations