"""
The init for the 'test_functions' subpackage of UQTestFuns.
"""

from .ackley import Ackley
from .bratley1992 import Bratley1992a, Bratley1992b, Bratley1992c, Bratley1992d
from .cantilever_beam_2d import CantileverBeam2D
from .circular_pipe_crack import CircularPipeCrack
from .coffee_cup import CoffeeCup
from .damped_cosine import DampedCosine
from .damped_oscillator import DampedOscillator, DampedOscillatorReliability
from .dette import Dette8D, DetteCurved, DetteExp
from .flood import Flood
from .forrester import Forrester2008
from .four_branch import FourBranch
from .friedman import Friedman6D, Friedman10D
from .gayton_hat import GaytonHat
from .genz import (
    GenzDiscontinuous,
    GenzContinuous,
    GenzCornerPeak,
    GenzGaussian,
    GenzOscillatory,
    GenzProductPeak,
)
from .higdon_sine import HigdonSine
from .holsclaw_sine import HolsclawSine
from .ishigami import Ishigami
from .lim import LimPoly, LimNonPoly
from .linkletter import (
    LinkletterDecCoeffs,
    LinkletterInert,
    LinkletterLinear,
    LinkletterSine,
)
from .otl_circuit import OTLCircuit
from .moon3d import Moon3D
from .morris2006 import Morris2006
from .piston import Piston
from .portfolio_3d import Portfolio3D
from .robot_arm import RobotArm
from .rosenbrock import Rosenbrock
from .rs_circular_bar import RSCircularBar
from .saltelli_linear import SaltelliLinear
from .sobol_g import SobolG
from .sobol_g_star import SobolGStar
from .sobol_levitan import SobolLevitan
from .solar_cell import SolarCell
from .speed_reducer_shaft import SpeedReducerShaft
from .sulfur import Sulfur
from .undamped_oscillator import UndampedOscillator
from .welch1992 import Welch1992
from .wing_weight import WingWeight

# NOTE: Import the new test function implementation class from its respective
__all__ = [
    "Ackley",
    "Bratley1992a",
    "Bratley1992b",
    "Bratley1992c",
    "Bratley1992d",
    "CantileverBeam2D",
    "CircularPipeCrack",
    "CoffeeCup",
    "DampedCosine",
    "DampedOscillator",
    "DampedOscillatorReliability",
    "Dette8D",
    "DetteCurved",
    "DetteExp",
    "Flood",
    "Forrester2008",
    "FourBranch",
    "Friedman6D",
    "Friedman10D",
    "GaytonHat",
    "GenzContinuous",
    "GenzCornerPeak",
    "GenzDiscontinuous",
    "GenzGaussian",
    "GenzOscillatory",
    "GenzProductPeak",
    "HigdonSine",
    "HolsclawSine",
    "Ishigami",
    "LimNonPoly",
    "LimPoly",
    "LinkletterDecCoeffs",
    "LinkletterInert",
    "LinkletterLinear",
    "LinkletterSine",
    "OTLCircuit",
    "Moon3D",
    "Morris2006",
    "Piston",
    "Portfolio3D",
    "RobotArm",
    "Rosenbrock",
    "RSCircularBar",
    "SaltelliLinear",
    "SobolG",
    "SobolGStar",
    "SobolLevitan",
    "SolarCell",
    "SpeedReducerShaft",
    "Sulfur",
    "UndampedOscillator",
    "Welch1992",
    "WingWeight",
]
# module manually here and update the list below.
