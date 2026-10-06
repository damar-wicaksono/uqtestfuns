(development:adding-test-function-implementation)=
# Adding a New Test Function Implementation

In this guide, we will explain how to implement a new UQ test function
into the UQTestFuns codebase.
A test function may be added on runtime using the ``UQTestFun`` class
as illustrated {ref}`here <getting-started:tutorial-custom-functions>`.
However, adding the test function directly to the codebase is advantageous
in that it becomes exposed to the high-level convenient functionalities
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
\mathcal{M}(x_1, x_2) = a \left( x_2 - b x_1^2 + c x_1 - r \right)^2 + s \left(1 - t \right) \cos{(x_1)} + s
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

We are going to implement this test function into the UQTestFuns codebase step-by-step.

## Step 0: Putting things in the right place

A built-in test function in UQTestFuns is defined by a pair of files
sharing the same stem, e.g. `branin.yaml` and `branin.py`, both stored
inside `src/uqtestfuns/test_functions` (with respect to the source root
directory). The YAML file declares everything about the function
except its evaluation logic, which is supplied by the Python module.

```{note}
For the full picture of how these two files get discovered and turned
into a usable `UQTestFun` instance, see {ref}`development:how-it-works`.
```

If you have a look at the directory you'll see the following (or something similar):

```text
test_functions/                     <- Sub-package that contains all UQ test function specs
├── __init__.py
├── ackley.yaml                     <- Specification of the Ackley function
├── ackley.py                       <- Evaluation logic of the Ackley function
├── borehole.yaml                   <- Specification of the borehole function
├── borehole.py                     <- Evaluation logic of the borehole function
├── ...
├── wing_weight.yaml                <- Specification of the wing weight function
└── wing_weight.py                  <- Evaluation logic of the wing weight function
```

For the Branin function, you'll add two files to this directory:
`branin.yaml` and `branin.py`.

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

### Implementing the evaluation function

You'll need `numpy` at minimum, and `scipy` is fine too, but we don't
otherwise add external dependencies to UQTestFuns.

For an implementation of a test function, create a top module-level function
(conventionally named `evaluate()` if there is only one test function in the
module):

```python
import numpy as np


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

## Step 2: Writing the specification

With `branin.py` in place, the next step is telling UQTestFuns about the
function: its name, its input space, and its parameters. This goes in
a YAML file with the same stem, `branin.yaml`, in the same directory.

This section only covers what Branin itself needs. For the full
schema, the different ways to declare marginals, parameter-value
expressions, shared inputs across function families, and so on, see
the {ref}`development:yaml-specification`.

### Declaring the function

Start with the function's identity: its name (which doubles as the
registry key and the constructor name, e.g. `uqtf.Branin()`), a short
description, and the tags describing its typical use.

```yaml
name: Branin
description: Branin function from Dixon and Szegő (1978)
tags:
  - optimization

dimensions:
  input: 2
  output: 1
```

`tags` must be drawn from a fixed set (`sensitivity`, `optimization`,
`metamodeling`, `reliability`, `integration`). These are what
`list_functions(tag=...)` filters on.

```{note}
Nothing in this YAML file names `branin.py` or its `evaluate()`
function explicitly. By default, the parser looks for a module with
the same stem as the YAML file (`branin.py`, matching `branin.yaml`)
and a function inside it named `evaluate`, exactly what Step 1
produced. An `evaluate` key exists for cases where that default
doesn't apply; the full schema reference covers those.
```

### Declaring the input space

Declare Branin's two input variables under `inputs`, using a unique ID
for this input specification (here, `Dixon1978`).
Each variable is one entry in a `marginals` list, in the same order
`evaluate()` expects them as `xx`'s columns:

```yaml
inputs:
  Dixon1978:
    description: Search domain for the Branin function from Dixon and Szegő (1978)
    marginals:
      - name: x1
        distribution: uniform
        parameters: [-5, 10]
      - name: x2
        distribution: uniform
        parameters: [0, 15]
```

```{note}
When a function declares more than one input specification, a
top-level `default_input` key names which one is used when
`uqtf.Branin()` is called without specifying `input_id` explicitly.
Branin only has one specification here, so this key can be omitted
entirely.
```

### Declaring the parameters

Declare Branin's six parameters under `parameters`, again keyed by the
source they come from. Constants involving $\pi$ can be written as
arithmetic expressions using `$()`:

```yaml
parameters:
  keyword_descriptions:
    a: Overall scaling constant
    b: Quadratic term coefficient
    c: Linear term coefficient
    r: Constant offset
    s: Additive constant
    t: Cosine term coefficient
  sets:
    Dixon1978:
      description: Parameter set from Dixon and Szegő (1978)
      a: 1.0
      b: $(5.1 / (2 * pi)**2)
      c: $(5 / pi)
      r: 6.0
      s: 10.0
      t: $(1 / (8 * pi))
```

The keyword names here (`a`, `b`, `c`, `r`, `s`, `t`) must exactly
match `evaluate()`'s parameter arguments.

```{note}
The same applies to `default_parameters`: a key under
`parameters` naming which parameter set is used by default, needed only
when a function declares more than one set. Branin only has one set here,
so it can be omitted too.
```

## Step 3: Sanity check

With both files in place, it's worth confirming everything is
correctly picked up before moving on.

```{note}
Earlier versions of the package required each new function to be
explicitly registered, by importing it in a package `__init__.py`.
That's no longer necessary: the registry discovers `branin.yaml`
automatically at import time.
```

A quick way to confirm this:

```python
>>> import uqtestfuns as uqtf
>>> "Branin" in uqtf.list_functions(tabulate=False)
True
```

Constructing and calling the function should also work:

```python
>>> branin = uqtf.Branin()
>>> branin
<UQTestFun name='Branin', input_dimension=2, input_id='Dixon1978', parameters_id='Dixon1978'>
```

If either check fails, the error usually points at what's wrong in
`branin.yaml`, since a malformed specification is caught the first
time the function is looked up.

## Step 4: Implementing a test

Although a generic test suite has been included that applies to all UQ test functions,
some test functions may have particular behaviors that must be tested separately.
In the case of the Branin function, as an optimization test function,
the optimum value and its (three) locations are known analytically:

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
`tests/builtin_test_functions/test_branin.py` and write:

```python
"""
Test module for the Branin test function.

Notes
-----
- The tests defined in this module deal with
  the correctness of the evaluation.
"""
import numpy as np

from uqtestfuns import Branin


def test_optimum_value():
    """Test the optimum values of the Branin function"""
    # Create a test instance
    branin_fun = Branin()

    yy_opt = 0.397887
    xx_opt = np.array([[-np.pi, 12.275], [np.pi, 2.275], [9.42478, 2.475]])

    # Assertions
    assert np.allclose(branin_fun(xx_opt), yy_opt)
```

Then run `pytest` from the root source directory to make sure that the function,
especially its evaluation function, has been implemented properly.

```{note}
Branin only has one parameter set, so a single hardcoded test is
enough. For a function with more than one, tests are usually
parametrized across the available sets instead; see, for instance,
`tests/builtin_test_functions/test_ishigami.py`.
```

## Step 5: Adding the documentation of the test function

Each test function in UQTestFuns has its dedicated page in the docs.
Your new test function is no exception! Check out the guide on
{ref}`adding a new test function documentation <development:adding-test-function-docs>`
to see how.

---

Congratulations, you've just successfully implemented your first UQ
test function and added it to the codebase!

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```
