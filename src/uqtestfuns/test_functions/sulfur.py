"""
Module with an implementation of the Sulfur model test function.

The Sulfur model from [1] is a nine-dimensional scalar-valued function
that analytically computes the direct radiative forcing by sulfate aerosols.
The test function was used in [2] for metamodeling and uncertainty propagation
purposes.
The probabilistic input specification used in [2] was originally based
from [3].

Due to the construction of the test function, the geometric mean and geometric
standard deviation of the response are analytically available given the input
specification (from [2], all are lognormals). Note that the geometric mean
and the geometric standard deviation of a lognormal distribution are
the exponentiated mu and sigma parameters (i.e., the mean and
standard deviation of the underlying normal distribution).

To complete the test function specification, two additional parameters are
taken from the literature: the solar constant [4] and the surface area
of the earth [5].

Notes
-----

- The equation of the Sulfur model in [2] (Eq. (12)) is erroneous.
  The solar constant term S0 should not be squared, otherwise the dimension
  will not agree. Moreover, the equation is missing factors of 365 in the
  denominator and 10^12 in the numerator. The parameter L
  (Sulfate lifetime in the atmosphere) is given in [days]
  while the parameter Q (Global input flux of anthropogenic sulfur is
  given in [TgS/year].
- The input specification of the model here is taken from [3] (Table 2).
  While they are similar, the parameters T and (1-Rs) in [3] are in the
  squared form (i.e., T^2 and (1-Rs)^2).

References
----------
1. R. J. Charlson, S. E. Schwartz, J. M. Hales, R. D. Cess, J. A. Coakley,
   J. E. Hansen, and D. J. Hofmann, “Climate forcing by anthropogenic
   aerosols,” Science, vol. 255, no. 5043, pp. 423–430, 1992.
   DOI: 10.1126/science.255.5043.423.
2. M. A. Tatang, W. Pan, R. G. Prinn, and G. J. McRae, “An efficient method
   for parametric uncertainty analysis of numerical geophysical models,”
   Journal of Geophysical Research, vol. 102, no. D18, pp. 21925–21932, 1997.
   DOI: 10.1029/97JD01654.
3. J. E. Penner, R. J. Charlson, S.E. Schwartz, J. M. Hales, N. S. Laulainen,
   L. Travis, R. Leifer, T. Novakov, J. Ogren, L. F. Radke, “Quantifying and
   Minimizing Uncertainty of Climate Forcing by Anthropogenic Aerosols,”
   Bulletin of the American Meteorological Society, vol. 75, no. 3,
   pp. 375–400, 1994.
   DOI: 10.1175/1520-0477(1994)075<0375:QAMUOC>2.0.CO;2.
4. G. Kopp and J. L. Lean, “A new, lower value of total solar irradiance:
   Evidence and climate significance,” Geophysical Research Letter, vol. 38,
   no. 1, 2011.
   DOI: 10.1029/2010GL045777.
5. M. Pidwirny, “Introduction to the Oceans,”
   Fundamentals of Physical Geography, 2nd Edition, 2006.
   Accessed: Jan. 25, 2023
   URL: http://www.physicalgeography.net/fundamentals/8o.html.
"""

import numpy as np

SOLAR_CONSTANT = 1361  # [W/m^2] from [4]
EARTH_AREA = 5.1e14  # [m^2] from [5]
DAYS_IN_YEAR = 365  # [days]


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Sulfur model test function on a set of input values.

    References
    ----------
    xx : np.ndarray
        An ``(N, 9)`` array of input values where ``N`` is the number of
        evaluation points.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the direct
        radiative forcing by sulfate aerosols.
    """
    # Source strength of anthropogenic Sulfur (initially given in Teragram)
    qq = xx[:, 0] * 1e12
    # Fraction of SO2 oxidized to SO4(2-) aerosol
    yy = xx[:, 1]
    # Average lifetime of atmospheric SO4(2-)
    ll = xx[:, 2]
    # Aerosol mass scattering efficiency
    psi_e = xx[:, 3]
    # Fraction of light scattered upward hemisphere
    beta = xx[:, 4]
    # Fractional increase in aerosol scattering eff. due hygroscopic growth
    ff_psi = xx[:, 5]
    # Square of atmospheric transmittance above aerosol layer
    tt_sq = xx[:, 6]
    # Fraction of earth not covered by cloud
    aa_c_complement = xx[:, 7]
    # Square of surface coalbedo
    co_rr_s_sq = xx[:, 8]

    # Sulfate burden (Eq. (5) in [1], notation from [2])
    # NOTE: Factor 3.0 due to conversion of mass from S to SO4(2-)
    # NOTE: Factor 1/365.0 due to average lifetime is given in [days]
    #       while qq is in [gS / year]
    sulfate_burden = 3.0 * qq * yy * ll / EARTH_AREA / DAYS_IN_YEAR

    # Loading of sulfate aerosol (Eq. (4) in [1], notation from [2])
    sulfate_loading = psi_e * ff_psi * sulfate_burden

    # Direct radiative forcing by sulfate aerosols
    factor_1 = SOLAR_CONSTANT * aa_c_complement * tt_sq * co_rr_s_sq * beta
    dd_f = -0.5 * factor_1 * sulfate_loading

    return dd_f
