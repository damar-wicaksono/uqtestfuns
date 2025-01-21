# UQTestFuns
[![JOSS](https://img.shields.io/badge/JOSS-10.21105/joss.05671-brightgreen?style=flat-square)](https://doi.org/10.21105/joss.05671)
[![DOI](http://img.shields.io/badge/DOI-10.5281/zenodo.14710452-blue.svg?style=flat-square)](https://doi.org/10.5281/zenodo.14710452)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg?style=flat-square)](https://www.python.org/downloads/release/python-370/)
[![License](https://img.shields.io/github/license/damar-wicaksono/uqtestfuns?style=flat-square)](https://choosealicense.com/licenses/mit/)
[![PyPI](https://img.shields.io/pypi/v/uqtestfuns?style=flat-square)](https://pypi.org/project/uqtestfuns/)

|                                  Branches                                  | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|:--------------------------------------------------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`main`](https://github.com/damar-wicaksono/uqtestfuns/tree/main) (stable) | ![build](https://img.shields.io/github/actions/workflow/status/damar-wicaksono/uqtestfuns/main.yml?branch=main&style=flat-square) [![codecov](https://img.shields.io/codecov/c/github/damar-wicaksono/uqtestfuns/main?logo=CodeCov&style=flat-square&token=Y6YQEPJ1TT)](https://app.codecov.io/gh/damar-wicaksono/uqtestfuns/tree/main) [![Docs](https://readthedocs.org/projects/uqtestfuns/badge/?version=stable&style=flat-square)](https://uqtestfuns.readthedocs.io/en/stable/?badge=stable) |
|  [`dev`](https://github.com/damar-wicaksono/uqtestfuns/tree/dev) (latest)  | ![build](https://img.shields.io/github/actions/workflow/status/damar-wicaksono/uqtestfuns/main.yml?branch=dev&style=flat-square) [![codecov](https://img.shields.io/codecov/c/github/damar-wicaksono/uqtestfuns/dev?logo=CodeCov&style=flat-square&token=Y6YQEPJ1TT)](https://app.codecov.io/gh/damar-wicaksono/uqtestfuns/tree/dev) [![Docs](https://readthedocs.org/projects/uqtestfuns/badge/?version=latest&style=flat-square)](https://uqtestfuns.readthedocs.io/en/latest/?badge=latest)    |

<!--One paragraph description-->
UQTestFuns is an open-source Python3 library of test functions commonly used
within the applied uncertainty quantification (UQ) community.
Specifically, the package provides:

- an implementation _with minimal dependencies_ (i.e., NumPy and SciPy) and
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
+-------+-------------------------------+-----------+------------+----------+---------------+--------------------------------+
|  No.  |          Constructor          |  # Input  |  # Output  |  Param.  |  Application  | Description                    |
+=======+===============================+===========+============+==========+===============+================================+
|   1   |           Ackley()            |     M     |     1      |   True   | optimization, | Optimization test function     |
|       |                               |           |            |          | metamodeling  | from Ackley (1987)             |
+-------+-------------------------------+-----------+------------+----------+---------------+--------------------------------+
|   2   |        Alemazkoor20D()        |    20     |     1      |  False   | metamodeling  | High-dimensional low-degree    |
|       |                               |           |            |          |               | polynomial from Alemazkoor &   |
|       |                               |           |            |          |               | Meidani (2018)                 |
+-------+-------------------------------+-----------+------------+----------+---------------+--------------------------------+
|   3   |        Alemazkoor2D()         |     2     |     1      |  False   | metamodeling  | Low-dimensional high-degree    |
|       |                               |           |            |          |               | polynomial from Alemazkoor &   |
|       |                               |           |            |          |               | Meidani (2018)                 |
+-------+-------------------------------+-----------+------------+----------+---------------+--------------------------------+
|   4   |          Borehole()           |     8     |     1      |  False   | metamodeling, | Borehole function from Harper  |
|       |                               |           |            |          |  sensitivity  | and Gupta (1983)               |
+-------+-------------------------------+-----------+------------+----------+---------------+--------------------------------+
...
```

Consider the Borehole function, a test function commonly used for metamodeling
and sensitivity analysis purposes; to create an instance of this test function:

```python-repl
>>> my_testfun = uqtf.Borehole()
>>> print(my_testfun)
Function ID      : Borehole
Input Dimension  : 8 (fixed)
Output Dimension : 1
Parameterized    : False
Description      : Borehole function from Harper and Gupta (1983)
Applications     : metamodeling, sensitivity
```

The probabilistic input specification of this test function is built-in:

```python-repl
>>> print(my_testfun.prob_input)
Function ID     : Borehole
Input ID        : Harper1983
Input Dimension : 8
Description     : Probabilistic input model of the Borehole model from
                  Harper and Gupta (1983)
Marginals       :

 No.    Name    Distribution        Parameters                          Description
-----  ------  --------------  ---------------------  -----------------------------------------------
  1      rw        normal      [0.1       0.0161812]            radius of the borehole [m]
  2      r       lognormal        [7.71   1.0056]                 radius of influence [m]
  3      Tu       uniform        [ 63070. 115600.]      transmissivity of upper aquifer [m^2/year]
  4      Hu       uniform          [ 990. 1100.]         potentiometric head of upper aquifer [m]
  5      Tl       uniform          [ 63.1 116. ]        transmissivity of lower aquifer [m^2/year]
  6      Hl       uniform           [700. 820.]          potentiometric head of lower aquifer [m]
  7      L        uniform          [1120. 1680.]                length of the borehole [m]
  8      Kw       uniform         [ 9985. 12045.]     hydraulic conductivity of the borehole [m/year]

Copulas         : Independence
```

A sample of input values can be generated from the input model:

```python-repl
>>> xx = my_testfun.prob_input.get_sample(10)
array([[8.40623544e-02, 2.43926544e+03, 8.12290909e+04, 1.06612711e+03,
        7.24216436e+01, 7.78916695e+02, 1.13125867e+03, 1.02170796e+04],
       [1.27235295e-01, 3.28026293e+03, 6.36463631e+04, 1.05132831e+03,
        6.81653728e+01, 8.17868370e+02, 1.16603931e+03, 1.09370944e+04],
       [8.72711602e-02, 7.22496512e+02, 9.18506063e+04, 1.06436843e+03,
        6.44306474e+01, 7.74700231e+02, 1.46266808e+03, 1.12531788e+04],
       [1.22301709e-01, 2.29922122e+02, 8.00390345e+04, 1.05290108e+03,
        1.10852262e+02, 7.94709283e+02, 1.28026313e+03, 1.01879077e+04],
...
```

...and used to evaluate the test function:

```python-repl
>>> yy = my_testfun(xx)
array([ 57.32635774, 110.12229548,  53.10585812,  96.15822154,
        58.51714875,  89.40068404,  52.61710076,  61.47419171,
        64.18005235,  79.00454634])
```

## Installation

You can obtain UQTestFuns directly from PyPI using `pip`:

```bash
$ pip install uqtestfuns
```

Alternatively, you can also install the latest version from the source:

```bash
pip install git+https://github.com/damar-wicaksono/uqtestfuns.git
```

> **NOTE**: UQTestFuns is currently work in progress,
> therefore interfaces are subject to change.

It's a good idea to install the package in an isolated virtual environment.

## Getting help

<!--Getting help-->
For a getting-started guide on UQTestFuns,
please refer to the [Documentation](https://uqtestfuns.readthedocs.io/en/latest/).
The documentation also includes details on each of the available test functions.

For any other questions related to the package,
post your questions on the GitHub Issue page.

## Package development and contribution

<!--Package Development-->
UQTestFuns is under ongoing development;
any contribution to the code (for example, a new test function)
and the documentation (including new reference results) are welcomed!

Please consider the [Contribution Guidelines](CONTRIBUTING.MD) first,
before making a pull request. 

## Citing UQTestFuns

If you use this package in your research or projects, please consider citing
both the associated paper and the Zenodo archive (for the specific version
used).

### Citing the paper (JOSS)

The citation of the paper associated with this package is:

```bibtex
@article{Wicaksono2023,
  author    = {Wicaksono, Damar and Hecht, Michael},
  title     = {{UQTestFuns}: A {Python3} library of uncertainty quantification ({UQ}) test functions},
  journal   = {Journal of Open Source Software},
  year      = {2023},
  volume    = {8},
  number    = {90},
  doi       = {10.21105/joss.05671},
}
```

### Citing a specific version (Zenodo)

To ensure reproducibility, cite the exact version of the package you used.
Each release is archived on Zenodo with a unique DOI; find and use the DOI
for the version you used at [Zenodo].

The citation for the current public version is:

```bibtex
@software{UQTestFuns_0_6_0,
  author       = {Wicaksono, Damar and Hecht, Michael},
  title        = {{UQTestFuns: A Python3 Library of Uncertainty Quantification (UQ) Test Functions}},
  month        = jan,
  year         = 2025,
  publisher    = {Zenodo},
  version      = {v0.6.0},
  doi          = {10.5281/zenodo.14710452},
  url          = {https://doi.org/10.5281/zenodo.14710452}
}
```

## Credits and contributors

<!--Credits and contributors-->
This work was partly funded
by the [Center for Advanced Systems Understanding (CASUS)](https://www.casus.science/)
which is financed by Germany's Federal Ministry of Education and Research (BMBF)
and by the Saxony Ministry for Science, Culture and Tourism (SMWK)
with tax funds on the basis of the budget approved
by the Saxony State Parliament.

UQTestFuns is currently maintained by:

- Damar Wicaksono ([HZDR/CASUS](https://www.casus.science/))

under the Mathematical Foundations of Complex System Science Group
led by Michael Hecht ([HZDR/CASUS](https://www.casus.science/)) at CASUS.

## License

<!--License-->
UQTestFuns is released under the [MIT License](LICENSE).

[Zenodo]: https://zenodo.org/search?q=parent.id%3A7701903&f=allversions%3Atrue&l=list&p=1&s=10&sort=version
