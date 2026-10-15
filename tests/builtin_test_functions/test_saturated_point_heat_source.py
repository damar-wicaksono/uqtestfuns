"""
Test module for the SaturatedPointHeatSource model.

Notes
-----
- The tests defined in this module deal with the correctness of the evaluation.
"""

import numpy as np
import pytest

from conftest import assert_call

from uqtestfuns import SaturatedPointHeatSource
from uqtestfuns.test_functions.saturated_point_heat_source import (
    evaluate as _evaluate,
)


def _make_fun(**overrides):
    """Return an instance with parameters copied and optionally overridden."""
    fun = SaturatedPointHeatSource(
        parameters=SaturatedPointHeatSource().parameters.copy()
    )
    for key, val in overrides.items():
        fun.parameters[key] = val
    return fun


# --- Grid validation


@pytest.mark.parametrize(
    "rr_bad",
    [
        [0.0, 5.0],  # zero radius
        [-1.0, 5.0],  # negative radius
        [[2.0, 5.0]],  # 2-D array
    ],
)
def test_invalid_rr_raises(rr_bad):
    """Invalid rr grids are rejected with ValueError."""
    fun = _make_fun(rr=rr_bad)
    xx = fun.prob_input.get_sample(2)
    with pytest.raises(ValueError):
        fun(xx)


@pytest.mark.parametrize(
    "tt_bad",
    [
        [-1.0, 86400.0],  # negative time
        [[-1.0, 86400.0]],  # 2-D array
    ],
)
def test_invalid_tt_raises(tt_bad):
    """Invalid tt grids are rejected with ValueError."""
    fun = _make_fun(tt=tt_bad)
    xx = fun.prob_input.get_sample(2)
    with pytest.raises(ValueError):
        fun(xx)


def test_zero_time_in_grid_accepted():
    """tt=0 is a valid entry and must not raise."""
    fun = _make_fun(tt=[0.0, 86400.0])
    xx = fun.prob_input.get_sample(2)

    # Assertion
    assert_call(fun, xx)


# --- Output shape


def test_output_shape_default():
    """Test that the default grid produces shape (N, 3, N_r, N_t)."""
    fun = SaturatedPointHeatSource()
    N = 5
    xx = fun.prob_input.get_sample(N, 42)
    yy = fun(xx)
    N_r = len(fun.parameters["rr"])
    N_t = len(fun.parameters["tt"])
    expected_shape = (N, 3, N_r, N_t)

    # Assertions
    assert fun.output_shape == expected_shape[1:]
    assert yy.shape == expected_shape


def test_output_shape_unequal_grids():
    """Testt that unequal N_r and N_t produce the correct 4-D shape."""
    rr = [2.0, 5.0, 10.0]
    tt = [86400.0, 31536000.0]
    fun = _make_fun(rr=rr, tt=tt)
    N = 4
    xx = fun.prob_input.get_sample(N, 42)
    yy = fun(xx)
    expected_shape = (N, 3, len(rr), len(tt))

    # Assertions
    assert fun.output_shape == expected_shape[1:]
    assert yy.shape == (N, 3, len(rr), len(tt))


# --- Zero-time initial conditions


def test_all_fields_zero_at_t0():
    """All three output fields are zero at t=0 (no diffusion has occurred)."""
    fun = _make_fun(rr=[2.0, 10.0], tt=[0.0, 86400.0])
    xx = fun.prob_input.get_sample(5, 42)
    yy = fun(xx)

    # Assertion
    np.testing.assert_array_equal(yy[:, :, :, 0], 0.0)


# --- Physics checks


def test_temperature_independent_of_mechanical_params():
    """ΔT depends only on K, C, rho and must not change with the others."""
    fun = _make_fun(rr=[5.0, 15.0], tt=[86400.0, 31536000.0])
    kwargs = dict(
        Q=fun.parameters["Q"],
        a_w=fun.parameters["a_w"],
        mu_w=fun.parameters["mu_w"],
        rr=fun.parameters["rr"],
        tt=fun.parameters["tt"],
    )

    # Vary only the mechanical/hydraulic inputs; keep K, C, rho identical.
    # Values are chosen freely (not constrained to the prior domain) to make
    # the test a genuine mathematical property check.
    base = np.array(
        [[1.79, 978.0, 2480.0, 12.8e9, 50.0e-5, 5.6e-20, 0.30, 0.15]]
    )
    alt = np.array(
        [[1.79, 978.0, 2480.0, 25.0e9, 9.0e-5, 1.0e-18, 0.40, 0.20]]
    )

    yy_base = _evaluate(base, **kwargs)
    yy_alt = _evaluate(alt, **kwargs)

    # Assertion
    np.testing.assert_array_equal(yy_base[0, 0], yy_alt[0, 0])


# --- Singularity c = kappa


def test_no_nan_at_c_equals_kappa():
    """p and u_r are finite (no NaN) when c = kappa exactly (delta = 0)."""
    K, C, rho = 1.79, 978.0, 2480.0
    E, nu = 12.8e9, 0.3
    a_s, phi = 5.0e-5, 0.15
    a_w, mu_w = 4.0e-4, 1.0e-3

    kappa = K / (C * rho)
    lam = E * nu / ((1 + nu) * (1 - 2 * nu))
    G = E / (2 * (1 + nu))
    M = lam + 2 * G
    # k_s chosen so that c = k_s / mu_w * M = kappa exactly
    k_s_singular = kappa * mu_w / M

    xx = np.array([[K, C, rho, E, a_s, k_s_singular, nu, phi]])
    fun = _make_fun(
        a_w=a_w,
        mu_w=mu_w,
        rr=[5.0, 10.0],
        tt=[86400.0, 31536000.0],
    )
    yy = _evaluate(
        xx,
        fun.parameters["Q"],
        a_w,
        mu_w,
        fun.parameters["rr"],
        fun.parameters["tt"],
    )

    # Assertion
    assert not np.any(np.isnan(yy))
