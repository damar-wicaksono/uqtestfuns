(prob-input:overview)=
# Probabilistic Input Modeling

Unique to uncertainty quantification (UQ) test functions is the representation
of the input variables as random variables.
This is because in a UQ problem, each of the relevant input variables is
considered _uncertain_ and modeled probabilistically. See
{ref}`Uncertainty Quantification Framework <fundamentals:overview>` for how
this fits into the broader UQ analysis workflow.

In such a setting, each input variable is represented as a random variable
whose distribution is described (in the case of a continuous random variable)
by a probability density function (PDF).
Multiple input variables are represented as a random vector
whose distribution is described by a _joint_ PDF.
The random variables in such a random vector
may or may not be statistically independent.

```{margin}
For more flexible and powerful probabilistic input modeling capabilities,
please refer to a complete UQ framework such as [UQLab](https://www.uqlab.com) or
[ChaosPy](https://github.com/jonathf/chaospy).
```

UQTestFuns includes some basic probabilistic input modeling capabilities
that allow the built-in test functions to be specified
without extensive dependencies[^dependencies].
These capabilities are not meant to be a flexible,
general-purpose toolkit for representing a wide range of distributions.
Density functions and (in the future) dependency structures are only made
available when a specific UQ test function requires them.
See the {ref}`list of supported univariate distributions <prob-input:available-marginal-distributions>`.

This section of the documentation explains in more detail how to specify
a probabilistic input in UQTestFuns.

In terms of the general probability concepts introduced in
{ref}`Probability Concepts and Notations <prob-input:concepts-and-notations>`,
UQTestFuns gives the random variable and the random vector distinct names
for their role as a UQ test function's input:

| General probability term |                      UQTestFuns term                      |
|:------------------------:|:---------------------------------------------------------:|
|     Random variable      | (One-dimensional) marginal distribution[^one-dimensional] |
|      Random vector       |                    Probabilistic input                    |

Concretely, a probabilistic input is composed of one marginal distribution
per input dimension, mirroring how a random vector
$\boldsymbol{X} = (X_1, \ldots, X_M)^T$ is composed of its component random
variables $X_1, \ldots, X_M$.

The following pages go into more detail:

- To learn more about how to create a (one-dimensional) marginal distribution,
  check out the {ref}`Creating a One-Dimensional Marginal Distribution <prob-input:marginal-distribution>`
  page.
- To learn more about how to model one or more input variables probabilistically,
  check out the {ref}`Creating a Probabilistic Input Model <prob-input:probabilistic-input-model>`
  page.
- To get an overview on the basic concepts in probability relevant to UQTestFuns,
  check out the {ref}`Probability Concepts and Notations <prob-input:concepts-and-notations>` page.

[^dependencies]: that is, outside the common numerical Python environment (NumPy and SciPy).
In fact, the univariate distributions in UQTestFuns wrap around the ones from `scipy.stats`
with parametrization that is more consistent with the applied UQ literature.

[^one-dimensional]: A marginal distribution of a joint distribution is not
necessarily one-dimensional in general (for example, the marginal over a
subset of components of a random vector). UQTestFuns' convention is to use
the term specifically for the one-dimensional case, corresponding to a
single component.