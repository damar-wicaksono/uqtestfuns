"""
The init for the 'test_functions' subpackage of UQTestFuns.
"""

from .ackley import Ackley
from .alemazkoor import Alemazkoor2D, Alemazkoor20D
from .borehole import Borehole
from .bratley1992 import Bratley1992a, Bratley1992b, Bratley1992c, Bratley1992d
from .cantilever_beam_2d import CantileverBeam2D
from .cheng2010 import Cheng2D
from .circular_pipe_crack import CircularPipeCrack
from .convex_fail_domain import ConvexFailDomain
from .damped_cosine import DampedCosine
from .damped_oscillator import DampedOscillator, DampedOscillatorReliability
from .flood import Flood
from .forrester import Forrester2008
from .four_branch import FourBranch
from .franke import Franke1, Franke2, Franke3, Franke4, Franke5, Franke6
from .friedman import Friedman6D, Friedman10D
from .gayton_hat import GaytonHat
from .gramacy2007 import Gramacy1DSine
from .hyper_sphere import HyperSphere
from .ishigami import Ishigami
from .lim import LimPoly, LimNonPoly
from .oakley2002 import Oakley1D
from .otl_circuit import OTLCircuit
from .mclain import McLainS1, McLainS2, McLainS3, McLainS4, McLainS5
from .moon3d import Moon3D
from .morris2006 import Morris2006
from .piston import Piston
from .portfolio_3d import Portfolio3D
from .rs_circular_bar import RSCircularBar
from .rs_quadratic import RSQuadratic
from .saltelli_linear import SaltelliLinear
from .sobol_g import SobolG
from .sobol_g_star import SobolGStar
from .speed_reducer_shaft import SpeedReducerShaft
from .sulfur import Sulfur
from .webster import Webster2D
from .welch1992 import Welch1992
from .wing_weight import WingWeight

# NOTE: Import the new test function implementation class from its respective
# module manually here and update the list below.

__all__ = [
    "Ackley",
    "Alemazkoor2D",
    "Alemazkoor20D",
    "Borehole",
    "Bratley1992a",
    "Bratley1992b",
    "Bratley1992c",
    "Bratley1992d",
    "CantileverBeam2D",
    "Cheng2D",
    "CircularPipeCrack",
    "ConvexFailDomain",
    "DampedCosine",
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
    "Friedman6D",
    "Friedman10D",
    "GaytonHat",
    "Gramacy1DSine",
    "HyperSphere",
    "Ishigami",
    "LimNonPoly",
    "LimPoly",
    "Oakley1D",
    "OTLCircuit",
    "McLainS1",
    "McLainS2",
    "McLainS3",
    "McLainS4",
    "McLainS5",
    "Moon3D",
    "Morris2006",
    "Piston",
    "Portfolio3D",
    "RSCircularBar",
    "RSQuadratic",
    "SaltelliLinear",
    "SobolG",
    "SobolGStar",
    "SpeedReducerShaft",
    "Sulfur",
    "Webster2D",
    "Welch1992",
    "WingWeight",
]
