"""Tests for instantiation of UQTestFun from YAML fixture specifications.

This module tests the full pipeline from YAML parsing through component
resolution to UQTestFun construction and evaluation. It uses purpose-built
fixture functions rather than the real registered collection, so structural
cases (e.g. field output) can be added without depending on real functions
that may not yet exist.
"""

import numpy as np
import pytest
import yaml

from uqtestfuns.core.uqtestfun import UQTestFun
from uqtestfuns.core.registry.parser import parse_spec
from uqtestfuns.core.registry.resolver import (
    resolve_evaluate,
    resolve_output_shape,
    resolve_parameters,
    resolve_prob_input,
)

from test_registry_parser import FIXTURE_ROOT, VALID_ROOT, VALID_SPEC_FILES


@pytest.fixture
def tmp_module_path(monkeypatch):
    monkeypatch.syspath_prepend(str(FIXTURE_ROOT))


@pytest.fixture(params=VALID_SPEC_FILES)
def uqtestfun_from_spec(request, tmp_module_path):
    """Construct a UQTestFun from a fixture YAML spec."""
    spec_file = VALID_ROOT / request.param

    with open(spec_file) as f:
        raw_data = yaml.safe_load(f)

    spec = parse_spec(spec_file, VALID_ROOT)

    input_dimension = raw_data["dimensions"]["input"]
    if input_dimension == "variable":
        input_dimension = 5

    # Resolve prob_input from the default input variant
    input_spec = spec.inputs.by_id[spec.inputs.default_id]
    prob_input = resolve_prob_input(input_spec, input_dimension)

    # Resolve parameters from the default variant (if any)
    parameters = None
    if spec.parameters is not None:
        parameters_spec = spec.parameters.by_id[spec.parameters.default_id]
        parameters = resolve_parameters(parameters_spec, input_dimension)

    evaluate = resolve_evaluate(spec.evaluate, parameters)
    output_shape = resolve_output_shape(spec.output_shape)

    instance = UQTestFun(
        evaluate=evaluate,
        prob_input=prob_input,
        parameters=parameters,
        output_shape=output_shape,
    )

    return instance, raw_data


def test_instantiation(uqtestfun_from_spec):
    """Test that a UQTestFun instance is successfully constructed from spec."""
    instance, _ = uqtestfun_from_spec
    assert isinstance(instance, UQTestFun)


def test_input_dimension(uqtestfun_from_spec):
    """Test that input_dimension matches the YAML specification."""
    instance, raw_data = uqtestfun_from_spec
    expected = raw_data["dimensions"]["input"]
    if expected == "variable":
        expected = 5
    assert instance.input_dimension == expected


def test_output_shape(uqtestfun_from_spec):
    """Test that output_shape matches the normalized YAML specification."""
    instance, raw_data = uqtestfun_from_spec

    raw_output = raw_data.get("dimensions", {}).get("output", 1)
    if isinstance(raw_output, list):
        expected = tuple(raw_output)
    elif raw_output == 1:
        expected = ()
    else:
        # Not statically known, the function must be evaluated
        yy = instance.get_sample(10)
        expected = yy[0].shape

    # Assertion
    assert instance.output_shape == expected


def test_output_dimension(uqtestfun_from_spec):
    """Test that output_dimension matches the product of the output shape."""
    instance, raw_data = uqtestfun_from_spec

    raw_output = raw_data.get("dimensions", {}).get("output", 1)
    if isinstance(raw_output, list):
        expected = 1
        for s in raw_output:
            expected *= s
    elif isinstance(raw_output, str):
        # Not statically known, the function must be evaluated
        yy = instance.get_sample(10)
        expected = np.prod(yy[0].shape)
    else:
        expected = raw_output

    # Assertion
    assert instance.output_dimension == expected


def test_call(uqtestfun_from_spec):
    """Test that calling the instance returns an array of the correct shape."""
    instance, _ = uqtestfun_from_spec
    sample_size = 10
    xx = instance.prob_input.get_sample(sample_size)
    yy = instance(xx)
    assert yy.shape == (sample_size,) + instance.output_shape


def test_parameters(uqtestfun_from_spec):
    """Test that parameters are set when declared in the YAML."""
    instance, raw_data = uqtestfun_from_spec
    if "parameters" in raw_data:
        assert instance.parameters is not None
    else:
        assert instance.parameters is None
