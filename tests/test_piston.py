"""
Test module for the Piston simulation test function.

Notes
-----
- The tests defined in this module deals with the correctness
  of the evaluation of this particular test function.
"""
import numpy as np

from uqtestfuns import create_from_default


def test_inert_inputs():
    """Test whether the inputs from 'Moon' specification are indeed inert."""
    otl_ben_ari = create_from_default("piston", input_selection="ben-ari")
    otl_moon = create_from_default("piston", input_selection="moon")

    # Generate sample and compare both
    num_sample = 1000000
    xx_otl_ben_ari = otl_ben_ari.input.get_sample(num_sample)
    xx_otl_moon = otl_moon.input.get_sample(num_sample)

    yy_otl_ben_ari = otl_ben_ari(xx_otl_ben_ari)
    yy_otl_moon = otl_moon(xx_otl_moon)

    # Assertions
    assert np.allclose(
        np.mean(yy_otl_moon), np.mean(yy_otl_ben_ari), rtol=1e-2
    )
    assert np.allclose(np.var(yy_otl_moon), np.var(yy_otl_ben_ari), rtol=1e-2)
