"""
Test module for the Ishigami test function.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""
import pytest

import uqtestfuns


def test_wrong_param_selection():
    """Test a wrong selection of the parameters; wing weight has none of it."""
    with pytest.raises(ValueError):
        uqtestfuns.create_from_default(
            "wing-weight",
            param_selection="marrei1",
        )
