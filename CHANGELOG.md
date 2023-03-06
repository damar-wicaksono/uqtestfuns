# Changelog

All notable changes to the UQTestFuns project is documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.0.1]: https://github.com/damar-wicaksono/uqtestfuns/releases/tag/v0.0.1
