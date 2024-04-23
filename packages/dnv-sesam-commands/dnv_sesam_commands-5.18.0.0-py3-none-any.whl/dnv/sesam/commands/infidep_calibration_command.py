from .executable_command_base import ExecutableCommandBase
from typing import Optional

class CalibrationCommand(ExecutableCommandBase):
    """
    The base class for the Sesam core commands.
    """

    def __init__(
        self,
        input_file_name: Optional[str] = None,
        calibration_directory: Optional[str] = None,
        quick_mode: bool = False
    ):
        super().__init__(working_dir="")
        self.input_file_name = input_file_name
        self.calibration_directory = calibration_directory
        self.quick_mode = quick_mode

    @property
    def type(self) -> str:
        """
        Get the type of the command.

        Returns:
            str: The type of the command.
        """
        return "DNV.Sesam.Commons.SesamCommands.Infidep.CalibrationCommand, DNV.Sesam.Commons.SesamCommands"

    @property
    def input_file_name(self) -> str:
        """
        Gets the name of the calibration input file.

        Returns:
            str: A string representing the name of the calibration input file.
        """
        return self.InputFilename

    @input_file_name.setter
    def input_file_name(self, value: str):
        """
        Sets the name of the calibration input file.

        Args:
            value (str): The name of the calibration input file.
        """
        self.InputFilename = value

    @property
    def calibration_directory(self) -> str:
        """
        Gets the path to the directory containing the calibration code. This should be 
        None for cloud runs.

        Returns:
            str: A string representing the path of the directory containing the calibration code.
        """
        return self.CalibrationDirectory

    @calibration_directory.setter
    def calibration_directory(self, value: str):
        """
        Sets the path to the directory containing the calibration code. This should be 
        left as None for cloud runs.

        Args:
            value (str): The path of the directory containing the calibration code.
        """
        self.CalibrationDirectory = value

    @property
    def quick_mode(self) -> str:
        """
        Gets a flag indicating whether the calibration should run in quick mode. In quick mode, only
        two calbration cycles are performed. This will produce incorrect results, but allows the 
        workflow to be tested quickly.

        Returns:
            bool: A bool indicating whether the calibration will run in quick mode.
        """
        return self.QuickMode

    @quick_mode.setter
    def quick_mode(self, value: bool):
        """
        Sets a flag indicating whether the calibration should run in quick mode. In quick mode, only
        two calbration cycles are performed. This will produce incorrect results, but allows the 
        workflow to be tested quickly.

        Args:
            value (bool): A bool indicating whether the calibration will run in quick mode.
        """
        self.QuickMode = value
