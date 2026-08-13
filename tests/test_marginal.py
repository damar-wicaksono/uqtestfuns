"""Tests for the Marginal class."""

import numpy as np
import pytest

from conftest import create_random_alphanumeric

from uqtestfuns.core.prob_input.marginal import Marginal
from uqtestfuns.core.prob_input.utils import SUPPORTED_MARGINALS


def _id_distribution(distribution):
    return f"{distribution:<12}"


@pytest.fixture(params=SUPPORTED_MARGINALS, ids=_id_distribution)
def univariate_distribution(request):
    """Return marginal distribution fixture."""
    return request.param


def _id_marginal_named(named):
    return f"named={str(named):<5}"


@pytest.fixture(params=[True, False], ids=_id_marginal_named)
def marginal_name(request):
    """Return marginal name fixture."""
    if request.param:
        return create_random_alphanumeric(2)
    else:
        return None


def _random_parameters(
    distribution: str,
    rng: np.random.Generator,
) -> np.ndarray:
    """Return valid random parameters for a supported marginal distribution."""

    if distribution == "beta":
        return np.sort(1 + 2 * rng.random(4))

    if distribution == "exponential":
        return 1 + rng.random(1)

    if distribution == "triangular":
        bounds = np.sort(1 + 2 * rng.random(2))
        mode = rng.uniform(bounds[0], bounds[1])
        return np.array([bounds[0], bounds[1], mode])

    if distribution in ["trunc-normal", "trunc-gumbel"]:
        lower, location, upper = np.sort(1 + 2 * rng.random(3))
        scale = 0.5 + rng.random()
        return np.array([location, scale, lower, upper])

    if distribution == "lognormal":
        return 1 + rng.random(2)

    # Other generic distributions
    return np.sort(1 + 2 * rng.random(2))


@pytest.fixture
def marginal(univariate_distribution, marginal_name) -> Marginal:
    """Create a random marginal distribution."""
    rng = np.random.default_rng(42)
    parameters = _random_parameters(univariate_distribution, rng)

    return Marginal(
        name=marginal_name,
        distribution=univariate_distribution,
        parameters=parameters,
    )


def test_str(marginal: Marginal):
    """Test the string representation of a marginal distribution instance."""
    my_str = str(marginal)

    # Assertions
    assert isinstance(my_str, str)
    name = marginal.name
    if name is not None:
        assert name in my_str
