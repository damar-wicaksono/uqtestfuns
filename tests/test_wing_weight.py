"""
Test module for the Ishigami test function.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""
import pytest

from uqtestfuns import WingWeight


def test_wrong_param_selection():
    """Test a wrong selection of the parameters; wing weight has none of it."""
    with pytest.raises(TypeError):
        WingWeight(parameters="marell1")
