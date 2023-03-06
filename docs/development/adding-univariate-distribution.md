(development:adding-univ-dist)=
# Adding a New Univariate Distribution Type

UQTestFuns is delivered with several {ref}`univariate distributions <prob-input:available-univariate-distributions>`
that are used by the currently available test functions.
In case a new univariate distribution type is required for a new test function,
the distribution should be added first to the code base.

This guide will help you with adding a new distribution type to the code base.
As a motivating example, let's assume we want to add the uniform distribution to the code base.

$$
X \sim \mathcal{U}(a, b)
$$

where $a$ and $b$ are the parameters of the distribution.
They correspond to the lower and upper bounds of the distribution, respectively.

```{note}
Strictly speaking, this is not necessary, because the uniform distribution is
_already_ in the code base.
It's a rather contrived example, we admit.
```

By implementing the distribution correctly, you'll be able to create a univariate random variable with that distribution.
For example:

```python
>>> import uqtestfuns as uqtf
>>> my_var = uqtf.UnivDist(distribution="uniform", parameters=[3, 5])
```

## Step 0: Putting things in the right place

Univariate random variables in UQTestFuns are represented as instances of the `UnivDist` class.
The supported distributions for the random variables are implemented in separate modules
located in the `src/uqtestfuns/core/prob_input/univariate_distributions` directory.
Here's how the directory look:

```text
src/uqtestfuns/core/prob_input/univariate_distributions
├── __init__.py
├── beta.py       <- An implementation of the Beta distribution
├── gumbel        <- An implementation of the Gumbel (max.) distribution
├── ...
└── utils.py      <- Sub-package utility functions
```

Pick a name for your new distribution and add it to this directory.
For our example, the name `uniform.py` would be apt.

## Step 1: Implementing the distribution

In the distribution module, you need to implement several module-level variables and functions;
they all need to have exactly the name and, for functions, signature as prescribed below.

| Name | Description |
|----|-------------|
| `DISTRIBUTION_NAME`             | The name of the distribution (no whitespace, please) |
| `NUM_PARAMS`                    | The required number of parameters | 
| `verify_parameters(parameters)` | Verification function |
| `lower(parameters)`             | Get the lower bound of the distribution |
| `upper(parameters)`             | Get the upper bound of the distribution |
| `pdf(xx, parameters, lower_bound, upper_bound)` | Compute the {term}`PDF` values on a set of input values |
| `cdf(xx, parameters, lower_bound, upper_bound)` | Compute the {term}`CDF` values on a set of input values |
| `icdf(xx, parameters, lower_bound, upper_bound)` | Compute the {term}`ICDF` values on a set of input values |

### Required packages

First, import the commonly used packages and internal functions:

```python
import numpy as np

from .utils import postprocess_icdf, verify_param_nums
from ....global_settings import ARRAY_FLOAT
```

### Module-level variables

Two module-level variables must be defined in all caps: `DISTRIBUTION_NAME` and `NUM_PARAMS`.
We pick the obvious name for the uniform distribution and assign the required number of parameters ($2$) to `NUM_PARAMS`:

```python
DISTRIBUTION_NAME = "uniform"  # lower case

NUM_PARAMS = 2
```

### Verify parameters

The `verify_parameters()` function verifies the consistency of the given parameters.
In our example, the parameters of the uniform distribution are the lower and upper bound of the distribution.
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
Even for distributions that are technically unbounded, this function must be defined for numerical consideration.
In our example, the uniform distribution has a straightforward lower bound; it's the first parameter.

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

### Upper bound

Similarly to the `lower()` function, the `upper()` function returns the upper bound of the distribution.
In our example, the function may read:

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

Note that for input values below (resp. above) the function lower bound (resp. upper bound), the function returns $0.0$ (resp. $1.0$). 

### Probability density function (PDF)

The PDF is the function $F_X:\mathcal{D}_X \subseteq \mathbb{R} \mapsto \mathbb{R}_{\geq 0}$.
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

Note that outside the function domain, the function values are zero.

### Inverse cumulative distribution function (ICDF)

Finally, the ICDF is the function $F_X^{-1}: [0, 1] \mapsto \mathcal{D}_X$.
For the uniform distribution, it reads:

$$
F^{-1}_X (x; a, b) = a + (b - a) \, x
$$

and can be implemented as follows:

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
    yy = lower_bound + np.diff(parameters) * xx

    # Check if values are within the set bounds
    yy = postprocess_icdf(yy, lower_bound, upper_bound)

    return yy
```

Note that by convention, input values outside the function domain, that is, $x \notin [0, 1]$, give invalid values.

## Step 2: Registering the distribution

Once you've done implementing the distribution, be sure to register it in the module so UQTestFuns can discover it.
Modify the file `src/uqtestfuns/prob_input/utils.py` as follows:

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

This way you can create a new instance of `UnivDist` class by passing the chosen name as the `distribution` and the corresponding parameters:

```python
>>> import uqtestfuns as uqtf
>>> my_var = uqtf.UnivDist(distribution="uniform", parameters=[3, 5])
```

Remember that the name `uniform` was chosen as the name of this distribution via the module-level variable `DISTRIBUTION_NAME`.

## Step 3: Running the test

UQTestFuns includes a test suite that tests the correctness of all registered univariate distributions.
In most cases, you don't need to have a specific test for the distribution you created.
Therefore, run `pytest` and make sure there's nothing broken.

---

Congratulations! You now know how to add a univariate distribution to the code base!

Consider making the new distribution available to all by {ref}`making a pull request <development:making-a-pull-request>`
to the main repository of UQTestFuns.