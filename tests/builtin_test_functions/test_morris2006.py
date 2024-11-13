"""
Test module for the Morris2006 test function.

Notes
-----
- The tests defined in this module deals with the correctness
  of the evaluation of this particular test function.
"""

import numpy as np

from uqtestfuns.test_functions import Morris2006


def test_p_larger_than_m():
    """Test if the parameter p is larger than the number of input dim."""
    # Create an instance
    fun = Morris2006(input_dimension=3)
    fun.parameters["p"] = 3

    # Generate sample
    num_sample = 1000000
    xx = fun.prob_input.get_sample(num_sample)

    yy_1 = fun(xx)

    # Replace the parameter value
    fun.parameters["p"] = 4
    yy_2 = fun(xx)

    assert np.array_equal(yy_1, yy_2)


def test_one_dimension():
    """Test for one-dimensional function.

    Notes
    -----
    - Normally Morris2006 function requires more than 1 input dimension,
      but safeguard is in place to allow the computation of one-dimensional
      Morris2006 function.
    """
    # Create an instance
    fun = Morris2006(input_dimension=1)

    # Generate sample
    num_sample = 1000000
    xx = fun.prob_input.get_sample(num_sample)

    yy = fun(xx)

    # The slope of the linear one-dimensional function is sqrt(12)
    assert np.allclose(yy / xx[:, 0], np.sqrt(12))

def test_inert_inputs():
    """Test whether the remaining inputs of Morris2006 are indeed inert."""
    # Construct two instances of test function
    # Default parameter set to 10 inputs as important, the rest are inert
    fun_1 = Morris2006(input_dimension=20)
    fun_2 = Morris2006(input_dimension=30)

    # Generate sample and compare both
    num_sample = 1000000
    xx_1 = fun_1.prob_input.get_sample(num_sample)
    xx_2 = fun_2.prob_input.get_sample(num_sample)

    yy_1 = fun_1(xx_1)
    yy_2 = fun_2(xx_2)

    # Assertions
    assert np.allclose(np.mean(yy_1), np.mean(yy_2), rtol=1e-2)
    assert np.allclose(np.var(yy_1), np.var(yy_2), rtol=1e-2)
