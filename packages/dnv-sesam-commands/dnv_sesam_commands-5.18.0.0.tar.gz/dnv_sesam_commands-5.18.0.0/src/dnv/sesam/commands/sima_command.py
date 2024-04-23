from typing import Any, Dict, Optional

from dnv.onecompute import FileSpecification

from .executable_command_base import ExecutableCommandBase


class SimaCommand(ExecutableCommandBase):
    """
    Represents a Sima command that extends the ExecutableCommandBase class.

    This class is used to encapsulate a Sima command with its associated inputs and commands.

    For more information on inputs and commands, see the SIMA documentation:
    https://sima.sintef.no/doc/4.6.0/userguide/Running_SIMA_Without_Graphical_User_Interface.html

    Attributes:
        working_dir (str): The working directory for the Sima command.
        inputs (Dict[str, Any], optional): A dictionary where each key-value pair represents a
            single input argument for the Sima command.
        commands (Dict[str, Any], optional): A dictionary where each key-value pair represents a
            single command to be executed by the worker.
        DEFAULT_OUTPUT_FILES_TO_INCLUDE (List[str]): Default list of glob patterns for output files
            to include after the Sima command execution. Files matching to this default list of
            patterns will be moved from their locations to the command's working directory during
            the file moving process.
        LOG_LEVEL (str): The level of logging to be used. Default is "ALL" for logging all messages.
        DATA_PATH (str): The path to the data directory. Default is "." to use the current
            directory.
    """

    DEFAULT_OUTPUT_FILES_TO_INCLUDE = [
        "*-sima.lis",
        "variable*.inp",
        "*.log",
        "results.tda",
        "results.txt",
        "sima_*.res",
        "sys-sima.dat",
        "sima_*.bin",
        "key_sima_*.txt",
        "sima.*",
    ]

    LOG_LEVEL: str = "ALL"
    DATA_PATH: str = "."

    def __init__(
        self,
        working_dir: str = "",
        inputs: Optional[Dict[str, Any]] = None,
        commands: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes a new instance of the SimaCommand class.

        Args:
            working_dir (str, optional): The working directory for the Sima command.
                Defaults to an empty string.
            inputs (Dict[str, Any], optional): A dictionary where each key-value pair represents a
                single input argument for the Sima command. Defaults to None.
            commands (Dict[str, Any], optional): A dictionary where each key-value pair represents a
                single command to be executed by the worker. Defaults to None.
        """
        super().__init__(working_dir)
        # The following attributes are named in PascalCase due to compatibility with an existing
        # codebase or API. Pylint warnings are disabled for these lines to allow this naming
        # convention.
        self.Inputs = inputs  # pylint: disable=invalid-name
        self.Commands = commands  # pylint: disable=invalid-name

    @property
    def type(self) -> str:
        """
        Gets the type of command.

        Returns:
            A string representing the type of command.
        """
        return "DNV.Sesam.Commons.HydroCommands.Sima.SimaCommand, DNV.Sesam.Commons.HydroCommands"

    @property
    def inputs(self) -> Optional[Dict[str, Any]]:
        """
        Gets the dictionary of inputs for the Sima command.

        Returns:
            A dictionary where each key-value pair represents a single input argument for the Sima
            command.
        """
        return self.Inputs

    @inputs.setter
    def inputs(self, value: Optional[Dict[str, Any]]):
        """
        Sets the dictionary of inputs for the Sima command.

        Args:
            value (Dict[str, Any]): A dictionary where each key-value pair represents a single input
                argument for the Sima command.
        """
        self.Inputs = value

    @property
    def commands(self) -> Optional[Dict[str, Any]]:
        """
        Gets the dictionary of commands to be executed by the worker.

        Returns:
            A dictionary where each key-value pair represents a single command to be executed by
            the worker.
        """
        return self.Commands

    @commands.setter
    def commands(self, value: Optional[Dict[str, Any]]):
        """
        Sets the dictionary of commands to be executed by the worker.

        Args:
            value (Dict[str, Any]): A dictionary where each key-value pair represents a single
            command to be executed by the worker.
        """
        self.Commands = value

    @staticmethod
    def create_sima_command(
        task_name: str,
        workflow_name: str,
        sima_case_data: Dict[str, Any],
        stask_filename: str,
        stask_foldername: str,
        is_stask_file_in_shared_folder: bool = True,
    ) -> "SimaCommand":
        """
        Constructs an instance of SimaCommand.

        Args:
            task_name (str): The name of the task to be run.
            workflow_name (str): The name of the workflow to be run.
            case_data (Dict[str, Any]): The data for the case. This data will be used to construct
                the input for SIMA.
            stask_filename (str): The name of the stask file. This filename will be used as an input
                for the SIMA command.
            stask_foldername (str): The name of the folder containing the stask file. This folder
                name will be used as an input for the SIMA command.
            is_stask_file_in_shared_folder (bool): A flag indicating whether the stask file is
                located in a shared folder. Defaults to True.
        Returns:
        """
        cmd = SimaCommand()
        cmd.inputs = SimaCommand.construct_inputs(sima_case_data)
        cmd.commands = SimaCommand.construct_commands(
            task_name,
            workflow_name,
            stask_filename,
            stask_foldername,
            is_stask_file_in_shared_folder,
        )
        cmd.should_move_output_files = True
        cmd.output_files_to_include = SimaCommand.DEFAULT_OUTPUT_FILES_TO_INCLUDE
        return cmd

    @staticmethod
    def construct_commands(
        task_name: str,
        workflow_name: str,
        stask_filename: str,
        stask_foldername: str,
        is_stask_file_in_shared_folder: bool = True,
    ) -> Dict[str, Any]:
        """
        Constructs the commands for a Sima task.

        Args:
            task_name (str): The name of the task to be run.
            workflow_name (str): The name of the workflow to be run.
            stask_filename (str): The name of the stask file. This filename will be used as an input
                for the SIMA command.
            stask_foldername (str): The name of the folder containing the stask file. This folder
                name will be used as an input for the SIMA command.
            is_stask_file_in_shared_folder (bool): A flag indicating whether the stask file is
                located in a shared folder.

        Returns:
            Dict[str, Any]: A dictionary of commands for the Sima task.
        """
        commands = {
            "--consoleLog": "",
            "--log-level": SimaCommand.LOG_LEVEL,
            "--data": SimaCommand.DATA_PATH,
            "--import": {
                "file": FileSpecification(
                    sharedfolder=is_stask_file_in_shared_folder,
                    directory=stask_foldername,
                    filename=stask_filename,
                )
            },
            "--run": {"task": task_name, "workflow": workflow_name},
        }

        return commands

    @staticmethod
    def construct_inputs(case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Constructs the inputs for a Sima case.

        Args:
            case (Dict[str, Any]): The data for the SIMA case.

        Returns:
            Dict[str, Any]: A dictionary of inputs for the SIMA case.
        """
        return case
