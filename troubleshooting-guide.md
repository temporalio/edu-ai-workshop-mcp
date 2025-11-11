# Troubleshooting Guide

## Common Issues and Solutions

### 1. Restarting a Worker After Code Changes

If you make changes to your Workflow or Activity code, you need to restart the worker for the changes to take effect. In your notebook, either find a cell that does this or create one.

a. On the top left of the screen click the `+ Code` button:

![Add a Codeblock](https://i.postimg.cc/Jh7ZDGCz/add-codeblock.png)

b. The codeblock to kill and restart the worker should contain:

```python
import asyncio

# Cancel the existing worker
x = worker.cancel()

# Restart the worker
worker = asyncio.create_task(run_worker())
```

### 2. Checking Running Workers

To see what workers are currently running, create a codeblock (see 1a):

```python
# Check if worker task is running
if worker and not worker.done():
    print("Worker is running")
else:
    print("Worker is not running")

# Get more details about the worker task
print(f"Worker task: {worker}")
print(f"Worker done: {worker.done()}")
print(f"Worker cancelled: {worker.cancelled()}")
```

### 3. Handling Workflow Task Errors

If there's an issue like a typo in your workflow code, it will cause a workflow task error. When this happens, the notebook block will run forever because it's blocking on the stalled workflow.

**Solution:**
- Click the **'Interrupt'** button in Jupyter notebook:

![Interrupt cell](https://i.postimg.cc/mrdXhvJz/interrupt-kernel.png)

- Fix the typo or error in your code
- Restart the Worker using the code block in section 1 above
- Re-run your Workflow

## MCP Issues

- If your tools aren't loading, verify that port 5125 is set to **Public** in the Ports tab. Right-click the port → Port Visibility → Public.