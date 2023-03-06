"""
Test module for instances of meta and random test function specs.
"""
import itertools
import numpy as np
import pytest
import random

from scipy.special import comb

from uqtestfuns.meta.metaspec import UQTestFunSpec, UQMetaFunSpec
from conftest import create_random_marginals


@pytest.fixture
def uqtestfunspec():
    """Create an instance of UQTestFunSpec."""

    # TODO: This is not a very good test because inputs should have been failed

    spatial_dimension = random.randint(1, 25)

    basis_functions = {0: lambda x: x, 1: lambda x: x**2}
    num_basis = len(basis_functions)

    selected_basis = tuple(np.random.randint(0, num_basis, spatial_dimension))

    effects_tuples = {}
    effects_coeffs = {}
    for i in range(1, spatial_dimension + 1):
        effects_tuples[i] = tuple(
            itertools.combinations(np.arange(spatial_dimension), i)
        )
        effects_coeffs[i] = np.random.rand(len(effects_tuples[i]))

    inputs = [{"name": "X1", "distribution": "uniform", "parameters": [0, 1]}]

    my_args = {
        "spatial_dimension": spatial_dimension,
        "basis_functions": basis_functions,
        "selected_basis": selected_basis,
        "effects_tuples": effects_tuples,
        "effects_coeffs": effects_coeffs,
        "inputs": inputs,
    }

    uqtestfunspec_instance = UQTestFunSpec(
        spatial_dimension=spatial_dimension,
        basis_functions=basis_functions,
        selected_basis=selected_basis,
        effects_tuples=effects_tuples,
        effects_coeffs=effects_coeffs,
        inputs=inputs,
    )

    return uqtestfunspec_instance, my_args


def test_create_instance(uqtestfunspec):
    """Test the creation of an instance of UQTestFunSpec."""

    uqtestfunspec_instance, uqtestfunspec_dict = uqtestfunspec

    # Assertions
    assert (
        uqtestfunspec_instance.spatial_dimension
        == uqtestfunspec_dict["spatial_dimension"]
    )
    assert (
        uqtestfunspec_instance.basis_functions
        == uqtestfunspec_dict["basis_functions"]
    )
    assert (
        uqtestfunspec_instance.selected_basis
        == uqtestfunspec_dict["selected_basis"]
    )
    assert (
        uqtestfunspec_instance.effects_tuples
        == uqtestfunspec_dict["effects_tuples"]
    )
    assert (
        uqtestfunspec_instance.effects_coeffs
        == uqtestfunspec_dict["effects_coeffs"]
    )
    # TODO create equality
    assert uqtestfunspec_instance.inputs == uqtestfunspec_dict["inputs"]


def test_create_instance_uqmetafunspec():
    """Test creating an instance of UQMetaFunSpec."""

    # Create an instance
    spatial_dimension = 3

    basis_functions = {0: lambda x: x, 1: lambda x: x**2}

    effects_dict = {
        1: None,
        4: 3,
        2: 1,
        5: None,
        3: 0,
    }

    effects_ref = {
        1: int(comb(spatial_dimension, 1)),
        2: 1,
    }

    input_marginals = create_random_marginals(spatial_dimension)
    coeffs_generator = np.random.rand

    metafun_spec = UQMetaFunSpec(
        spatial_dimension,
        basis_functions,
        effects_dict,
        input_marginals,
        coeffs_generator,
    )

    # Assertions
    assert metafun_spec.spatial_dimension == spatial_dimension
    assert metafun_spec.basis_functions == basis_functions
    assert metafun_spec.effects == effects_ref
    assert metafun_spec.coeffs_generator == coeffs_generator


def _create_args_effects_dict(spatial_dimension):
    """Create a dictionary of effects-length specification."""
    effects_dict = dict()

    for i in range(1, spatial_dimension + 1):
        max_num = int(comb(spatial_dimension, i))
        effects_dict[i] = np.random.randint(1, max_num + 1)

    return effects_dict


def _create_effects_tuples_coeffs(spatial_dimension, coeffs_generator):
    """Create a dictionary of effect tuples and coefficients specifications."""
    effects_tuples = {}
    effects_coeffs = {}
    for i in range(1, spatial_dimension + 1):
        effects_tuples[i] = tuple(
            itertools.combinations(np.arange(spatial_dimension), i)
        )
        effects_coeffs[i] = coeffs_generator(len(effects_tuples[i]))

    return effects_tuples, effects_coeffs


@pytest.mark.parametrize("spatial_dimension", [1, 2, 10])
def test_get_sample_uqmetafunspec(spatial_dimension):
    """Test getting a sample of function specifications realizations."""

    # Create an instance
    spatial_dimension = 1

    basis_functions = {0: lambda x: x}

    effects_dict = _create_args_effects_dict(spatial_dimension)

    inputs = create_random_marginals(spatial_dimension)
    coeffs_generator = np.random.rand

    metafun_spec = UQMetaFunSpec(
        spatial_dimension,
        basis_functions,
        effects_dict,
        inputs,
        coeffs_generator,
    )

    # Get 0 sample
    testfun_spec = metafun_spec.get_sample(0)
    # Assertion
    assert testfun_spec is None

    # Get 1 sample
    testfun_spec = metafun_spec.get_sample()
    # Assertion
    assert isinstance(testfun_spec, UQTestFunSpec)

    selected_basis = testfun_spec.selected_basis
    effects_tuples, effects_coeffs = _create_effects_tuples_coeffs(
        spatial_dimension, coeffs_generator
    )

    # Comparison with test function specification created separately
    testfun_spec_ref = UQTestFunSpec(
        spatial_dimension,
        basis_functions,
        selected_basis,
        effects_tuples,
        effects_coeffs,
        inputs,
    )

    # Assertions
    assert testfun_spec.spatial_dimension == testfun_spec_ref.spatial_dimension
    # TODO: Introduce input equality
    # assert testfun_spec.inputs == testfun_spec_ref.inputs
    assert testfun_spec.selected_basis == testfun_spec_ref.selected_basis
    assert testfun_spec.basis_functions == testfun_spec_ref.basis_functions
    assert testfun_spec.effects_tuples == testfun_spec_ref.effects_tuples

    # Get multiple samples
    sample_size = np.random.randint(2, 11)
    testfun_specs = metafun_spec.get_sample(sample_size)

    # Assertions
    assert isinstance(testfun_specs, list)
    assert len(testfun_specs) == sample_size
    for i in range(sample_size):
        assert isinstance(testfun_specs[i], UQTestFunSpec)
