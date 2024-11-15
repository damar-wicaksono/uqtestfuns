# Changelog

All notable changes to the UQTestFuns project is documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- A commentary on metamodeling within the UQ framework in the docs.
- A better overview of UQ framework in the docs.
- A new parameter set for the Sobol'-G function from Sun et al. (2022).
- The 6-dimensional undamped non-linear oscillator function for reliability
  analysis exercises.
- The M-dimension Sobol'-Levitan function from Sobol' and Levitan (1999) for
  sensitivity analysis exercises.
- The M-dimensional test function from Morris et al. (2006) for sensitivity
  analysis exercises.
- The modified Sobol'-G test function (i.e., Sobol'-G*) from Saltelli et al.
  (2010) for sensitivity analysis exercises.
- The two-dimensional test function from Cheng and Sandu (2010)
  for metamodeling exercises.
- The M-dimensional linear function from Saltelli et al. (2008) for sensitivity
  analysis.
- The two-dimensional non-polynomial test function for metamodeling from
  Lim et al. (2002).
- The two-dimensional polynomial test function for metamodeling from 
  Lim et al. (2002).
- The three-dimensional sensitivity test function from Moon (2010).
- Two new abstract base classes are added, namely `UQTestFunFixDimABC` and
  `UQTestFunVarDimABC` to deal with the construction of UQ test functions of
  fixed and variable dimensions, respectively. Both abstract classes are derived
  from `UQTestFunABC` such that the interfaces remain consistent. 
- `function_id` and `input_id` are now property of `ProbInput`.
- `output_dimension` is now property of `UQTestFunBareABC` and inherited to
  all concrete classes of UQ test functions.
- Printing a test function instance now shows whether the function is 
  parameterized or not.
- The information related to the parameterization of a function is now
  shown in the output of `list_functions()`
- New class `FunParams` to organize function parameters.
- The six-dimensional and ten-dimensional Friedman functions from
  Friedman et al. (1983) and Friedman (1991), respectively.
- The three-dimensional simple portfolio model from Saltelli et al. (2004).
- The 20-dimensional polynomial test function from Alemazkoor
  and Meidani (2018).
- The exponential distribution as a distribution of `UnivDist` instances.

### Changed

- "None" copula is now printed as "Independence"; this is a temporary solution
  as there is no independence copula object yet.
- Application tags are now displayed when an instance of test function is
  printed on the terminal.
- `list_functions()` is now printed in grid format and include information
  regarding the output dimension and the parameterization. Furthermore,
  filtering can be done based on the input dimension, output dimension,
  tag, and parameterization.
- The class `UnivDist` has been renamed to `Marginal`. The name more clearly
  refers to one-dimensional marginal distributions (of a univariate random
  variable), which form a `ProbInput`.
- The property `spatial_dimension` of `ProbInput` and `UQTestFunBareABC` is
  renamed to `input_dimension` for clarity (as opposed to `output_dimension`).
- The property `name` of UQ test function instances has been renamed to
  `function_id` that implies uniqueness although it is not strictly enforced.
- The parameter in the Gramacy 1D sine function is now removed. Noise can
  be added on the fly if needed.
- `evaluate()` abstract method is now must be implemented directly in the
  concrete UQ test function; `eval_()` in the `UQTestFunABC` has been removed.

## [0.4.1] - 2023-10-27

### Added

- The two-dimensional polynomial function of high-degree for metamodeling
  exercises from Alemazkoor and Meidani (2008).
- New tutorials (how the package may be used in a sensitivity analysis or
  reliability analysis exercises) have been added to the documentation
  following the review process in the submission of the package
  to the Journal of Open Source Software (JOSS).

### Changed

- The documentation landing page now includes explicit statement regarding 
  the purpose of the package.

### Fixed

- Several typos in the documentation have been fixed with an additional
  minor improvements overall.

## [0.4.0] - 2023-07-07

### Added

- The two-dimensional convex failure domain problem for reliability
  analysis exercises from Borri and Speranzini (1997).
- The two-dimensional Quadratic RS problem for reliability analysis
  exercises from Waarts (2000). This is a variant of the classic RS 
  problem with one quadratic term.
- The one-dimensional damped cosine function for metamodeling exercises
  from an example in Santner et al. (2018).
- The two-dimensional circular bar RS problem for reliability analysis
  exercises taken from an example in Verma et al. (2015).
- The two-dimensional polynomial function with random inputs
  from Webster et al. (1996) for metamodeling exercises.
- New instance method for `UnivDist` and `ProbInput` classes
  called `reset_rng()`. When called (optionally with a seed number), a new
  instance of NumPy default RNG will be created and attached to the instance.
- GitHub actions now include testing on Python v3.11 via Tox.

### Changed

- `rng_seed_prob_input` keyword parameter has been removed from the list
  of parameters to the constructor of all UQ test functions.
  The accepted way to reset an RNG with a seed is to use the instance
  method `reset_rng()` (optionally with a seed number)
  of the `ProbInput` instance attached.
- Some background information in the documentation has been changed
  to match the description in the JOSS paper draft.

### Fixed

- A mistake in one the parameter values of the Sobol'-G function
  has been fixed. 

## [0.3.0] - 2023-07-03

### Added

- The two-dimensional Gayton Hat function from Echard et al. (2013) used
  in the context of reliability analysis.
- The eight-dimensional damped oscillator reliability problem from
  Der Kiureghian and De Stefano (1990); the problem is based on the existing
  Damped Oscillator model in the code base.
- The two-dimensional hyper-sphere bound reliability problem
  from Li et al. (2018).
- The two-dimensional cantilever beam reliability problem from
  Rajashekhar and Ellington (1993).
- The two-dimensional four-branch function for reliability analysis
  from Katsuki and Frangopol (1994).
- The five-dimensional speed reducer shaft reliability problem
  from Du and Sudjianto (2004).
- The two-dimensional reliability problem of a circular pipe crack
  under a bending moment under Verma et al. (2015).
- New docs section on list of functions for reliability analysis including
  a brief description on the reliability analysis problem.

## [0.2.0] - 2023-06-26

### Added

- The two-dimensional Franke functions (1st, 2nd, 3rd, 4th, 5th, and 6th),
  relevant for metamodeling exercises, are added as UQ test functions.
- The two-dimensional McLain functions (S1, S2, S3, S4, and S5),
  relevant for metamodeling exercises, are added as UQ test functions.
- An implementation of the Welch et al. (1992) test function, a 20-dimensional
  function used in the context of metamodeling and sensitivity analysis.
- Four M-dimensional test functions from Bratley et al. (1992) useful for
  testing multi-dimensional numerical integrations as well as 
  global sensitivity analysis methods.
- Add a new parameterization to the Sobol'-G function taken from
  Bratley et al. (1992) and Saltelli and Sobol' (1995).
- An implementation of the one-dimensional function from Forrester et al.
  (2008). The function was used as a test function for optimization approaches
  using metamodels.
- An implementation of the Gramacy (2007) one-dimensional sine function,
  a function with two regimes.
- Two base classes are now available `UQTestFunBareABC` and `UQTestFunABC`.
  The former is used to implement a _bare_ UQ test function
  (with only `evaluate()` and `ProbInput`), while the latter is used to
  implement _published_ UQ test functions in the code base (i.e., with 
  additional metadata such as tags and description).
- An instance of NumPy random number generator is now attached to instances of
  `UnivDist` and `ProbInput`. The random seed number may be passed 
  to the corresponding constructor for reproducibility.
- CITATION.cff file to the code base.

### Changed

- The date format in CHANGELOG.md has been changed from YYYY-DD-MM to the 
  ISO format YYYY-MM-DD.
- The bibliography style in the docs has been changed to 'unsrtalpha'
  (alphanumeric labels, sorted by order of appearance).
- When `list_functions()` is called with a `tag` argument,
  then the application tags are no longer displayed to save terminal spaces.
- The one-dimensional `OakleyOHagan1D` function has been renamed to
  `Oakley1D`.

### Fixed

- The original citation for the Sobol'-G function has been fixed;
  it is now referred to Saltelli and Sobol' (1995).
- If a function is used as parameters in a test function (e.g., if
  variable dimension), then it must have the keyword parameter
  "spatial_dimension" for the function to be called when an instance of
  a UQ test function is created. This is to allow an arbitrary function
  (without a parameter named "spatial_dimension") to be a parameter of
  UQ test function.
- One-dimensional test function now returns a one-dimensional array.

## [0.1.1] - 2023-03-07

### Fixed

- v0.1.0 was erroneously already registered at PyPI;
  latest version of UQTestFuns that was planned for v0.1.0 is now v0.1.1
- Missing link in CHANGELOG.md

## [0.1.0] - 2023-03-07

### Added

- Publishing to PyPI is now automated
  once a tagged (with semantic version) release is carried out via GitHub
- Add a few additional classifiers in `setup.cfg` for the PyPI record
- DOI from Zenodo in README.md

### Fixed

- Wrong classifier specification in `setup.cfg` causing upload to PyPI to fail
- Issue with RTD document built crashing from time to time;
  probably due to a problematic matplotlib version

### Changed

- The HTML representation of `ProbInput` instances now takes less space
- Relax the numerical tolerance of a test (i.e., univariate beta distribution)
- Minor edit in the docs

## [0.0.1] - 2023-03-06

First public release of UQTestFuns.

### Added

- An abstract class (`UQTestFunABC`) to unify the interface of a UQ test function
- Probabilistic input modeling (via `ProbInput` class) with a joint independent distribution function
- `UnivDist` class to represent one-dimensional marginal distributions (a univariate continuous random variable)
- Nine univariate distributions
- A total of 11 UQ test functions (concrete implementations of `UQTestFunABC`)
  typically used for the metamodeling, sensitivity analysis, and optimization applications
- A concrete class implementation (`UQTestFun`) to create a UQ test function on runtime
- A minimal documentation built using [Jupyter Book](https://jupyterbook.org)
- CI/CD to build and serve the documentation on [ReadTheDocs](https://readthedocs.org/)
- Mirror GitHub action to the [CASUS organization](https://github.com/casus)

[Unreleased]: https://github.com/damar-wicaksono/uqtestfuns/compare/main...dev
[0.4.1]: https://github.com/damar-wicaksono/uqtestfuns/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/damar-wicaksono/uqtestfuns/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/damar-wicaksono/uqtestfuns/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/damar-wicaksono/uqtestfuns/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/damar-wicaksono/uqtestfuns/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/damar-wicaksono/uqtestfuns/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/damar-wicaksono/uqtestfuns/releases/tag/v0.0.1
