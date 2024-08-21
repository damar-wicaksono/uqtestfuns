"""
Test module for the prob. input specification class.
"""

from typing import List

from uqtestfuns.core.prob_input.input_spec import (
    UnivDistSpec,
    ProbInputSpecFixDim,
    ProbInputSpecVarDim,
)


def test_marginalspec():
    """Test the creation of MarginalSpec NamedTuple."""

    name = "T0"
    distribution = "uniform"
    parameters = [340.0, 360.0]
    description = "Filling gas temperature"

    # Create a MarginalSpec
    my_marginalspec = UnivDistSpec(
        name=name,
        distribution=distribution,
        parameters=parameters,
        description=description,
    )

    # Assertions
    assert my_marginalspec.name == name
    assert my_marginalspec.distribution == distribution
    assert my_marginalspec.parameters == parameters
    assert my_marginalspec.description == description


def test_probinputspec_list():
    """Test the creation of ProbInputSpec NamedTuple w/ list of marginals."""

    # Create a list of marginals
    marginals = _create_marginals(10)

    # Create a ProbInputSpec
    name = "Some input"
    description = "Probabilistic input model from somewhere"
    copulas = None
    my_probinputspec = ProbInputSpecFixDim(
        name=name,
        description=description,
        marginals=marginals,
        copulas=copulas,
    )

    # Assertions
    assert my_probinputspec.name == name
    assert my_probinputspec.description == description
    assert my_probinputspec.copulas == copulas
    assert my_probinputspec.marginals == marginals


def test_probinputspec_vardim():
    """Test the creation of ProbInputSpec w/ a callable as marginal."""

    # Create a list of marginals
    marginals_gen = _create_marginals

    # Create a ProbInputSpec
    name = "Some input"
    description = "Probabilistic input model from somewhere"
    copulas = None
    my_probinputspec = ProbInputSpecVarDim(
        name=name,
        description=description,
        marginals_generator=marginals_gen,
        copulas=copulas,
    )

    # Assertions
    assert my_probinputspec.name == name
    assert my_probinputspec.description == description
    assert my_probinputspec.copulas == copulas
    assert my_probinputspec.marginals_generator == marginals_gen


def _create_marginals(spatial_dimension: int) -> List[UnivDistSpec]:
    """Create a list of test marginals."""
    return [
        UnivDistSpec(
            name=f"x{i + 1}",
            distribution="uniform",
            parameters=[0.0, 1.0],
            description="None",
        )
        for i in range(spatial_dimension)
    ]
