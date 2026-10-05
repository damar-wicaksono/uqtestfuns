(development:adding-marginal-distribution)=
# Adding a New Marginal Distribution Type

UQTestFuns ships with several one-dimensional
{ref}`marginal distributions <prob-input:available-marginal-distributions>`
(i.e., univariate distributions) used by its built-in test functions.
If a new test function needs a distribution type that isn't supported
yet, add the distribution to the codebase first.

In this guide, we'll explain how to add a new distribution type,
using the uniform distribution as a worked example:

$$
X \sim \mathcal{U}(a, b)
$$

where $a$ and $b$ are the distribution's parameters, the lower and
upper bounds, respectively.

```{note}
The uniform distribution is already in the codebase.
While it may seem rather contrived,
we're using it here anyway, since it's simple enough to walk through in full
while every code snippet below can be checked against the actual implementation.
```

Implementing the distribution correctly lets you create a `Marginal`
instance with it:

```python
>>> import uqtestfuns as uqtf
>>> my_var = uqtf.Marginal(distribution="uniform", parameters=[3, 5])
```

## Step 0: Putting things in the right place

Univariate random variables in UQTestFuns are represented as
instances of the `Marginal` class. The supported distributions are
implemented in separate modules under
`src/uqtestfuns/core/prob_input/univariate_distributions`:

```text
src/uqtestfuns/core/prob_input/univariate_distributions
├── __init__.py
├── beta.py       <- An implementation of the Beta distribution
├── gumbel.py     <- An implementation of the Gumbel (max.) distribution
├── ...
└── utils.py      <- Sub-package utility functions
```

Pick a name for your new distribution and add it to this directory as
a new module. For our worked example, that module already exists:
`uniform.py`.

## Step 1: Implementing the distribution

In the distribution module, you need to implement several module-level variables and functions;
they all need to have exactly the name and, for functions, signature as prescribed below.

| Name                                             | Description                                                                                                             |
|--------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| `DISTRIBUTION_NAME`                              | The name of the distribution (no whitespace, please), used as the `distribution` keyword when constructing a `Marginal` |
| `DISPLAY_NAME`                                   | Human-readable name of the distribution, used in `Marginal`'s string representation                                     |
| `NUM_PARAMS`                                     | The required number of parameters                                                                                       |
| `PARAM_NAMES`                                    | Tuple of parameter names, in the same order as `parameters`, also used in `Marginal`'s string representation            |
| `verify_parameters(parameters)`                  | Verification function                                                                                                   |
| `lower(parameters)`                              | Get the lower bound of the distribution                                                                                 |
| `upper(parameters)`                              | Get the upper bound of the distribution                                                                                 |
| `pdf(xx, parameters, lower_bound, upper_bound)`  | Compute the {term}`PDF` values on a set of input values                                                                 |
| `cdf(xx, parameters, lower_bound, upper_bound)`  | Compute the {term}`CDF` values on a set of input values                                                                 |
| `icdf(xx, parameters, lower_bound, upper_bound)` | Compute the {term}`ICDF` values on a set of input values                                                                |

### Required packages

First, import the commonly used packages and internal functions:

```python
import numpy as np

from .utils import postprocess_icdf, verify_param_nums
from ....global_settings import ARRAY_FLOAT
```

`postprocess_icdf()` and `verify_param_nums()` are shared helpers from
the sub-package's own `utils.py`: the former clamps a distribution's
raw ICDF output to stay within its bounds, the latter checks the
number of given parameters against what the distribution expects.
`ARRAY_FLOAT` is a type alias for `numpy.typing.NDArray[np.float64]`,
used throughout for type hints.

### Module-level variables

Four module-level variables must be defined, all in caps:
`DISTRIBUTION_NAME`, `DISPLAY_NAME`, `NUM_PARAMS`, and `PARAM_NAMES`.

For the uniform distribution:

```python
DISTRIBUTION_NAME = "uniform"
DISPLAY_NAME = "Uniform"
NUM_PARAMS = 2
PARAM_NAMES = ("a", "b")
```

```{note}
`DISTRIBUTION_NAME` is the registry lookup key: it's what a
`Marginal`'s `distribution` argument matches against. `DISPLAY_NAME`
and `PARAM_NAMES` are read directly by the string representation
of the `Marginal` instance.

None of these variables can be omitted.
```

### Verify parameters

The `verify_parameters()` function verifies the consistency of the given parameters.
In our example, the parameters of the uniform distribution are the lower and upper bounds of the distribution.
Therefore, the first parameter cannot be equal to or larger than the second parameter.

An implementation of the verification function is as follows:

```python
def verify_parameters(parameters: ARRAY_FLOAT) -> None:
    """Verify the parameters of a uniform distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of the uniform distribution
        (i.e., lower and upper bounds).

    Returns
    ------
    None
        The function exits without any return value when nothing is wrong.

    Raises
    ------
    ValueError
        If any of the parameter values are invalid
        or the shapes are inconsistent.
    """
    # Verify overall shape
    verify_param_nums(parameters.size, NUM_PARAMS, DISTRIBUTION_NAME)

    if parameters[0] >= parameters[1]:
        raise ValueError(
            f"The lower bound {parameters[0]} "
            f"cannot be greater than the upper bound {parameters[1]}!"
        )
```

### Lower bound

The `lower()` function returns the lower bound of the distribution.
Even for distributions that are technically unbounded,
this function must be defined for numerical reasons (see the box below).
In our example, the uniform distribution has a straightforward lower bound;
it's the first parameter.

```python
def lower(parameters: ARRAY_FLOAT) -> float:
    """Get the lower bound of a uniform distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a uniform distribution.

    Returns
    -------
    float
        The lower bound of the uniform distribution.
    """
    lower_bound = float(parameters[0])

    return lower_bound
```

```{important}
"Unbounded" doesn't mean `lower()`/`upper()` can return $\pm\infty$.
Even a genuinely unbounded distribution needs a finite numerical
bound, chosen so that the probability mass excluded by it is
negligible. The
{ref}`Normal <prob-input:marginal-distributions:normal>` distribution
is a good example. Its `lower()`/`upper()` pick the quantile at
probability $10^{-16}$ for the standard normal, scaled by `sigma` and
shifted by `mu`, so the probability mass on the order of $10^{-16}$ falls
outside `[lower, upper]`. The same pattern appears in every
distribution that's unbounded or semi-unbounded (`Gumbel (max.)`,
`Log-Normal`, `Exponential`).

$10^{-16}$ isn't an arbitrary choice. It's on the order of
`np.finfo(float).eps` ($\approx 2.2 \times 10^{-16}$), the relative
rounding error of double-precision arithmetic. The excluded tail mass
is therefore comparable to the rounding error already present in
ordinary floating-point calculations, and far below what any practical
sampling-based estimate could resolve.

This clamping could, in principle, affect a reliability study
targeting a failure probability smaller than roughly $10^{-15}$. All
the currently available reliability test functions have failure
probabilities far larger than that, typically by ten orders of
magnitude or more.
A future test function targeting such an extremely rare event would need to
account for this.
```

### Upper bound

Similarly to the `lower()` function, the `upper()` function returns
the upper bound of the distribution,
with the same numerical-bound reasoning applying.
In our example, the function reads:

```python
def upper(parameters: ARRAY_FLOAT) -> float:
    """Get the upper bound of a uniform distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a uniform distribution.

    Returns
    -------
    float
        The upper bound of the uniform distribution.
    """
    upper_bound = float(parameters[1])

    return upper_bound
```

### Cumulative distribution function (CDF)

The CDF is the function $F_X:\mathcal{D}_X \subseteq \mathbb{R} \mapsto [0, 1]$.
For the uniform distribution, this function reads:

$$
F_X (x; a, b) = \begin{cases} 0 & x < a \\ \frac{x - a}{b - a} & x \in [a, b] \\ 1 & x > b \end{cases}
$$

It can be implemented as follows:

```python
def cdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the CDF values of a uniform distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a uniform distribution.
    parameters : ARRAY_FLOAT
        Parameters of the uniform distribution.
    lower_bound : float
        Lower bound of the uniform distribution
    upper_bound : float
        Upper bound of the uniform distribution.

    Returns
    -------
    ARRAY_FLOAT
        The CDF values of the uniform distribution.

    Notes
    -----
    - The CDF values for sample values below the lower bound are set to 0.0,
      and for sample values above the upper bound are set to 1.0.
    """
    yy = np.empty(xx.shape)
    idx_lower = xx < lower_bound
    idx_upper = xx > upper_bound
    idx_rest = np.logical_and(
        np.logical_not(idx_lower), np.logical_not(idx_upper)
    )

    yy[idx_lower] = 0.0
    yy[idx_upper] = 1.0
    yy[idx_rest] = (xx[idx_rest] - parameters[0]) / np.diff(parameters)

    return yy
```

Note that for input values below (resp. above) the lower bound (resp. upper bound),
the function returns $0.0$ (resp. $1.0$).

### Probability density function (PDF)

The PDF is the function $f_X:\mathcal{D}_X \subseteq \mathbb{R} \mapsto \mathbb{R}_{\geq 0}$.
For the uniform distribution, the function reads:

$$
f_X (x; a, b) = \begin{cases} \frac{1}{b - a} & x \in [a, b] \\ 0 & x \notin [a, b] \end{cases}
$$

and can be implemented as follows:

```python
def pdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the PDF values of a uniform distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a uniform distribution.
    parameters : ARRAY_FLOAT
        Parameters of the uniform distribution.
    lower_bound: float
        Lower bound of the uniform distribution.
    upper_bound: float
        Upper bound of the distribution.

    Returns
    -------
    ARRAY_FLOAT
        The PDF values of the uniform distribution.

    Notes
    -----
    - The sample values ``xx`` themselves are not used in the computation of
      density value (it is, after all, a constant),
      but required nevertheless as the function is vectorized.
      Given a vector input, the function should return the PDF values of the
      same length as the input.
      Moreover, this signature must be consistent with the other distributions.
    - The values outside the bounds are set to 0.0.
    """
    yy = np.zeros(xx.shape)
    idx = np.logical_and(xx >= lower_bound, xx <= upper_bound)

    yy[idx] = 1 / (np.diff(parameters))

    return yy
```

Outside $[a, b]$, the PDF is zero.

### Inverse cumulative distribution function (ICDF)

Finally, the ICDF is the function $F_X^{-1}: [0, 1] \mapsto \mathcal{D}_X$.
For the uniform distribution, it reads:

$$
F^{-1}_X (x; a, b) = a + (b - a) \, x
$$

The implementation reads:

```python
def icdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the inverse CDF values of a uniform distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) in the [0, 1] domain.
    parameters : ARRAY_FLOAT
        Parameters of a uniform distribution.
    lower_bound : float
        Lower bound of the uniform distribution.
    upper_bound : float
        Upper bound of the uniform distribution.
        This parameter is not used but must appear for interface consistency.

    Returns
    -------
    np.ndarray
        Transformed values in the domain of the uniform distribution.
    Notes
    -----
    - ICDF for sample values outside [0.0, 1.0] is set to NaN.
    """
    xx[xx < 0.0] = np.nan
    xx[xx > 1.0] = np.nan

    # Compute the ICDF
    yy = (lower_bound + np.diff(parameters) * xx).astype(np.float64)

    # Check if values are within the set bounds
    yy_post = postprocess_icdf(yy, lower_bound, upper_bound)

    return yy_post
```

By convention, input values outside $[0, 1]$ are set to `NaN`.

## Step 2: Registering the distribution

Once you've done implementing the distribution,
be sure to register it in the module so UQTestFuns can discover it.
Modify the file `src/uqtestfuns/core/prob_input/utils.py` as follows:

```python
from .univariate_distributions import (
    ...
    uniform,   # Import the new module here
)

...

SUPPORTED_MARGINALS = {
    ...
    uniform.DISTRIBUTION_NAME: uniform,  # register the module with the name as the keyword
}
```

This way you can create a new instance of the `Marginal` class
by passing the chosen name as the `distribution`
and the corresponding parameters:

```python
>>> import uqtestfuns as uqtf
>>> my_var = uqtf.Marginal(distribution="uniform", parameters=[3, 5])
```

Remember that `uniform` here is exactly the string
assigned to `DISTRIBUTION_NAME` back in Step 1.

## Step 3: Running the test

UQTestFuns includes a test suite that tests the correctness
of all registered univariate distributions.
In most cases, you don't need to have a specific test
for the distribution you created.

So to make sure that there's nothing broken in the implementation, run `pytest`.

## Step 4: Adding the documentation

Once the distribution is implemented, registered, and tested, add its
documentation page under `docs/prob-input/marginal-distributions/`.
For our worked example, that page already exists:
{ref}`Uniform <prob-input:marginal-distributions:uniform>`.

Each page follows the same structure: a label and title, a short
opening sentence, a summary table (Notation, Parameters, Support,
PDF, CDF, ICDF), and a set of PDF/CDF/ICDF/sample-histogram plots
across a few parameter values. Follow the example of the other
distribution pages already in the documentation.

Once the page exists, make it discoverable by modifying these files.
Both keep their entries in alphabetical order, so add yours in the
right position:

- `docs/_toc.yml`, add an entry under the `prob-input/available`
  section's `marginal-distributions/` list
- `docs/prob-input/available.md`, add a row to the summary table
  (keyword value, mathematical notation, support, and number of
  parameters)

---

Congratulations!

You now know how to add a univariate distribution to the codebase!

Consider making the new distribution available to all
by {ref}`making a pull request <development:making-a-pull-request>`
to the main repository of UQTestFuns.
