"""
The init for the 'test_functions' subpackage of UQTestFuns.
"""
from .ackley import Ackley
from .borehole import Borehole
from .bratley1992 import Bratley1992a, Bratley1992b, Bratley1992c, Bratley1992d
from .damped_oscillator import DampedOscillator
from .flood import Flood
from .forrester import Forrester2008
from .franke import Franke1, Franke2, Franke3, Franke4, Franke5, Franke6
from .gramacy2007 import Gramacy1DSine
from .ishigami import Ishigami
from .oakley2002 import Oakley1D
from .otl_circuit import OTLCircuit
from .mclain import McLainS1, McLainS2, McLainS3, McLainS4, McLainS5
from .piston import Piston
from .sobol_g import SobolG
from .sulfur import Sulfur
from .welch1992 import Welch1992
from .wing_weight import WingWeight

# NOTE: Import the new test function implementation class from its respective
# module manually here and update the list below.

__all__ = [
    "Ackley",
    "Borehole",
    "Bratley1992a",
    "Bratley1992b",
    "Bratley1992c",
    "Bratley1992d",
    "DampedOscillator",
    "Flood",
    "Forrester2008",
    "Franke1",
    "Franke2",
    "Franke3",
    "Franke4",
    "Franke5",
    "Franke6",
    "Gramacy1DSine",
    "Ishigami",
    "Oakley1D",
    "OTLCircuit",
    "McLainS1",
    "McLainS2",
    "McLainS3",
    "McLainS4",
    "McLainS5",
    "Piston",
    "SobolG",
    "Sulfur",
    "Welch1992",
    "WingWeight",
]
