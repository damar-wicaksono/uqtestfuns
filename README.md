<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/damar-wicaksono/uqtestfuns/main/docs/_static/logo-dark-tagline.png">
    <img src="https://raw.githubusercontent.com/damar-wicaksono/uqtestfuns/main/docs/_static/logo-light-tagline.png" alt="UQTestFuns" width="550">
  </picture>
</div>

---

[![JOSS](https://img.shields.io/badge/JOSS-10.21105/joss.05671-brightgreen?style=flat-square)](https://doi.org/10.21105/joss.05671)
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.7701903-blue.svg?style=flat-square)](https://doi.org/10.5281/zenodo.7701903)
[![Hatch](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pypa/hatch/master/docs/assets/badge/v0.json)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python](https://img.shields.io/pypi/pyversions/uqtestfuns?style=flat-square)](https://pypi.org/project/uqtestfuns/)
[![License](https://img.shields.io/github/license/damar-wicaksono/uqtestfuns?style=flat-square)](https://choosealicense.com/licenses/mit/)
[![PyPI](https://img.shields.io/pypi/v/uqtestfuns?style=flat-square)](https://pypi.org/project/uqtestfuns/)

|                                  Branches                                  | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|:--------------------------------------------------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`main`](https://github.com/damar-wicaksono/uqtestfuns/tree/main) (stable) | ![build](https://img.shields.io/github/actions/workflow/status/damar-wicaksono/uqtestfuns/main.yml?branch=main&style=flat-square) [![codecov](https://img.shields.io/codecov/c/github/damar-wicaksono/uqtestfuns/main?logo=CodeCov&style=flat-square&token=Y6YQEPJ1TT)](https://app.codecov.io/gh/damar-wicaksono/uqtestfuns/tree/main) [![Docs](https://readthedocs.org/projects/uqtestfuns/badge/?version=stable&style=flat-square)](https://uqtestfuns.readthedocs.io/en/stable/?badge=stable) |
|  [`dev`](https://github.com/damar-wicaksono/uqtestfuns/tree/dev) (latest)  | ![build](https://img.shields.io/github/actions/workflow/status/damar-wicaksono/uqtestfuns/main.yml?branch=dev&style=flat-square) [![codecov](https://img.shields.io/codecov/c/github/damar-wicaksono/uqtestfuns/dev?logo=CodeCov&style=flat-square&token=Y6YQEPJ1TT)](https://app.codecov.io/gh/damar-wicaksono/uqtestfuns/tree/dev) [![Docs](https://readthedocs.org/projects/uqtestfuns/badge/?version=latest&style=flat-square)](https://uqtestfuns.readthedocs.io/en/latest/?badge=latest)    |

UQTestFuns is an open-source Python library of test functions commonly used
within the applied uncertainty quantification (UQ) community.
Specifically, the package provides:

- an implementation _with minimal dependencies_ (i.e., NumPy, SciPy,
  PyYAML, and tabulate) and
  _a common interface_ of many test functions available in the UQ literature
- a _single entry point_ collecting test functions _and_ their probabilistic
  input specifications in a single Python package
- an _opportunity for an open-source contribution_, supporting
  the implementation of new test functions or posting reference results.

In short, UQTestFuns is an homage
to the [Virtual Library of Simulation Experiments (VLSE)](https://www.sfu.ca/~ssurjano/).

## Usage

UQTestFuns includes several commonly used test functions in the UQ community.
To list the available functions:

```python-repl
>>> import uqtestfuns as uqtf
>>> uqtf.list_functions()
+-------+-----------------------+-----------+---------------+--------------------------------+
|  No.  | Constructor           |  # Input  | Application   | Description                    |
+=======+=======================+===========+===============+================================+
|   1   | Ackley()              |     M     | optimization, | Optimization test function     |
|       |                       |           | metamodeling  | from Ackley (1987)             |
+-------+-----------------------+-----------+---------------+--------------------------------+
|   2   | Alemazkoor20D()       |    20     | metamodeling  | High-dimensional high-degree   |
|       |                       |           |               | polynomial from Alemazkoor and |
|       |                       |           |               | Meidani (2018)                 |
+-------+-----------------------+-----------+---------------+--------------------------------+
|   3   | Alemazkoor2D()        |     2     | metamodeling  | Two-dimensional high-degree    |
|       |                       |           |               | polynomial from Alemazkoor and |
|       |                       |           |               | Meidani (2018)                 |
+-------+-----------------------+-----------+---------------+--------------------------------+
|   4   | Borehole()            |     8     | metamodeling, | Eight-dimensional water flow   |
|       |                       |           | sensitivity   | model through a borehole from  |
|       |                       |           |               | Harper and Gupta (1983)        |
+-------+-----------------------+-----------+---------------+--------------------------------+
...
```

Consider the Borehole function, a test function commonly used for metamodeling
and sensitivity analysis purposes; to create an instance of this test function:

```python-repl
>>> my_testfun = uqtf.Borehole()
>>> print(my_testfun)
Name          : Borehole
Description   : Eight-dimensional water flow model through a borehole from Harper and Gupta (1983)
Input dim.    : 8
Output dim.   : 1
Parameterized : False
```

The probabilistic input specification of this test function is built-in:

```python-repl
>>> print(my_testfun.prob_input)
Name      : Harper1983
Dimension : 8
Marginals :

 No.    Variable   Distribution                      Description
-----  ----------  --------------------------------  -----------------------------------------------
  1        rw      Normal(mu=0.1, sigma=0.0161812)   Radius of the borehole [m]
  2        r       LogNormal(mu=7.71, sigma=1.0056)  Radius of influence [m]
  3        Tu      Uniform(a=63070, b=115600)        Transmissivity of upper aquifer [m^2/year]
  4        Hu      Uniform(a=990, b=1100)            Potentiometric head of upper aquifer [m]
  5        Tl      Uniform(a=63.1, b=116)            Transmissivity of lower aquifer [m^2/year]
  6        Hl      Uniform(a=700, b=820)             Potentiometric head of lower aquifer [m]
  7        L       Uniform(a=1120, b=1680)           Length of the borehole [m]
  8        Kw      Uniform(a=9985, b=12045)          Hydraulic conductivity of the borehole [m/year]

Copulas   : Independence
```

A sample of input values can be generated from the input model:

```python-repl
>>> xx = my_testfun.prob_input.get_sample(3)
>>> xx
array([[1.14767352e-01, 2.03186041e+03, 7.22520341e+04, 1.08721577e+03,
        6.72807052e+01, 7.32078512e+02, 1.25201069e+03, 1.19356620e+04],
       [1.10369118e-01, 1.67792766e+03, 8.95368986e+04, 1.00066209e+03,
        6.98963053e+01, 8.12938360e+02, 1.39096239e+03, 1.06572602e+04],
       [9.35256001e-02, 5.87630961e+02, 9.42363505e+04, 1.00844966e+03,
        1.04179964e+02, 7.67443161e+02, 1.51149823e+03, 1.11376654e+04]])
```

...and used to evaluate the test function:

```python-repl
>>> yy = my_testfun(xx)
>>> yy
array([138.82622459,  54.69015322,  48.66889977])
```

## Installation

You can obtain UQTestFuns directly from PyPI using `pip`:

```bash
$ pip install uqtestfuns
```

Alternatively, you can also install the latest version from the source,
including changes not yet published to PyPI:

```bash
$ pip install git+https://github.com/damar-wicaksono/uqtestfuns.git
```

> **NOTE**: UQTestFuns is currently a work in progress;
> its interfaces are, therefore, subject to change.

It's a good idea to install the package in an isolated virtual environment.
See the [documentation](https://uqtestfuns.readthedocs.io/en/latest/getting-started/obtaining-and-installing.html)
for Python version requirements and more detailed instructions.

## Getting help

For a getting-started guide on UQTestFuns,
please refer to the [Documentation](https://uqtestfuns.readthedocs.io/en/latest/).
The documentation also includes details on each of the available test functions.

For any other questions related to the package,
post your questions on the [GitHub Issues page](https://github.com/damar-wicaksono/uqtestfuns/issues).

## Package development and contribution

UQTestFuns is under ongoing development;
any contribution to the code (for example, a new test function)
and the documentation (including new reference results) are welcomed!

Please consider the [Contribution Guidelines](CONTRIBUTING.md) first 
before making a pull request. 

## Citing UQTestFuns

If you use this package in your research, please cite both
the [paper](https://doi.org/10.21105/joss.05671) and
the [software archive](https://doi.org/10.5281/zenodo.7701903),
or use the citation metadata in [`CITATION.cff`](CITATION.cff).
The [documentation](https://uqtestfuns.readthedocs.io/en/latest/getting-started/citing.html)
provides a ready-to-use BibTeX entry for the paper, guidance on citing
the specific version you used, and instructions on citing individual
test functions.

## Credits and contributors

This work was partly funded
by the [Center for Advanced Systems Understanding (CASUS)](https://www.casus.science/)
which is financed by Germany's Federal Ministry of Education and Research (BMBF)
and by the Saxony Ministry for Science, Culture and Tourism (SMWK)
with tax funds on the basis of the budget approved
by the Saxony State Parliament.

UQTestFuns is currently maintained by:

- [Damar Wicaksono](mailto:d.wicaksono@hzdr.de) ([HZDR/CASUS](https://www.casus.science/))

The project was originally developed under the Mathematical Foundations of
Complex System Science Group led by Michael Hecht at CASUS.

Contributors:

- Daniel S. Katz: editorial contributions to the JOSS paper during review

See [AUTHORS.md](AUTHORS.md) for the full, up-to-date list.

## License

UQTestFuns is released under the [MIT License](LICENSE).
