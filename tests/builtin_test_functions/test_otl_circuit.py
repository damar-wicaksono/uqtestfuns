"""
Test module for the OTL circuit test function.

Notes
-----
- The tests defined in this module deals with the correctness
  of the evaluation of this particular test function.
"""

import numpy as np

from uqtestfuns.test_functions import OTLCircuit


def test_inert_inputs():
    """Test whether the inputs from 'Moon' specification are indeed inert."""
    otl_ben_ari = OTLCircuit(input_id="BenAri2007")
    otl_moon = OTLCircuit(input_id="Moon2010")

    # Assertions: ProbInput is assigned
    assert otl_ben_ari.prob_input is not None
    assert otl_moon.prob_input is not None

    # Generate sample and compare both
    num_sample = 1000000
    xx_otl_ben_ari = otl_ben_ari.prob_input.get_sample(num_sample)
    xx_otl_moon = otl_moon.prob_input.get_sample(num_sample)

    yy_otl_ben_ari = otl_ben_ari(xx_otl_ben_ari)
    yy_otl_moon = otl_moon(xx_otl_moon)

    # Assertions
    assert np.allclose(
        np.mean(yy_otl_moon), np.mean(yy_otl_ben_ari), rtol=1e-2
    )
    assert np.allclose(np.var(yy_otl_moon), np.var(yy_otl_ben_ari), rtol=1e-2)
