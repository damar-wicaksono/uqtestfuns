"""
The init for the 'test_functions' subpackage of UQTestFuns.
"""

from .ackley import Ackley
from .damped_oscillator import DampedOscillator, DampedOscillatorReliability
from .four_branch import FourBranch
from .genz import (
    GenzDiscontinuous,
    GenzContinuous,
    GenzCornerPeak,
    GenzGaussian,
    GenzOscillatory,
    GenzProductPeak,
)
from .robot_arm import RobotArm
from .sobol_levitan import SobolLevitan
from .solar_cell import SolarCell
from .speed_reducer_shaft import SpeedReducerShaft
from .sulfur import Sulfur

# NOTE: Import the new test function implementation class from its respective
__all__ = [
    "Ackley",
    "DampedOscillator",
    "DampedOscillatorReliability",
    "FourBranch",
    "GenzContinuous",
    "GenzCornerPeak",
    "GenzDiscontinuous",
    "GenzGaussian",
    "GenzOscillatory",
    "GenzProductPeak",
    "RobotArm",
    "SobolLevitan",
    "SolarCell",
    "SpeedReducerShaft",
    "Sulfur",
]
# module manually here and update the list below.
