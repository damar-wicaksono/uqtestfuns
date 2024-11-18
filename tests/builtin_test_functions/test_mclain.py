"""
Test module for the McLain test functions.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""

import numpy as np

from uqtestfuns.test_functions import (
    McLainS1,
    McLainS2,
    McLainS3,
    McLainS4,
    McLainS5,
)


def test_mclain_s1():
    """Test the McLain S1 function."""
    my_fun = McLainS1()

    yy_ref = 8.0
    xx = np.array([[5.5, 5.5]])

    # Assertion: The maximum is known
    assert np.isclose(yy_ref, my_fun(xx))

    xx_test = my_fun.prob_input.get_sample(100000)
    yy_test = my_fun(xx_test)

    # Assertion: The maximum is indeed a maximum
    assert np.all(yy_test <= yy_ref)


def test_mclain_s2():
    """Test the McLain S2 function."""
    my_fun = McLainS2()

    yy_ref = 1.0
    xx = np.array([[5.0, 5.0]])

    # Assertion: The maximum is known
    assert np.isclose(yy_ref, my_fun(xx))

    xx_test = my_fun.prob_input.get_sample(100000)
    yy_test = my_fun(xx_test)

    # Assertion: The maximum is indeed a maximum
    assert np.all(yy_test <= yy_ref)


def test_mclain_s3():
    """Test the McLain S3 function."""
    my_fun = McLainS3()

    yy_ref = 1.0
    xx = np.array([[5.0, 5.0]])

    # Assertion: The maximum is known
    assert np.isclose(yy_ref, my_fun(xx))

    xx_test = my_fun.prob_input.get_sample(100000)
    yy_test = my_fun(xx_test)

    # Assertion: The maximum is indeed a maximum
    assert np.all(yy_test <= yy_ref)


def test_mclain_s4():
    """Test the McLain S4 function."""
    my_fun = McLainS4()

    yy_ref = 1.0
    xx = np.array([[5.5, 5.5]])

    # Assertion: The maximum is known
    assert np.isclose(yy_ref, my_fun(xx))

    xx_test = my_fun.prob_input.get_sample(100000)
    yy_test = my_fun(xx_test)

    # Assertion: The maximum is indeed a maximum
    assert np.all(yy_test <= yy_ref)


def test_mclain_s5():
    """Test the McLain S5 function."""
    my_fun = McLainS5()

    yy_ref = -1.0
    xx = np.array([[1.0, 1.0]])

    # Assertion: The minimum is known
    assert np.isclose(yy_ref, my_fun(xx))

    yy_ref = 1.0
    xx = np.array([[10.0, 10.0]])

    # Assertion: The maximum is known
    assert np.isclose(yy_ref, my_fun(xx))

    xx_test = my_fun.prob_input.get_sample(100000)
    yy_test = my_fun(xx_test)

    # Assertion: The maximum is indeed a maximum
    assert np.all(yy_test <= yy_ref)
