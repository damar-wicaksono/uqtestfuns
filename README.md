![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/damar-wicaksono/uqtestfuns/Packaging/dev)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# UQTestFuns

<!--One paragrah description-->
UQTestFuns is an open-source Python3 library of test functions commonly used
within the uncertainty quantification (UQ) community.
The package aims to provide:

- a _lightweight implementation_ (with minimal dependencies) of
  many test functions available in the UQ literature
- a _single entry point_ (combining models and their probabilistic input
  specification) to a wide range of test functions
- an opportunity for an _open-source contribution_ where new test functions and
  reference results are posted.

In short, UQTestFuns is an homage
to the [Virtual Library of Simulation Experiments (VLSE)](https://www.sfu.ca/~ssurjano/).

## Usage

UQTestFuns includes several commonly used test functions in the UQ community.
To list the available functions:

```python
>>> import uqtestfuns as uqtf
>>> uqtf.list_functions()
 No.      Constructor       Spatial Dimension          Application          Description
-----  ------------------  -------------------  --------------------------  ----------------------------------------------------------------------------
  1         Ackley()                M           optimization, metamodeling  Ackley function from Ackley (1987)
  2        Borehole()               8           metamodeling, sensitivity   Borehole function from Harper and Gupta (1983)
  3    DampedOscillator()           8           metamodeling, sensitivity   Damped oscillator model from Igusa and Der Kiureghian (1985)
  4         Flood()                 8           metamodeling, sensitivity   Flood model from Iooss and Lemaître (2015)
  5        Ishigami()               3                  sensitivity          Ishigami function from Ishigami and Homma (1991)
...
```

Consider the Borehole function, a test function commonly used for metamodeling
and sensitivity analysis purposes; to create an instance of this test function:

```python
>>> my_testfun = uqtf.Borehole()
>>> print(my_testfun)
Name              : Borehole
Spatial dimension : 8
Description       : Borehole function from Harper and Gupta (1983)
```

The probabilistic input specification of this test function is built-in:

```python
>>> print(my_testfun.prob_input)
Name         : Borehole-Harper-1983
Spatial Dim. : 8
Description  : Probabilistic input model of the Borehole model from Harper and Gupta (1983).
Marginals    :

  No.   Name    Distribution        Parameters                          Description                  
                                                                                                     
-----  ------  --------------  ---------------------  -----------------------------------------------
    1    rw        normal      [0.1       0.0161812]            radius of the borehole [m]
    2    r       lognormal        [7.71   1.0056]                 radius of influence [m]
    3    Tu       uniform        [ 63070. 115600.]      transmissivity of upper aquifer [m^2/year]
    4    Hu       uniform          [ 990. 1100.]         potentiometric head of upper aquifer [m]
    5    Tl       uniform          [ 63.1 116. ]        transmissivity of lower aquifer [m^2/year]
    6    Hl       uniform           [700. 820.]          potentiometric head of lower aquifer [m]    
    7    L        uniform          [1120. 1680.]                length of the borehole [m]                                       
    8    Kw       uniform         [ 9985. 12045.]     hydraulic conductivity of the borehole [m/year]

    Copulas      : None
```

A sample of input values can be generated from the input model:

```python
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

```python
>>> yy = my_testfun(xx)
array([ 57.32635774, 110.12229548,  53.10585812,  96.15822154,
        58.51714875,  89.40068404,  52.61710076,  61.47419171,
        64.18005235,  79.00454634])
```

## Installation

<!--Installation-->
UQTestFuns is not yet available via PyPI; the source can be obtained from GitHub:

```bash
$ git clone https://github.com/damar-wicaksono/uqtestfuns
```

To install UQTestFuns from the source, type:

```bash
$ pip install [-e] 
```

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

## License

<!--License-->
UQTestFuns is released under the [MIT License](LICENSE).
