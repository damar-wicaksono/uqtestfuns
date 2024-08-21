"""
Test module for the Piston simulation test function.

Notes
-----
- The tests defined in this module deals with the correctness
  of the evaluation of this particular test function.
"""

import numpy as np

from uqtestfuns.test_functions import Piston


def test_inert_inputs():
    """Test whether the inputs from 'Moon' specification are indeed inert."""
    piston_ben_ari = Piston(prob_input_selection="BenAri2007")
    piston_moon = Piston(prob_input_selection="Moon2010")

    # Assert that the ProbInput is correctly attached
    assert piston_ben_ari.prob_input is not None
    assert piston_moon.prob_input is not None

    # Generate sample and compare both
    num_sample = 1000000
    xx_ben_ari = piston_ben_ari.prob_input.get_sample(num_sample)
    xx_moon = piston_moon.prob_input.get_sample(num_sample)

    yy_ben_ari = piston_ben_ari(xx_ben_ari)
    yy_moon = piston_moon(xx_moon)

    # Assertions
    assert np.allclose(np.mean(yy_moon), np.mean(yy_ben_ari), rtol=1e-2)
    assert np.allclose(np.var(yy_moon), np.var(yy_ben_ari), rtol=1e-2)
