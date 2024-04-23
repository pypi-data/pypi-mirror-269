# SesamCommands: Streamlining Sesam Workflows

For developers seeking to simplify the development and execution of Sesam workflows on both local and cloud platforms, the SesamCommands is an invaluable Python package. It empowers you to execute Sesam Core, Wasim, and Sestra applications within your workflows. The intricacies involved in the execution and management of workflows are taken care of by OneWorkflow and OneCompute Python packages. In summary, the SesamCommands Python library is optimal for developers aiming to enhance their Sesam workflow development process.

## Usage and Examples

For a more comprehensive understanding and additional examples, please visit the Homepage link provided on this page.

```python
"""Demonstration of executing a SesamCoreCommand using the OneWorkflow client asynchronously."""

# Import necessary modules and functions
import asyncio
from dnv.oneworkflow.utils import (
    CommandInfo,
    one_workflow_client,
    run_managed_commands_in_parallel_async,
)
from dnv.sesam.commands import SesamCoreCommand

# Instantiate the OneWorkflow client with workspace ID and path
client = one_workflow_client(
    workspace_id="TestWorkflow", workspace_path=r"C:\MyWorkspace", cloud_run=False
)

# Create an instance of the SesamCoreCommand class, specifying the command, input file name, and options
sesam_core_command = SesamCoreCommand(
    command="uls", input_file_name="input.json", options="-v"
)

# Create an instance of the CommandInfo class, specifying the commands and load case folder name
cmd_info = CommandInfo(
    commands=[sesam_core_command],
    load_case_foldername="LoadCase1",
)

# Run workflow/command asynchronously
asyncio.run(
    run_managed_commands_in_parallel_async(
        client=client,
        commands_info=[cmd_info],
    )
)
```
