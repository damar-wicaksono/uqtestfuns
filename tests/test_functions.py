"""Tests for UQTestFuns test function construction, evaluation, and API.

This module contains comprehensive tests for creating and using
UQ test functions, including construction via the API,
parameter/input ID handling, dimension validation,
function evaluation, sampling, input transformation, and string representation.
"""

import copy
import numpy as np
import pytest
import random
import string

import uqtestfuns as uqtf

from uqtestfuns import UQTestFun, Marginal
from uqtestfuns.core.parameters import Parameters, ParametersProtectedError
from uqtestfuns.core.prob_input.probabilistic_input_new import ProbInput
from uqtestfuns.api import create
from uqtestfuns.core.registry.entries import UQTestFunInfo


def random_string(length):
    letters = string.ascii_letters  # a-z and A-Z
    return "".join(random.choice(letters) for _ in range(length))


def assert_equal(f1: UQTestFun, f2: UQTestFun) -> None:
    """Assert that two UQTestFun instances are equal in value."""
    assert isinstance(f1, UQTestFun)
    assert isinstance(f2, UQTestFun)
    assert f1.name == f2.name
    assert f1.description == f2.description
    assert f1._evaluate == f2._evaluate
    assert f1.prob_input == f2.prob_input

    # --- Assert parameter equality
    f1_params = f1.parameters
    f2_params = f2.parameters
    if f1_params is not None and f2_params is not None:

        assert isinstance(f1.name, str)
        assert isinstance(f1_params.name, str)
        if "SobolGStar" in f1.name and "Saltelli2010" in f1_params.name:
            # 'Saltelli2010-*' parameter set has randomness
            assert True
            return

        for v_1, v_2 in zip(f1_params.values(), f2_params.values()):
            if isinstance(v_1, np.ndarray) and isinstance(v_2, np.ndarray):
                assert np.array_equal(v_1, v_2)
            else:
                assert v_1 == v_2


@pytest.fixture(params=[1, 3, 5])
def input_dimension(request) -> int:
    return request.param


def test_dir_includes_registered_names(builtin_name: str):
    """Test that the module's dir includes all registered function names."""
    assert builtin_name in dir(uqtf)


def test_factory_metadata(builtin_name: str, info: UQTestFunInfo):
    """Test that the factory function has the correct metadata."""
    factory = getattr(uqtf, builtin_name)

    # Assertions
    assert factory.__name__ == builtin_name
    assert factory.__doc__ == info.description


class TestConstruction:

    def test_props_fixed_dim(self, builtin_name: str, info: UQTestFunInfo):
        """Test the properties of a fixed-dimension UQ test function."""
        if info.variable_dimension:
            pytest.skip(f"{builtin_name} is variable dimension")

        f = create(builtin_name)

        # Assertions
        assert f.name == info.name
        assert f.input_dimension == info.input_dimension
        assert f.output_dimension == info.output_dimension
        assert f.description == info.description

    def test_props_var_dim(self, builtin_name: str, info: UQTestFunInfo):
        """Test the properties of a variable-dimension UQ test function."""
        if not info.variable_dimension:
            pytest.skip(f"{builtin_name} is fixed dimension")

        input_dim = 5
        f = create(builtin_name, input_dimension=input_dim)

        # Assertions
        assert f.name == info.name
        assert f.input_dimension == input_dim
        assert f.output_dimension == info.output_dimension
        assert f.description == info.description

    def test_create_fixed_dim_default(
        self,
        builtin_name: str,
        info: UQTestFunInfo,
    ):
        """Test creating a default fixed-dim UQ test function."""
        if info.variable_dimension:
            pytest.skip(f"{builtin_name} is not fixed dimension")

        f1 = create(builtin_name)
        f2 = getattr(uqtf, builtin_name)()

        # Assertion
        assert_equal(f1, f2)

    def test_create_var_dim_default(
        self,
        builtin_name: str,
        input_dimension: int,
        info: UQTestFunInfo,
    ):
        """Test creating a default variable-dim UQ test function."""
        if not info.variable_dimension:
            pytest.skip(f"{builtin_name} is not variable dimension")

        f_1 = create(builtin_name, input_dimension=input_dimension)
        f_2 = getattr(uqtf, builtin_name)(input_dimension=input_dimension)

        assert_equal(f_1, f_2)

    def test_create_input_id(self, builtin_name: str, info: UQTestFunInfo):
        """Test creating a UQ test function with input_id."""

        if info.input_dimension is None:
            input_dim = 5
        else:
            input_dim = info.input_dimension

        for input_id in info.available_input_ids.keys():
            f_1 = create(builtin_name, input_dim, input_id=input_id)
            f_2 = getattr(uqtf, builtin_name)(input_dim, input_id=input_id)

            assert_equal(f_1, f_2)

    def test_create_params_id(self, builtin_name: str, info: UQTestFunInfo):
        """Test creating a UQ test function with parameters_id."""

        if info.input_dimension is None:
            input_dim = 15
        else:
            input_dim = info.input_dimension

        if info.available_parameters_ids is not None:
            for parameters_id in info.available_parameters_ids.keys():
                f_1 = create(
                    builtin_name,
                    input_dim,
                    parameters_id=parameters_id,
                )
                f_2 = getattr(uqtf, builtin_name)(
                    input_dim,
                    parameters_id=parameters_id,
                )

                assert_equal(f_1, f_2)
        else:
            pytest.skip(f"No parameters IDs available for {builtin_name}")

    def test_invalid_dim_neg(self, builtin_name: str, info: UQTestFunInfo):
        """Test creating a UQ test function with negative dimension."""
        with pytest.raises(ValueError):
            _ = create(builtin_name, input_dimension=-1)

        with pytest.raises(ValueError):
            _ = getattr(uqtf, builtin_name)(input_dimension=-1)

    def test_invalid_var_dim(self, builtin_name: str, info: UQTestFunInfo):
        """Test creating a UQ test function with an invalid var dimension."""

        if info.input_dimension is not None:
            pytest.skip(f"{builtin_name} is not variable dimension")
        else:
            with pytest.raises(ValueError):
                _ = create(builtin_name)

            with pytest.raises(ValueError):
                _ = getattr(uqtf, builtin_name)()

    def test_invalid_fixed_dim(self, builtin_name: str, info: UQTestFunInfo):
        """Test creating a UQ test function with invalid fixed dimension."""

        if info.input_dimension is None:
            pytest.skip(f"{builtin_name} is not fixed dimension")
        else:
            fixed_dim = info.input_dimension + 1
            with pytest.raises(ValueError):
                _ = create(builtin_name, input_dimension=fixed_dim)

            with pytest.raises(ValueError):
                _ = getattr(uqtf, builtin_name)(input_dimension=fixed_dim)

    def test_invalid_input_id(self, builtin_name: str, info: UQTestFunInfo):
        """Test creating a UQ test function with invalid input ID."""
        if info.input_dimension is None:
            input_dim = 5
        else:
            input_dim = info.input_dimension

        random_id = random_string(5)
        with pytest.raises(ValueError):
            _ = create(builtin_name, input_dim, input_id=random_id)
        with pytest.raises(ValueError):
            _ = getattr(uqtf, builtin_name)(input_dim, input_id=random_id)

    def test_invalid_params_id(self, builtin_name: str, info: UQTestFunInfo):
        """Test creating a UQ test function with invalid parameters ID."""

        if info.input_dimension is None:
            input_dim = 5
        else:
            input_dim = info.input_dimension

        if not info.available_parameters_ids:
            pytest.skip(f"{builtin_name} is not parameterized")

        random_id = random_string(5)
        with pytest.raises(ValueError):
            _ = create(builtin_name, input_dim, parameters_id=random_id)
        with pytest.raises(ValueError):
            _ = getattr(uqtf, builtin_name)(input_dim, parameters_id=random_id)

    def test_set_parameter(self, builtin_name: str, info: UQTestFunInfo):
        """Test setting a value of a parameter raises an exception."""
        if info.default_parameters_id is None:
            pytest.skip(f"{builtin_name} does not support parameterization")

        if info.input_dimension is None:
            input_dim = 5
        else:
            input_dim = info.input_dimension

        # Create an instance
        f = create(builtin_name, input_dim)

        # Assertion
        assert f.parameters is not None
        assert isinstance(f.parameters, Parameters)
        key = next(iter(f.parameters.keys()))
        with pytest.raises(ParametersProtectedError):
            f.parameters[key] = 1.0


class TestCall:

    def test_call(self, builtin_name: str, info: UQTestFunInfo):
        """Test calling an instance of built-in UQ test function."""

        # Create instances of UQ test function
        if info.variable_dimension:
            input_dimension = 5
            f_1 = create(builtin_name, input_dimension=input_dimension)
            f_2 = getattr(uqtf, builtin_name)(input_dimension=input_dimension)
        else:
            f_1 = create(builtin_name)
            f_2 = getattr(uqtf, builtin_name)()

        # Generate and evaluate sample points
        sample_size = 100
        rng_seed = 42
        xx_1 = f_1.prob_input.get_sample(sample_size, rng_seed)
        xx_2 = f_2.prob_input.get_sample(sample_size, rng_seed)
        yy_1 = f_1(xx_1)
        yy_2 = f_2(xx_2)

        # Assertions
        assert xx_1.shape == (sample_size, f_1.input_dimension)
        assert xx_2.shape == (sample_size, f_2.input_dimension)
        assert len(yy_1) == sample_size
        assert len(yy_2) == sample_size
        assert np.array_equal(xx_1, xx_2)
        assert np.array_equal(yy_1, yy_2)

    def test_get_sample(self, builtin_name: str, info: UQTestFunInfo):
        """Test getting sample from built-in UQ test function instances."""

        # Create instances of UQ test function
        if info.variable_dimension:
            input_dimension = 5
            f_1 = create(builtin_name, input_dimension=input_dimension)
            f_2 = getattr(uqtf, builtin_name)(input_dimension=input_dimension)
        else:
            f_1 = create(builtin_name)
            f_2 = getattr(uqtf, builtin_name)()

        # Generate sample with the same random seed
        sample_size = 100
        rng_seed = 42
        yy_1 = f_1.get_sample(sample_size, rng_seed)
        yy_2 = f_2.get_sample(sample_size, rng_seed)

        # Assertion
        assert len(yy_1) == sample_size
        assert len(yy_2) == sample_size
        assert np.array_equal(yy_1, yy_2)


class TestStr:

    def test_str(self, builtin_name: str, info: UQTestFunInfo):
        """Test the __str__() method of a test function instance."""
        input_dim = info.input_dimension
        if input_dim is None:
            input_dim = 5
        f = create(builtin_name, input_dimension=input_dim)

        s = str(f)

        # Assertions
        name = f.name
        if name is not None:
            assert name in s
        assert str(input_dim) in s
        assert str(f.output_dimension) in s
        if f._parameters is None:
            assert "False" in s
        else:
            assert "True" in s

    def test_repr(self, builtin_name: str, info: UQTestFunInfo):
        """Test the __repr__() method of a test function instance."""
        input_dim = info.input_dimension
        if input_dim is None:
            input_dim = 5
        f = create(builtin_name, input_dimension=input_dim)

        r = repr(f)

        # Assertions
        assert "UQTestFun" in r
        name = f.name
        if name is not None:
            assert name in r
        assert str(input_dim) in r
        assert info.default_input_id in r
        default_parameters_id = info.default_parameters_id
        if default_parameters_id is not None:
            assert default_parameters_id in r


class TestProbInputObject:
    """Test using an instance of ProbInput for a test function construction."""

    def test_valid(self, builtin_name: str, info: UQTestFunInfo):
        """Test that the ProbInput object is valid for construction."""
        if info.input_dimension is None:
            input_dim = 5
        else:
            input_dim = info.input_dimension
        f_1 = create(builtin_name, input_dimension=input_dim)
        prob_input = copy.copy(f_1.prob_input)

        # Construct a new instance
        f_2 = create(builtin_name, prob_input=prob_input)

        # Generate function values
        sample_size = 100
        seed = 42
        yy_1 = f_1.get_sample(sample_size, seed)
        yy_2 = f_2.get_sample(sample_size, seed)

        # Assertion
        assert np.array_equal(yy_1, yy_2)

    def test_invalid_dim(self, builtin_name: str, info: UQTestFunInfo):
        """Test invalid dimension with ProbInput for construction."""
        if info.input_dimension is None:
            input_dim = 5
        else:
            input_dim = info.input_dimension
        f_1 = create(builtin_name, input_dimension=input_dim)
        prob_input = copy.copy(f_1.prob_input)

        # Assertion
        with pytest.raises(ValueError):
            _ = create(
                builtin_name,
                input_dimension=input_dim + 1,
                prob_input=prob_input,
            )

    def test_invalid_prob_input(self, builtin_name: str, info: UQTestFunInfo):
        """Test creating a UQ test function with invalid ProbInput."""
        if info.input_dimension is None:
            pytest.skip()
        else:
            input_dim = info.input_dimension

        # Create ProbInput with mismatched dimension
        marginals = []
        for _ in range(input_dim + 1):
            marginals.append(Marginal("uniform", [0, 1]))
        prob_input = ProbInput(marginals)

        # Assert
        with pytest.raises(ValueError):
            _ = create(
                builtin_name,
                input_dimension=input_dim,
                prob_input=prob_input,
            )

    def test_invalid_exclusive(self, builtin_name: str, info: UQTestFunInfo):
        """Test invalid exclusive arguments for construction."""
        if info.input_dimension is None:
            input_dim = 5
        else:
            input_dim = info.input_dimension

        f_1 = create(builtin_name, input_dimension=input_dim)
        prob_input = copy.copy(f_1.prob_input)

        # Assert
        with pytest.raises(ValueError):
            _ = create(
                builtin_name,
                input_dimension=input_dim,
                input_id=info.default_input_id,
                prob_input=prob_input,
            )


class TestParametersObject:
    """Test the Parameters class for a test function construction."""

    def test_invalid_exclusive(self, builtin_name: str, info: UQTestFunInfo):
        """Test invalid exclusive parameters arguments for construction."""

        if info.input_dimension is None:
            input_dim = 5
        else:
            input_dim = info.input_dimension

        if info.default_parameters_id is None:
            pytest.skip(
                "Non-parameterized functions do not support parameters"
            )

        f_1 = create(builtin_name, input_dim)
        parameters = copy.copy(f_1.parameters)

        # Construct a new instance
        f_2 = create(builtin_name, input_dim, parameters=parameters)

        # Generate function values
        sample_size = 100
        seed = 42
        yy_1 = f_1.get_sample(sample_size, seed)
        yy_2 = f_2.get_sample(sample_size, seed)

        # Assertion
        assert np.array_equal(yy_1, yy_2)

    def test_no_parameters(self, builtin_name: str, info: UQTestFunInfo):
        """Test passing parameters for non-parameterized functions."""
        if info.input_dimension is None:
            input_dim = 5
        else:
            input_dim = info.input_dimension

        if info.default_parameters_id is not None:
            pytest.skip(
                "Non-parameterized functions do not support parameters"
            )

        # Create a dummpy Parameters
        params = Parameters({})

        with pytest.raises(ValueError):
            _ = create(builtin_name, input_dim, parameters=params)

        with pytest.raises(ValueError):
            _ = create(builtin_name, input_dim, parameters_id="123")

    def test_valid(self, builtin_name: str, info: UQTestFunInfo):
        """Test invalid exclusive parameters arguments for construction."""

        if info.input_dimension is None:
            input_dim = 5
        else:
            input_dim = info.input_dimension

        if info.default_parameters_id is None:
            pytest.skip()

        f = create(builtin_name, input_dimension=input_dim)
        parameters = copy.copy(f.parameters)

        # Assert
        with pytest.raises(ValueError):
            _ = create(
                builtin_name,
                input_dimension=input_dim,
                parameters_id=info.default_parameters_id,
                parameters=parameters,
            )
