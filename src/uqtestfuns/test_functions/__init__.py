"""
The init for the 'test_functions' subpackage of UQTestFuns.
"""
from .ackley import Ackley
from .borehole import Borehole
from .damped_oscillator import DampedOscillator
from .franke import Franke1, Franke2, Franke3, Franke4
from .flood import Flood
from .ishigami import Ishigami
from .oakley_ohagan_1d import OakleyOHagan1D
from .otl_circuit import OTLCircuit
from .mclain import McLainS1, McLainS2, McLainS3, McLainS4, McLainS5
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
    "Franke1",
    "Franke2",
    "Franke3",
    "Franke4",
    "Ishigami",
    "OakleyOHagan1D",
    "OTLCircuit",
    "McLainS1",
    "McLainS2",
    "McLainS3",
    "McLainS4",
    "McLainS5",
    "Piston",
    "SobolG",
    "Sulfur",
    "WingWeight",
]
