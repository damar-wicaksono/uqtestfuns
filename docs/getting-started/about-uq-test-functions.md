(getting-started:about-uq-test-functions)=
# About UQ Test Functions

If you're interested in some background information about the what and why of uncertainty quantification (UQ) test functions,
their role within UQ analysis methods development, and how to usually get them, read on.

## What are UQ test functions

Consider the following analytical function that computes
the maximum annual underflow of a river:

$$
\begin{align}
	\mathcal{M}(\boldsymbol{x}) & = z_v + h - h_d - c_b\\
	h & = \left[ \frac{q}{b k_s \left(\frac{z_m - z_v}{l} \right)^{0.5}} \right]^{0.6}
\end{align}
$$

where $\boldsymbol{x} = \{ q, k_s, z_v, z_m, h_d, c_b, l, b \}$ is the eight-dimensional vector of input variables. 
The output is given in $[\mathrm{m}]$.
A negative value indicates that an overflow (_flooding_) occurs.
This test function is known as the {ref}`flood model <test-functions:flood>` {cite}`Iooss2015`.

```{margin}
The inputs of a UQ test function is probabilistic, modeled as random variables
```

The input variables of the function are modeled probabilistically as eight independent random variables with univariate marginals specified
in the table below.

| No. | Name  |      Distribution       |        Parameters        |                   Description                   |
|:---:|:-----:|:-----------------------:|:------------------------:|:-----------------------------------------------:|
|  1  |  $q$  | Truncated Gumbel (max.) | $[1013, 558, 500, 3000]$ |   Maximum annual flow rate $[\mathrm{m^3/s}]$   |
|  2  | $k_s$ |    Truncated Normal     |  $[30, 8, 15, \infty]$   | Strickler coefficient $[\mathrm{m^{(1/3)}/s}]$  |
|  3  | $z_v$ |       Triangular        |      $[49, 51, 50]$      |      River downstream level $[\mathrm{m}]$      |
|  4  | $z_m$ |       Triangular        |      $[54, 56, 55]$      |       River upstream level $[\mathrm{m}]$       |
|  5  | $h_d$ |         Uniform         |         $[7, 9]$         |           Dyke height $[\mathrm{m}]$            |
|  6  | $c_b$ |       Triangular        |     $[55, 56, 55.5]$     |            Bank level $[\mathrm{m}]$            |
|  7  |  $l$  |       Triangular        |   $[4990, 5010, 5000]$   |   Length of the river stretch $[\mathrm{m}]$    |
|  8  |  $b$  |       Triangular        |    $[295, 305, 300]$     |           River width $[\mathrm{m}]$            |

```{margin}
In a calibration (inverse quantification) analysis, the task is to obtain
the probabilistic input (posterior) given a function, input prior,
and some observed data.
```

UQ test functions are unique in this way: _the input variables are modeled probabilistically  as a joint multivariate random variable_.
In most cases, the specification of the inputs (the distribution, parameters, and dependence structure) are given as part of the problem specification.

```{margin}
Some typical questions in UQ analyses
```

Given both the function and the input specification, in a typical UQ analysis, we would ask the following questions:

- _what is the mean and variance of the output_? (uncertainty propagation)
- _which input variables drive the uncertainty in the output_? (sensitivity analysis)
- _what is the probability that an overflow occurs_? (reliability analysis / rare event estimation) 

Granted, this model is an oversimplification of the real situation and most probably not used to make any real-world decision.
But as far as a test function goes, this function exhibits some challenging features for a UQ analysis method.
Specifically, the function:

- is multidimensional
- contains non-uniform random variables
- involves some interaction terms between the input variables

Before a new UQ method is applied to a real-world problem to answer similar questions as the above,
it might be a good idea to check if the method can perform well when applied to the well-known flood model.

## Why use UQ test functions

As illustrated above, applied uncertainty quantification in computational
science and engineering encompasses many activities,
including uncertainty propagation, sensitivity analysis, reliability analysis,
optimization, etc.
New methods for each of the UQ analyses are continuously being developed.
Although such a method is eventually aimed at solving
real-world problems&mdash;typically involved a complex expensive-to-evaluate computational model&mdash;,
during the development phase,
developers prefer to use the so-called _test functions_
for validation and benchmarking purposes because:

```{margin}
Many UQ test functions have analytical forms, but this is not in any way a requirement
```

- test functions are _fast to evaluate_, at least, _faster_ than the real ones
- there are _many of them available_ in the literature
  for various types of analyses
- while a UQ analysis usually takes the computational model of interest as a blackbox,
  the _test functions are known_
  (and for some, the results are also analytically known)
  such that developers can do proper diagnostics based on particular structures 
  of the function

Assuming that real models are expensive to evaluate,
the cost of analysis is typically measured in the number of function evaluations
to achieve the desired accuracy.

## Where to get UQ test functions

```{margin}
Online resources to get UQ test functions
```

Several online resources provide a wide range of test functions relevant
to the applied UQ community.
For example:

- The [Virtual Library of Simulation Experiments: Test Functions and Datasets](https://www.sfu.ca/~ssurjano/index.html)
  is the definitive repository for UQ test functions.
  The site provides about a hundred test functions for a wide range of applications,
  each test function is described in a dedicated page complemented with implementations in MATLAB and R.
- The [Benchmark proposals of GdR](https://www.gdr-mascotnum.fr/benchmarks.html)
  provide a series of documents that contain test function specifications,
  but no code implementation whatsoever.
- The [Benchmark page of UQWorld](https://uqworld.org/c/uq-with-uqlab/benchmarks)
  provides a selection of test functions in metamodeling, sensitivity analysis,
  and reliability analysis along with their implementation in MATLAB.
  Although the implementations themselves are of generic MATLAB,
  they are geared towards usage in [UQLab](https://uqlab.com)
  (a framework for UQ in MATLAB).

Common to all these online resources are the requirement to either:

- implement the test function oneself following the specification, or
- when available, download each of the test functions separately.

Both are neither time-efficient nor convenient.

```{margin}
Alternative sources of UQ test functions: test functions inside an analysis package
```

Alternatively, in a given programming language,
some UQ analysis packages are often shipped with a selection of test functions
either for illustration, validation, or benchmarking.
Some examples within the Python UQ community are
(the data below is as of 2023-02-28):

- [UncertainPy](https://github.com/simetenn/uncertainpy)
  includes 8 test functions (mainly in the context of neuroscience)
  for illustrating the package capabilities {cite}`Tennoee2018`.
- [PyApprox](https://github.com/sandialabs/pyapprox) includes 18 test functions,
  including some non-algebraic functions for benchmarking purposes {cite}`Jakeman2021`.
- [Surrogate Modeling Toolbox (SMT)](https://github.com/SMTorg/smt) includes
  11 analytical and engineering problems
  for [benchmarking purposes](https://smt.readthedocs.io/en/stable/_src_docs/problems.html)
  {cite}`Bouhlel2019`.
- [OpenTURNS](https://github.com/openturns/openturns) {cite}`Baudin2017` has
  its own separate benchmark package called 
  [OTBenchmark](https://github.com/mbaudin47/otbenchmark)
  that includes 37 test functions {cite}`Fekhari2021`.

Taken together, and still considering some overlaps,
all these open-source packages provide quite a lot of test functions
already implemented in Python.
The problem is that these functions are part of the respective package.
To get access to the test functions belonging to a package,
the whole analysis package must be installed.

Moreover, test functions from a given package may be implemented in such a way
that is tightly coupled with the package itself.
To use the test functions belonging to a package,
you may need to learn some basic usage and terminologies of the package. 

If you are developing a new UQ method and would like to test it against some test functions,
going through all of these packages just to get an implementation of (say, algebraic) function
sounds like a hassle.
You might end up implementing some selection of the test functions yourself
and eventually ship them together with your package,
just like the other packages.

## Why another package

```{margin}
_Do we need another package for that_?
```

It seems there is indeed a problem in obtaining UQ test functions implemented in Python.
But, a healthy dose of skepticism is, well, healthy;
so it's natural to ask _do we need another package for that_?
UQ test functions are supposed to be available _somewhere_, at the very least in the literature; 
their implementations are even already available in _some languages_.
So the question is indeed a valid one.

As exemplified in the list above,
some test functions are already implemented in Python
and delivered as part of a UQ analysis package.
One is even a dedicated benchmark package.

```{margin}
We think "yes"
```

And yet, we think none of them is satisfactory.
Specifically, none of them provides:

- _a lightweight implementation_ (with minimal dependencies)
  of many test functions available in the UQ literature;
  this means our package will be free of any implementations
  of any UQ analysis methods resulting in a minimal overhead
  in setting up the test functions,
- _a single entry point_ (combining models and input specification)
  to a wide range of test functions,
- an opportunity for an _open-source contribution_ where new test functions are
  added and new reference results are posted.

Satisfying all the above requirements is exactly the goal
of the UQTestFuns package.

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```
