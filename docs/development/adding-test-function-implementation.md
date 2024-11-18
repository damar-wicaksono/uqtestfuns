(development:adding-test-function-implementation)=
# Adding a New Test Function Implementation

In this guide, we will explain how to implement a new UQ test function into the UQTestFuns code base.
A test function may be added on runtime using the ``UQTestFun`` class
as illustrated {ref}`here <getting-started:tutorial-custom-functions>`.
However, adding the test function directly to the code base is advantageous
that it becomes exposed to the high-level convenient functionalities
(such as `list_functions()`).
Furthermore, once merged, the test function will become available for all.

```{note}
Before moving on, make sure you've set up a local development environment
as explained {ref}`here <development:setting-up-dev-env>`.
```

Similar to creating a new test function on runtime,
we are going to use the Branin function {cite}`Dixon1978` as the motivating problem.
The function is defined as follows:

$$
\mathcal{M}(x_1, x_2) = a \left( x_2 - b x_1^2 + c x_1 - r \right)^2 + s \left(1 - t \right) \cos{(x_1}) + s
$$

where $x_1$ and $x_2$ are the input variables
and $\{ a, b, c, r, s, t \}$ are the parameters.

The input variables are defined in the table below.

|   No.    |  Name   | Distribution  | Parameters  |
|:--------:|:-------:|:-------------:|:-----------:|
|    1     |  $x_1$  |    uniform    | $[-5, 10]$  |
|    2     |  $x_2$  |    uniform    |  $[0, 15]$  |

The typical values for the parameters are shown in the table below.

| No.     | Parameter |          Value          |
|:-------:|:---------:|:-----------------------:|
| 1       |    $a$    |        $1.0$            |
| 2       |    $b$    | $\frac{5.1}{(2 \pi)^2}$ |
| 3       |    $c$    |     $\frac{5}{\pi}$     |
| 4       |    $r$    |           $6$           |
| 5       |    $s$    |          $10$           |
| 6       |    $t$    |    $\frac{1}{8 \pi}$    |

We are going to implement this test function into the UQTestFuns code base step-by-step.

## Step 0: Putting things in the right place

A built-in test function in UQTestFuns is implemented as a Python module 
and stored inside `src/uqtestfuns/test_functions` (with respect to the source root directory).
If you have a look at the directory you'll see the following (or something similar):

```text
├── core
├── test_functions              <- Sub-package that contains all UQ test function modules
│   ├── __init__.py
│   ├── ackley.py               <- An implementation of the Ackley function
│   ├── borehole.py             <- An implementation of the borehole function
│   ├── damped_oscillator.py    <- An implementation of the damped oscillator model
│   ├── ...
│   └── wing_weight.py          <- An implementation of the wing weight function
├── ...
└── utils.py
```

Say you've (aptly) named the Python module implementing the Branin function `branin.py`.
You must put that file inside the directory.

## Step 1: Implementing the function

Now you're ready to implement the test function inside `branin.py`.
Let's start with module-level docstring.

### Adding module-level docstring

Describe the module and add some information regarding the test function,
where it was first used and in which context.
Don't forget to add the proper bibliographic information here (under the heading _References_).

So for example, we may write the following as the module-level docstring.

```python
"""
Module with an implementation of the two-dimensional Branin function.

The Branin function is a two-dimensional scalar-valued function.
The function is commonly used as a test function for optimization algorithms [1].

References
----------

1. L. C. W. Dixon and G. P. Szegö. Towards global optimization 2,
   chapter The global optimization problem: an introduction, pages 1–15.
   North-Holland, Amsterdam, 1978.
"""
```

### Importing relevant packages, classes, and functions

Next, there are a few packages, classes, and utility functions
that are commonly used in every test function implementation.
Depending on a particular test function, you might import more.
Be aware, however, we don't arbitrarily add external dependencies
to UQTestFuns (outside NumPy and SciPy).

Here are the few things we usually use:

```python
import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs, FunParamSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["Branin"]
```

Here are some explanations:

- NumPy is usually a must, especially for implementing the evaluation function.
- Because Branin test function is a test function with a fixed number of (input)
  dimensions, the class will be derived from the abstract base class
  {ref}`UQTestFunFixDimABC <api_reference_uqtestfun_fix_dim_abc>`.
- To assist specifying the data for probabilistic input model the custom type
  `ProbInputSpecs` can be used; these are supposed to help you specifying
  all the required data via the typechecker.
- Similarly, the custom type `FunParamSpecs` is used for specifying the
  function parameters.

```{notes}
In case the function is of variable dimension, use the abstract base class
{ref}`UQTestFunVarDimABC <api_reference_uqtestfun_var_dim_abc>` instead.
```

### Implementing a concrete evaluation function

For an implementation of a test function, create a top module-level function
(conventionally named `evaluate()` if there is only one test function in the
module):

```python
def evaluate(xx: np.ndarray, a: float, b: float, c: float, r: float, s: float, t: float):
    """Evaluate the Branin function on a set of input values.
    
    Parameters
    ----------
    xx : np.ndarray
        2-Dimensional input values given by an N-by-2 array where
        N is the number of input values.
    a : float
        Parameter 'a' of the Branin function.
    b : float
        Parameter 'b' of the Branin function.
    c : float
        Parameter 'c' of the Branin function.
    r : float
        Parameter 'r' of the Branin function.
    s : float
        Parameter 's' of the Branin function.
    t : float
        Parameter 't' of the Branin function.
    
    Returns
    -------
    np.ndarray
        The output of the Branin function evaluated on the input values.
        The output is a 1-dimensional array of length N.    
    """
    yy = (
        a * (xx[:, 1] - b * xx[:, 0]**2 + c * xx[:, 0] - r)**2
        + s * (1 - t) * np.cos(xx[:, 0]) 
        + s
    )
    
    return yy
```

Notice that for a test function with parameters, the signature should also
include the parameters.

### Specifying probabilistic input model

The specification of the probabilistic model is stored in a module-level
dictionary. While you're free to name the dictionary anything you like,
the convention is `AVAILABLE_INPUTS`.
We define the variable as follows:

```python
AVAILABLE_INPUT_SPECS: ProbInputSpecs = {
    "Dixon1978": {
        "name": "Branin",
        "description": (
            "Search domain for the Branin function from Dixon and Szegö (1978)."
        ),
        "marginals": [
            {
                "name": "x1",
                "distribution": "uniform",
                "parameters": [-5, 10],
                "description": None,
            },
            {
                "name": "x2",
                "distribution": "uniform",
                "parameters": [0.0, 15.0],
                "description": None,
            },
        ],
        "copulas": None,
    },
}
```

Each key-value pair of this dictionary contains the specification
to create an input model as an instance of the `ProbInput` class.
For this particular example, we only have one input specification available.
If there were more, we would add them here in the dictionary each with a unique keyword.

```{note}
The keyword is, by convention, the citation key of the particular reference as listed in the BibTeX file. 
```

Also notice that in the code above, we store the specifications of
the marginals in a list of marginal specifications.
Each element of this list is used to create an instance of `Marginal`.

With that, we have completed the input specification of the Branin function.

### Specifying parameters

For a parameterized test function, we also need to define a module-level
dictionary that stores the parameter sets.
Conventionally, we name this variable `AVAILABLE_PARAMETERS`:

```python
AVAILABLE_PARAMETERS: FunParamSpecs = {
    "Dixon1978": {
      "function_id": "Branin",
      "description": "Parameter set for the Branin function from Dixon (1978)",
      "declared_parameters": [
          {
              "keyword": "a",
              "value": 1.0,
              "type": float,
          },
          {
              "keyword": "b",
              "value": 5.1 / (2 * np.pi) ** 2,
              "type": float,
          },
          {
              "keyword": "c",
              "value": 5 / np.pi,
              "type": float,
          },
          {
              "keyword": "r",
              "value": 6.0,
              "type": float,
          },
          {
              "keyword": "s",
              "value": 10.0,
              "type": float,
          },
          {
              "keyword": "t",
              "value": 1 / 8 / np.pi,
              "type": float,
          },
      ],
    },
}
```

This is a nested dictionary, where each top key-value pair contains one set of 
parameters from the literature.

The value of the parameters in the set can be of any type, as long as it is
consistent  with how the parameters are going to be consumed
by the `evaluate()` function.

As before, if there are multiple parameter sets available in the literature,
additional key-value pair should be added here.

### Implementing a concrete class

Each built-in test function is an implementation of the abstract base class
`UQTestFunABC`.
A concrete implementation of this base class requires the following:

- a static method named `evaluate()`
- several class-level properties, namely: `_tags`, `_description`, 
  `_available_inputs`, `_available_parameters`, `_default_input_id`,
  and `_default_parameters_id`.

The full definition of the class for the Branin test function is shown below.

```python
class Branin(UQTestFunABC):
    """A concrete implementation of the Branin test function."""
  
    _tags = ["optimization"]  # Application tags
    _description = "Branin function from Dixon and Szegö (1978)"  # Short description
    _available_inputs = AVAILABLE_INPUTS          # As defined above 
    _available_parameters = AVAILABLE_PARAMETERS  # As defined above
    _default_input_id = "Dixon1978"       # Optional, if only one input is available
    _default_parameters_id = "Dixon1978"  # Optional, if only one set of parameters is available

    evaluate = staticmethod(evaluate)  # assuming `evaluate()` has been defined
```

There is no need to define an `__init__()` method.
We will use the default `__init__()` from the base class.

Notice the two last class properties: `_default_input` and `_default_parameters`.
In case of only one input specification (resp. set of parameters) is available,
these properties are optional.
With more than one specification (resp. set), you must explicitly tell UQTestFuns
which specification and set should be used by default (i.e., when not specified).

With this, the test function implementation is complete.
We now need to import the test function at the package level.

## Step 2: Making the function available upstream

To make your new test function available upstream, you need to modify
the file `src/uqtestfuns/test_functions/__init__.py` with the following:

```python
...
from .branin import Branin
...

__all__ = [
  ...,
  "Branin",
  ...,
]
```

Now you can check if all has been correctly set up by listing the available
built-in functions from a Python terminal.

```python
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
|   5   |            Branin()           |     2     |     1      |  False   | optimization  | Branin function from Dixon     |
|       |                               |           |            |          |               | and Szegö (1978)               |
+-------+-------------------------------+-----------+------------+----------+---------------+--------------------------------+
...
```

## Step 3: Implementing a test

Although a generic test suite has been included that applies to all UQ test functions.
Some test functions may have particular behaviors that must be tested separately.
In the case of the Branin function, as an optimization test function,
the optimum value and their (three) locations are known (analytically):

$$
\begin{align}
  \mathcal{M}(\boldsymbol{x}^*) & = 0.397887 \\
  \boldsymbol{x}^*_1  & = (-\pi, 12.275) \\
  \boldsymbol{x}^*_2  & = (\pi, 2.275)\\
  \boldsymbol{x}^*_3  & = (9.42478, 2.475)\\
\end{align}
$$

An additional test can (and should) be added to the suite to test this.
Create a new test file specifically for the Branin function in
`tests/uq_test_functions/test_branin.py` and write:

```python
"""
Test module for the Branin test function.

Notes
-----
- The tests defined in this module deal with
  the correctness of the evaluation.
"""
import numpy as np
import uqtestfuns as uqtf

def test_optimum_value():
    """Test the optimum values of the Branin function"""
    # Create a test instance
    branin_fun = uqtf.Branin()

    yy_opt = 0.397887
    xx_opt = np.array([[-np.pi, 12.275], [np.pi, 2.275], [9.42478, 2.475]])

    # Assertions
    assert np.allclose(branin_fun(xx_opt), yy_opt)
```

Then run `pytest` from the root source directory to make sure that the function,
especially its evaluation function, has been implemented properly.

## Step 4: Adding the documentation of the test function

Each test function in UQTestFuns has its dedicated page in the docs.
Your new test function is no exception!
Check out {ref}`this guide <development:adding-test-function-docs>`
on how to add the documentation for a test function.

---

Congratulations you just successfully implemented your first UQ test function
and add it to the code base!

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```
