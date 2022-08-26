import numpy as np

from uqtestfuns import WingWeight
from uqtestfuns.test_functions import wing_weight
from conftest import assert_call

def test_create_instance():
    """Test the creation of the default instance of the Wing Weight function."""
    my_wing_weight = WingWeight()

    # Assertions
    assert my_wing_weight.spatial_dimension == \
           wing_weight.DEFAULT_INPUT.spatial_dimension
    assert my_wing_weight.input == wing_weight.DEFAULT_INPUT


def test_call_instance():
    """Test calling an instance of the test function."""
    my_wing_weight = WingWeight()

    xx = np.random.rand(10, my_wing_weight.spatial_dimension)

    # Assertions
    assert_call(my_wing_weight, xx)
    assert_call(my_wing_weight.evaluate, xx)


def test_transform_input():
    """Test transforming an input."""
    my_wing_weight = WingWeight()

    # Transformation from the default uniform domain to the input domain.
    np.random.seed(315)
    xx_1 = -1 + 2 * np.random.rand(100, my_wing_weight.spatial_dimension)
    xx_1 = my_wing_weight.transform_inputs(xx_1)

    # Directly sample from the input property.
    np.random.seed(315)
    xx_2 = my_wing_weight.input.get_sample(100)

    # Assertion: two sampled values are equal
    assert np.allclose(xx_1, xx_2)


def test_transform_input_non_default():
    """Test transforming an input from non-default domain."""
    my_wing_weight = WingWeight()

    # Transformation from non-default uniform domain to the input domain.
    np.random.seed(315)
    xx_1 = np.random.rand(100, my_wing_weight.spatial_dimension)
    xx_1 = my_wing_weight.transform_inputs(xx_1, min_value=0.0, max_value=1.0)

    # Directly sample from the input property.
    np.random.seed(315)
    xx_2 = my_wing_weight.input.get_sample(100)

    # Assertion: two sampled values are equal.
    assert np.allclose(xx_1, xx_2)

# TODO: Test the correctness of results