"""
The init for the 'test_functions' subpackage of UQTestFuns.
"""

from .ackley import Ackley
from .bratley1992 import Bratley1992a, Bratley1992b, Bratley1992c, Bratley1992d
from .cantilever_beam_2d import CantileverBeam2D
from .circular_pipe_crack import CircularPipeCrack
from .coffee_cup import CoffeeCup
from .damped_oscillator import DampedOscillator, DampedOscillatorReliability
from .flood import Flood
from .four_branch import FourBranch
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
    "DampedOscillator",
    "DampedOscillatorReliability",
    "Flood",
    "FourBranch",
    "GenzContinuous",
    "GenzCornerPeak",
    "GenzDiscontinuous",
    "GenzGaussian",
    "GenzOscillatory",
    "GenzProductPeak",
    "HigdonSine",
    "HolsclawSine",
    "Ishigami",
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
    "WingWeight",
]
# module manually here and update the list below.
