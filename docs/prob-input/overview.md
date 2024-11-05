(prob-input:overview)=
# Probabilistic Input Modeling

Unique to uncertainty quantification (UQ) test functions is the representation
of the input variables as random variables.
This is because in a UQ problem, each of the relevant input variables is
considered _uncertain_ and they are modeled probabilistically.

In such a setting, each input variable is represented as a random variable
whose distribution is described (in the case of a continuous random variable)
by a probability density function (PDF).
Multiple input variables are represented as a multivariate random variable
whose distribution is described by a _joint_ PDF.
The random variables in such a multivariate random variable
may or may not be statistically independent.

```{margin}
For more flexible and powerful probabilistic input modeling capabilities,
please refer to a complete UQ framework such as [UQLab](https://www.uqlab.com) or
[ChaosPy](https://github.com/jonathf/chaospy).
```

UQTestFuns includes some basic probabilistic input modeling capabilities
that allows the built-in test functions to be specified
without extensive dependencies[^dependencies].
These capabilities, however, are not designed to be a flexible suite of tools 
to handle the representation of a wide range of distributions
for practical applications.
Density functions and dependency structures are only made available
when a specific UQ test function requires them.
The list of supported univariate distributions can be found {ref}`here <prob-input:available-marginal-distributions>`.

This section of the documentation explains in more detail how to specify
a probabilistic input in UQTestFuns.
In UQTestFuns, a probabilistic input consists of one or more input variables,
each of which is represented as a univariate random variable with a prescribed
distribution:

- To learn more about how to create a univariate random variable,
  check out the {ref}`Creating a One-Dimensional Marginal Distribution <prob-input:marginal-distribution>`
  page.
- To learn more about how to model one or more input variables probabilistically,
  check out the {ref}`Creating a Probabilistic Input Model <prob-input:probabilistic-input-model>`
  page.
- To get an overview on the basic concepts in probability relevant to UQTestFuns,
  check out the {ref}`prob-input:preliminaries` page.

[^dependencies]: that is, outside the common numerical Python environment (NumPy and SciPy).
In fact, the univariate distributions in UQTestFuns wrap around the ones from `scipy.stats`
with parametrization that is more consistent with the applied UQ literature.