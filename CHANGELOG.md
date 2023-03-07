# Changelog

All notable changes to the UQTestFuns project is documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2023-07-03

### Fixed

- v0.1.0 was erroneously already registered at PyPI;
  latest version of UQTestFuns that was planned for v0.1.0 is now v0.1.1
- Missing link in CHANGELOG.md

## [0.1.0] - 2023-07-03

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

## [0.0.1] - 2023-06-03

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

[0.1.0]: https://github.com/damar-wicaksono/uqtestfuns/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/damar-wicaksono/uqtestfuns/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/damar-wicaksono/uqtestfuns/releases/tag/v0.0.1
