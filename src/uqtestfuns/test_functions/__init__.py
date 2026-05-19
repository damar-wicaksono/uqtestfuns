"""
The init for the 'test_functions' subpackage of UQTestFuns.
"""

from .damped_oscillator import DampedOscillator, DampedOscillatorReliability
from .four_branch import FourBranch
from .robot_arm import RobotArm
from .solar_cell import SolarCell
from .speed_reducer_shaft import SpeedReducerShaft
from .sulfur import Sulfur

# NOTE: Import the new test function implementation class from its respective
__all__ = [
    "DampedOscillator",
    "DampedOscillatorReliability",
    "FourBranch",
    "RobotArm",
    "SolarCell",
    "SpeedReducerShaft",
    "Sulfur",
]
# module manually here and update the list below.
