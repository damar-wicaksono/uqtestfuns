"""
The init for the 'test_functions' subpackage of UQTestFuns.
"""
from .ackley import Ackley
from .borehole import Borehole
from .damped_oscillator import DampedOscillator
from .flood import Flood
from .ishigami import Ishigami
from .oakley_ohagan_1d import OakleyOHagan1D
from .otl_circuit import OTLCircuit
from .piston import Piston
from .sobol_g import SobolG
from .sulfur import Sulfur
from .wing_weight import WingWeight

# NOTE: Import the new test function implementation class from its respective
# module manually here and update the list below.

__all__ = [
    "Ackley",
    "Borehole",
    "DampedOscillator",
    "Flood",
    "Ishigami",
    "OakleyOHagan1D",
    "OTLCircuit",
    "Piston",
    "SobolG",
    "Sulfur",
    "WingWeight",
]
