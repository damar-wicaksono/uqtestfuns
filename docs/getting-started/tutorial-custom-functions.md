---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(getting-started:tutorial-custom-functions)=
# Tutorial: Create a Custom Test Function

You can add your own uncertainty quantification (UQ) test function
to UQTestFuns, so that it shares the same interface
as the {ref}`built-in ones <getting-started:tutorial-built-in-functions>`.
There are two ways to do it:

1. *Interactively*, within a Python session. The function lives only
   in that session and is gone once it ends, unless you save it yourself.
2. *As part of the package*, by implementing the function into the codebase.
   The function is then available like any other built-in,
   every time you import UQTestFuns.

This tutorial covers the interactive route.
To add a test function as a module instead,
see the {ref}`relevant section <development:adding-test-function-implementation>`
in the Developer's Guide.

By the end, you'll have combined the three components of a test function
(evaluation function, probabilistic input, and parameters) into a single object
that behaves like any {ref}`built-in one <getting-started:tutorial-built-in-functions>`.

```{code-cell}
import numpy as np
import uqtestfuns as uqtf
```

## UQ test functions revisited

A UQ test function has three components:

- *an evaluation function* that takes inputs and produces outputs;
  you can think of it as a black-box;
- *a probabilistic input model* that specifies the inputs to that function
  as a joint random variable; the results of a UQ analysis
  depend on this specification;
- (optional) *a set of parameters* that completes the specification;
  once set, these values stay fixed throughout evaluation
  (for example, a flag, a numerical tolerance, or a time-step size).

The distinction between input and parameters is worth pinning down,
because a UQ test function treats them very differently.
The probabilistic input is the uncertain part of the problem:
you put distributions over it, sample from it, and propagate it
through the function to see how the output responds.

The parameters, on the other hand, are not uncertain.
They are part of the model's definition, held fixed while the input varies.
Changing a parameter does not produce a new sample from the same function;
it changes which function you are studying.
This is why the two are specified separately.

Before building a new test function, it helps to think about it
in these three terms and to have each specification ready.

## Branin function

Suppose we want to add the two-dimensional Branin (or Branin-Hoo) function
as a test function {cite}`Dixon1978`.
It is a classic optimization benchmark,
with three global optima across its domain, and it reads

$$
\mathcal{M}(x_1, x_2) = a \left( x_2 - b x_1^2 + c x_1 - r \right)^2 + s \left( 1 - t \right) \cos{(x_1)} + s,
$$

where $x_1$ and $x_2$ are the input variables
and $\{ a, b, c, r, s, t \}$ are the parameters.

The input variables are defined as follows:

|  Name  | Distribution |  Parameters |
| :----: |:------------:| :---------: |
| $x_1$  |   uniform    | $[-5, 10]$  |
| $x_2$  |   uniform    |  $[0, 15]$  |

The parameters take the following typical values:

| Parameter |          Value          |
| :-------: |:-----------------------:|
|    $a$    |          $1.0$          |
|    $b$    | $\frac{5.1}{(2 \pi)^2}$ |
|    $c$    |     $\frac{5}{\pi}$     |
|    $r$    |           $6$           |
|    $s$    |          $10$           |
|    $t$    |    $\frac{1}{8 \pi}$    |

## Evaluation function

The first component is the evaluation function itself.
UQTestFuns requires the function to take the input array as its first argument,
with any parameters following after.
The Branin function takes its six parameters individually.

The evaluation functions should follow the convention that the input `xx` is an
`N`-by-`M` NumPy array, where `N` is the number of points and `M` is the
input dimension. The function should return a one-dimensional NumPy array
of length `N`.

```{code-cell}
def evaluate_branin(
    xx: np.ndarray,
    a: float,
    b: float,
    c: float,
    r: float,
    s: float,
    t: float,
) -> np.ndarray:
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
        a * (xx[:, 1] - b * xx[:, 0] ** 2 + c * xx[:, 0] - r) ** 2
        + s * (1 - t) * np.cos(xx[:, 0])
        + s
    )

    return yy
```

## Probabilistic input

The second component is the probabilistic input.
For the Branin function it consists of two independent uniform random variables
with different bounds.
In UQTestFuns, a probabilistic input model is represented
by the {ref}`ProbInput <api_reference_probabilistic_input>` class,
built from a list
of {ref}`Marginal <api_reference_marginal_distribution>` objects,
one per input variable.
For a uniform marginal, the two parameters are the lower and upper bounds.

```{code-cell}
# Define a list of marginals
marginals = [
    uqtf.Marginal(distribution="uniform", parameters=[-5, 10], name="x1"),
    uqtf.Marginal(distribution="uniform", parameters=[0, 15], name="x2"),
]
# Create a probabilistic input
my_input = uqtf.ProbInput(marginals=marginals, name="Branin")
```

Print the instance to verify it:

```{code-cell}
print(my_input)
```

## Parameters

The third and final component is the parameter set.
Not every test function has one;
the Branin function has six parameters, $\{ a, b, c, r, s, t \}$.

A parameter set in UQTestFuns is represented
by the {ref}`Parameters <api_reference_parameters>` class.
You construct it from a dictionary, mapping each keyword to its value:

```{code-cell}
my_params = uqtf.Parameters(
    values={
        "a": 1.0,
        "b": 5.1 / (2 * np.pi) ** 2,
        "c": 5 / np.pi,
        "r": 6.0,
        "s": 10.0,
        "t": 1 / (8 * np.pi),
    },
    name="Branin",
)
```

The keywords must match the parameter names
in the evaluation function's signature,
since they are passed to it as keyword arguments.
The values can be of any Python type;
what matters is that the evaluation function knows how to consume them.

Print the instance to verify it:

```{code-cell}
print(my_params)
```
## Creating a UQ test function

```{margin}
Recall that a UQ test function consists of an evaluation function,
a probabilistic input model, and (optionally) a set of parameters.
```

The three components are combined into a test function
through the `UQTestFun` class.
The `name` and `descriptions` fields are optional,
but can be useful for documenting the object:

```{code-cell}
my_testfun = uqtf.UQTestFun(
    evaluate=evaluate_branin,
    prob_input=my_input,
    parameters=my_params,
    name="Branin",
    description="Branin optimization test function",
)
```

Print the instance to verify it:

```{code-cell}
print(my_testfun)
```

Congratulations! You've built a Branin test function inside a Python session,
and it behaves like any {ref}`built-in one <getting-started:tutorial-built-in-functions>`.
You can now use it just like one.

```{admonition} Common issues
:class: tip

Some common issues that may arise during the construction and evaluation
of a UQTestFun instance:

- the evaluation function does not accept `xx` as its first argument;
- parameter names in `Parameters` do not match
  the evaluation function signature;
- the evaluation function returns a scalar instead of an array of length `N`;
- the number of input columns does not match the number of marginals.
```

## Using a UQ test function

To generate a few random sample points from the input model,
access the underlying `prob_input`:

```{code-cell}
xx = my_testfun.prob_input.get_sample(10)
xx
```

To evaluate the function on the sample points, call the instance:

```{code-cell}
yy = my_testfun(xx)
yy
```

The surface and contour plots below both evaluate the function on a grid.

```{code-cell}
:tags: [hide-input]
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- Create a 2-D grid
grid_size = 250
xx_1 = np.linspace(
    my_input.marginals[0].lower, my_input.marginals[0].upper, grid_size
)
xx_2 = np.linspace(
    my_input.marginals[1].lower, my_input.marginals[1].upper, grid_size
)
mesh_2d = np.meshgrid(xx_1, xx_2)
xx_2d = np.array(mesh_2d).T.reshape(-1, 2)
yy_2d = my_testfun(xx_2d)

# --- Create the plots
fig = plt.figure(figsize=(11, 5))

# --- Surface plot
axs_1 = plt.subplot(121, projection="3d")
axs_1.plot_surface(
    mesh_2d[0],
    mesh_2d[1],
    yy_2d.reshape(grid_size, grid_size).T,
    cmap="plasma",
    linewidth=0,
    antialiased=False,
    alpha=0.5,
)
axs_1.set_xlabel(r"$x_1$", fontsize=14)
axs_1.set_ylabel(r"$x_2$", fontsize=14)
axs_1.set_zlabel(r"$\mathcal{M}(x_1, x_2)$", fontsize=14)

# --- Contour plot
axs_2 = plt.subplot(122)
cf = axs_2.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(grid_size, grid_size).T, 20, cmap="plasma"
)
axs_2.set_xlabel(r"$x_1$", fontsize=14)
axs_2.set_ylabel(r"$x_2$", fontsize=14)
divider = make_axes_locatable(axs_2)
cax = divider.append_axes("right", size="5%", pad=0.05)
fig.colorbar(cf, cax=cax, orientation="vertical")
axs_2.axis("scaled")

# --- Mark the three global optima
axs_2.scatter(
    np.array([-np.pi, np.pi, 9.42478]),
    np.array([12.275, 2.275, 2.475]),
    s=80,
    marker="x",
    color="white",
)

fig.tight_layout(pad=3.0)
```

The white markers on the contour plot show the three global optima.

```{margin}
The parameter sets that ship with built-in functions are protected to preserve
their provenance, so you cannot modify them in place. To experiment with a
built-in function's parameters, work from a copy instead. See the
{ref}`built-in functions tutorial <getting-started:tutorial-built-in-functions>`
for how.
```

Because you built this function yourself, its parameter set is yours to modify.
You can change a parameter in place by its keyword:

```{code-cell}
my_testfun.parameters["a"] = 3.5
my_testfun.parameters["t"] = 1 / (4 * np.pi)
```

The next evaluation uses the new values, which reshape the landscape:

```{code-cell}
:tags: [hide-input]

# --- Create a 2-D grid
grid_size = 250
xx_1 = np.linspace(
    my_input.marginals[0].lower, my_input.marginals[0].upper, grid_size
)
xx_2 = np.linspace(
    my_input.marginals[1].lower, my_input.marginals[1].upper, grid_size
)
mesh_2d = np.meshgrid(xx_1, xx_2)
xx_2d = np.array(mesh_2d).T.reshape(-1, 2)
yy_2d = my_testfun(xx_2d)

# --- Create the plots
fig = plt.figure(figsize=(11, 5))

# --- Surface plot
axs_1 = plt.subplot(121, projection="3d")
axs_1.plot_surface(
    mesh_2d[0],
    mesh_2d[1],
    yy_2d.reshape(grid_size, grid_size).T,
    cmap="plasma",
    linewidth=0,
    antialiased=False,
    alpha=0.5,
)
axs_1.set_xlabel(r"$x_1$", fontsize=14)
axs_1.set_ylabel(r"$x_2$", fontsize=14)
axs_1.set_zlabel(r"$\mathcal{M}(x_1, x_2)$", fontsize=14)

# --- Contour plot
axs_2 = plt.subplot(122)
cf = axs_2.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(grid_size, grid_size).T, 20, cmap="plasma"
)
axs_2.set_xlabel(r"$x_1$", fontsize=14)
axs_2.set_ylabel(r"$x_2$", fontsize=14)
divider = make_axes_locatable(axs_2)
cax = divider.append_axes("right", size="5%", pad=0.05)
fig.colorbar(cf, cax=cax, orientation="vertical")
axs_2.axis("scaled");
```

## Concluding remarks

The test function you built lives only in the current Python session.
To reuse it in another session,
place the evaluation function and component definitions in a Python script
or notebook and run them again when needed.
Alternatively, you can save the object to disk and load it later.

For a more permanent solution,
you can extend UQTestFuns by adding the function into the codebase.
Once the function is part of the package,
it constructs like any other built-in.

Suppose you name it `Branin`, then

```python
my_testfun = uqtf.Branin()
```

would build an instance using the default input and parameter values.
The {ref}`relevant section <development:adding-test-function-implementation>`
of the Developer's Guide walks through how.

---

## Summary

This tutorial showed the basic workflow
for creating a custom test function interactively:

1. define an evaluation function;
2. define a probabilistic input model;
3. optionally define parameters;
4. combine them into a `UQTestFun` instance.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```