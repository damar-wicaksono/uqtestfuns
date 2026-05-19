"""
The init for the 'test_functions' subpackage of UQTestFuns.
"""

from .damped_oscillator import DampedOscillator, DampedOscillatorReliability
from .robot_arm import RobotArm
from .speed_reducer_shaft import SpeedReducerShaft

# NOTE: Import the new test function implementation class from its respective
__all__ = [
    "DampedOscillator",
    "DampedOscillatorReliability",
    "RobotArm",
    "SpeedReducerShaft",
]
# module manually here and update the list below.
