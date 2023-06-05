"""
Test module for the Franke test functions.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""
import numpy as np

from uqtestfuns.test_functions import Franke2, Franke4, Franke5


def test_franke2():
    """Test the (2nd) Franke function."""
    my_fun = Franke2()

    yy_ref = 0.0
    xx = np.array([[1.0, 0.0]])

    # Assertion: The minimum is known
    assert np.isclose(yy_ref, my_fun(xx))

    yy_ref = 2.0 / 9.0
    xx = np.array([[0.0, 1.0]])

    # Assertion: The maximum is known
    assert np.isclose(yy_ref, my_fun(xx))

    xx_test = my_fun.prob_input.get_sample(100000)
    yy_test = my_fun(xx_test)

    # Assertion: The maximum is indeed a maximum
    assert np.all(yy_test <= yy_ref)


def test_franke4():
    """Test the (4th) Franke function"""
    franke_fun = Franke4()

    yy_ref = 1.0 / 3.0
    xx = np.array([[0.5, 0.5]])

    # Assertion: The maximum is known
    assert np.isclose(yy_ref, franke_fun(xx))

    xx_test = franke_fun.prob_input.get_sample(100000)
    yy_test = franke_fun(xx_test)

    # Assertion: The maximum is indeed a maximum
    assert np.all(yy_test <= yy_ref)


def test_franke5():
    """Test the (5th) Franke function"""
    franke_fun = Franke5()

    yy_ref = 1.0 / 3.0
    xx = np.array([[0.5, 0.5]])

    # Assertion: The maximum is known
    assert np.isclose(yy_ref, franke_fun(xx))

    xx_test = franke_fun.prob_input.get_sample(100000)
    yy_test = franke_fun(xx_test)

    # Assertion: The maximum is indeed a maximum
    assert np.all(yy_test <= yy_ref)
