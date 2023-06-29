"""
The init for the 'test_functions' subpackage of UQTestFuns.
"""
from .ackley import Ackley
from .borehole import Borehole
from .bratley1992 import Bratley1992a, Bratley1992b, Bratley1992c, Bratley1992d
from .cantilever_beam_2d import CantileverBeam2D
from .circular_pipe_crack import CircularPipeCrack
from .damped_oscillator import DampedOscillator, DampedOscillatorReliability
from .flood import Flood
from .forrester import Forrester2008
from .four_branch import FourBranch
from .franke import Franke1, Franke2, Franke3, Franke4, Franke5, Franke6
from .gayton_hat import GaytonHat
from .gramacy2007 import Gramacy1DSine
from .hyper_sphere import HyperSphere
from .ishigami import Ishigami
from .oakley2002 import Oakley1D
from .otl_circuit import OTLCircuit
from .mclain import McLainS1, McLainS2, McLainS3, McLainS4, McLainS5
from .piston import Piston
from .sobol_g import SobolG
from .speed_reducer_shaft import SpeedReducerShaft
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
    "CantileverBeam2D",
    "CircularPipeCrack",
    "DampedOscillator",
    "DampedOscillatorReliability",
    "Flood",
    "Forrester2008",
    "FourBranch",
    "Franke1",
    "Franke2",
    "Franke3",
    "Franke4",
    "Franke5",
    "Franke6",
    "GaytonHat",
    "Gramacy1DSine",
    "HyperSphere",
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
    "SpeedReducerShaft",
    "Sulfur",
    "Welch1992",
    "WingWeight",
]
