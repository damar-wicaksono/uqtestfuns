"""
The init for the 'test_functions' subpackage of UQTestFuns.
"""

from .damped_oscillator import DampedOscillator, DampedOscillatorReliability
from .speed_reducer_shaft import SpeedReducerShaft

# NOTE: Import the new test function implementation class from its respective
__all__ = [
    "DampedOscillator",
    "DampedOscillatorReliability",
    "SpeedReducerShaft",
]
# module manually here and update the list below.
