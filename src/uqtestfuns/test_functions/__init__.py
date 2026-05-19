"""
The init for the 'test_functions' subpackage of UQTestFuns.
"""

from .damped_oscillator import DampedOscillatorReliability

# NOTE: Import the new test function implementation class from its respective
__all__ = [
    "DampedOscillatorReliability",
]
# module manually here and update the list below.
