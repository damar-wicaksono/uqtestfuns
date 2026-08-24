---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(api-reference:overview)=
# UQTestFuns API Reference Guide

This reference guide describes the main building blocks of UQTestFuns:
how to get a test function instance, and what objects make it up.

```{note}
For a tour of how a built-in test function actually gets constructed
under the hood, see {ref}`development:how-it-works` in the
Contributor's Guide.
```

## Getting a test function instance

The primary entry point is {ref}`create() <api_reference_create>`,
a factory function that looks up a built-in test function by name and
returns a ready-to-use instance:

```{code-cell} ipython3
import uqtestfuns as uqtf

my_testfun = uqtf.create("Borehole")
print(my_testfun)
```

As a shorthand, every built-in function is also available as a
constructor of the same name (`uqtf.Borehole()`, `uqtf.Ishigami()`, etc.);
both routes go through the same underlying registry.

Three companion functions help with discovery:

- {ref}`list_functions() <api_reference_list_functions>` lists all
  built-in test functions, optionally filtered by dimension or tag.
- {ref}`list_parameters(name) <api_reference_list_parameters>` lists the
  available parameter sets for a given function.
- {ref}`list_inputs(name) <api_reference_list_inputs>` lists the
  available probabilistic input specifications for a given function.

## The object model

Every built-in test function is an instance of the same concrete class,
{ref}`UQTestFun <api_reference_uqtestfun>` (there is no per-function
subclass to look up). A `UQTestFun` instance is a callable object made up
of three parts:

- An evaluation function, invoked by calling the instance directly:
  `my_testfun(xx)`.
- A {ref}`ProbInput <api_reference_probabilistic_input>` (accessible via
  the `prob_input` property), the probabilistic input model defining the
  function's input space. A `ProbInput` is composed of one
  {ref}`Marginal <api_reference_marginal_distribution>` per input
  dimension; each `Marginal` represents a single one-dimensional
  probability distribution.
- An optional {ref}`Parameters <api_reference_parameters>` set
  (accessible via the `parameters` property), for functions that expose
  named, literature-defined parameter values. Not every function has
  parameters; `my_testfun.parameters` is `None` when it doesn't.

```{code-cell} ipython3
print(my_testfun.prob_input)
```

```{code-cell} ipython3
xx = my_testfun.prob_input.get_sample(5)
yy = my_testfun(xx)
yy
```

A parameterized function, by contrast, exposes its parameter set
directly:

```{code-cell} ipython3
ishigami = uqtf.create("Ishigami")
print(ishigami.parameters)
```

```{note}
To build a custom test function outside of the built-in registry,
construct a {ref}`UQTestFun <api_reference_uqtestfun>` directly from your
own evaluation function and `ProbInput`. See
{ref}`getting-started:tutorial-custom-functions` for a worked example.
```
