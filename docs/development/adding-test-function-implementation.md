(development:adding-test-function-implementation)=
# Adding a New Test Function Implementation

In this guide, we will explain how to implement a new UQ test function into the UQTestFuns code base.
A test function may be added on runtime using the ``UQTestFun`` class as illustrated {ref}`here <getting-started:creating-a-custom>`.
However, adding the test function directly to the code base is advantageous
that it becomes exposed to the high-level convenient functionalities
(such as `list_functions()`).
Furthermore, once merged, the test function will become available for all.

```{note}
Before moving on, make sure you've set up a local development environment
as explained {ref}`here <development:setting-up-dev-env>`.
```

Similar to creating a new test function on runtime,
we are going to use the Branin function as the motivating problem.
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
│   ├── available.py            <- Utility functions of the sub-package
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

from typing import Optional

from ..core.uqtestfun_abc import UQTestFunABC
from ..core.prob_input.univariate_distribution import UnivDist
from .available import (
    create_prob_input_from_available,
    create_parameters_from_available,
)

__all__ = ["Branin"]
```

Here are some explanations:

- NumPy is usually a must, especially for implementing the evaluation function.
- All test functions are concrete implementations of the abstract base class `UQTestFunABC`.
- One-dimensional marginals are defined using the `UnivDist` class.
- `create_prob_input_from_available` and `create_parameters_from_available` are internal functions used to allow users to select a particular probabilistic input
  and/or parameters specifications (from several available selections) using a keyword passed in the class constructor.

### Implementing a concrete class

Each built-in test function is an implementation of the abstract base class `UQTestFunABC`.
`UQTestFunABC` prescribes an abstract method called `evaluate`
and a few class-level properties that must be implemented in the concrete class.
More about them is below.

But first, we create a new class called `Branin` derived from this abstract base class:

```python
class Branin(UQTestFunABC):
    ...
```

Afterward, we need to define the constructor of the class.
The rules regarding the signature of the constructor are not written in stone (yet, or ever).
But keep in mind that you should be able to call the constructor without any obligatory parameters.

Following the precedence of how signatures for the other test functions are written, we write the constructor along with its body:

```python
class Branin(UQTestFunABC):
    """A concrete implementation of the 2-dimensional Branin test function.

    Parameters
    ----------
    spatial_dimension : int
        The requested number of spatial_dimension. If not specified,
        the default is set to 2.
    prob_input_selection : str, optional
        The selection of a probabilistic input model from a list of
        available specifications. This is a keyword-only parameter.
    parameters_selection : str, optional
        The selection of a parameters set from a list of available
        parameter sets. This is a keyword-only parameter.
    """

    def __init__(
        self,
        *,
        prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
        parameters_selection: Optional[str] = DEFAULT_PARAMETERS_SELECTION,
        name: Optional[str] = None,
    ):
        # --- Arguments processing
        # Create a probabilistic input model based on the selection
        prob_input = create_prob_input_from_available(
            prob_input_selection, AVAILABLE_INPUT_SPECS
        )
        # Select parameters
        parameters = create_parameters_from_available(
            parameters_selection, AVAILABLE_PARAMETERS
        )
        # Process the default name
        if name is None:
            name = Branin.__name__

        super().__init__(
            prob_input=prob_input, parameters=parameters, name=name
        )
```

Here we expose the following (optional) parameters in the constructor:

- `prob_input_selection`: so a keyword selecting a particular probabilistic input specification can be passed
- `parameters_selection`: so a keyword selecting a particular set of parameters values can be passed
- `name`: so a custom name of an instance can be passed

Notice that these parameters are all optional and must be given as keyword arguments (it's good to be explicit).

There are a couple of missing things in the constructor definition above: 

- `DEFAULT_INPUT_SELECTION` and `AVAILABLE_INPUT_SPECS`
- `DEFAULT_PARAMETERS_SELECTION` and `AVAILABLE_PARAMETERS`

### Specifying probabilistic input model

`AVAILABLE_INPUT_SPECS` is a module-level variable that stores a dictionary containing
all the available input specifications available in UQTestFuns for the Branin function.
We define the variable as follows:

```python
AVAILABLE_INPUT_SPECS = {
    "Dixon1978": {
        "name": "Branin-Dixon-2008",
        "description": (
            "Search domain for the Branin function from Dixon and Szegö (1978)."
        ),
        "marginals": INPUT_MARGINALS_DIXON1978,
        "copulas": None,
    }
}
```

Each element of this dictionary contains the arguments to create an input model as an instance of the `ProbInput` class.
For this particular example, we only have one input specification available.
If there were more, we would add them here in the dictionary each with a unique keyword.

```{note}
The keyword is, by convention, the citation key of the particular reference as listed in the BibTeX file. 
```

In the code above, we store the specification of the marginal inside another variable.
The marginals specification is a list of instances of `UnivDist` describing each of the input variables.

```python
INPUT_MARGINALS_DIXON1978 = [
    UnivDist(
        name="x1",
        distribution="uniform",
        parameters=[-5, 10],
        description="None",
    ),
    UnivDist(
        name="x2",
        distribution="uniform",
        parameters=[0.0, 15.0],
        description="None",
    ),
]
```

Finally, we need to tell UQTestFuns which input specification needs to be used by default.
We put the keyword selecting the default specification inside the variable `DEFAULT_INPUT_SELECTION`:

```python
DEFAULT_INPUT_SELECTION = "Dixon1978"
```

With that, we have completed the input specification of the Branin function.

### Specifying parameters

Similar to the previous step, `DEFAULT_PARAMETERS_SELECTION` is a module-level variable that stores a string keyword referring
to the default set of parameter values for the Branin function.

```python
DEFAULT_PARAMETERS_SELECTION = "Dixon1978"
```

As before, the keyword refers to a dictionary that contains all the available parameter values.
For this example, we need to define the dictionary inside a module-level variable called `AVAILABLE_PARAMETERS`:

```python
AVAILABLE_PARAMETERS = {
    "Dixon1978": np.array(
        [1.0, 5.1 / (2 * np.pi) ** 2, 5 / np.pi, 6, 10, 1 / 8 / np.pi]
    )
}
```

### Implementing a concrete evaluation method

For an implementation of a test function, the abstract method `evaluate()` must be implemented.

```python
    ...
    def evaluate(self, xx: np.ndarray):
        """Evaluate the Branin function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            2-Dimensional input values given by an N-by-2 array where
            N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the Branin func. evaluated on the input values.
            The output is a 1-dimensional array of length N.
        """
        params = self.parameters
        yy = (
            params[0]
            * (
                xx[:, 1]
                - params[1] * xx[:, 0] ** 2
                + params[2] * xx[:, 0]
                - params[3]
            )
            ** 2
            + params[4] * (1 - params[5]) * np.cos(xx[:, 0])
            + params[4]
        )

        return yy
```

Notice that the stored function parameters are accessible as a property of the instance and can be accessed via `self`;
the parameter should not be directly passed in the calling of the method.

### Adding concrete class properties

Several class properties must be defined for a concrete implementation.
They are useful for the organization and bookkeeping of the test functions.

```python
class Branin(UQTestFunABC):
    ...
    _tags = ["optimization"]  # Application tags

    _available_inputs = tuple(AVAILABLE_INPUT_SPECS.keys())  # Input selection keywords

    _available_parameters = tuple(AVAILABLE_PARAMETERS.keys())  # Parameters selection keywords

    _default_spatial_dimension = 2  # Spatial dimension of the function

    _description = "Branin function from Dixon and Szegö (1978)"  # Short description
    ...
```

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
  ...
  "Branin",
  ...
]
```

Now you can check if all has been correctly set up by listing the available built-in function from a Python terminal.

```python
>>> import uqtestfuns as uqtf
>>> uqtf.list_functions()
 No.      Constructor       Spatial Dimension          Application          Description
-----  ------------------  -------------------  --------------------------  ----------------------------------------------------------------------------
  1         Ackley()                M           optimization, metamodeling  Ackley function from Ackley (1987)
  2        Borehole()               8           metamodeling, sensitivity   Borehole function from Harper and Gupta (1983)
  3         Branin()                2                  optimization         Branin function from Dixon and Szegö (1978)
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
