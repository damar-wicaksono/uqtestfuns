# Welcome to the UQTestFuns documentation!

UQTestFuns is an open-source Python3 library of test functions commonly used
within the applied uncertainty quantification (UQ) community.
Specifically, the package provides:

- an implementation _with minimal dependencies_ (i.e., NumPy and SciPy) and
  _a common interface_ of many test functions available in the UQ literature
- a _single entry point_ collecting test functions _and_ their probabilistic
  input specifications in a single Python package
- an _opportunity for an open-source contribution_, supporting
  the implementation of new test functions or posting reference results.

UQTestFuns aims to save the researchers' and developers' time from having to
reimplement many of the commonly used test functions (and the corresponding
probabilistic input specifications) from the UQ literature themselves.
More background information regarding UQ test functions and UQTestFuns
can be found {ref}`here <getting-started:about-uq-test-functions>`.

::::{grid}
:gutter: 2

:::{grid-item-card} Getting Started
:text-align: center
New to, but ready to use, UQTestFuns?
You can check out the tutorials!
Need some background info first?
Check out the what & why of these test functions.
+++
```{button-ref} getting-started:tutorials
:ref-type: myst
:color: primary
:outline:
To the UQTestFuns Tutorials
```
```{button-ref} getting-started:about-uq-test-functions
:ref-type: myst
:color: primary
:outline:
About UQ Test Functions
```
:::

:::{grid-item-card} User Guide
:text-align: center

Browse through all the available test functions in UQTestFuns;
they are crudely classified into their usage in typical UQ analyses.
Need a reference on how to define a probabilistic input model,
there's a dedicated section on that!
+++
```{button-ref} test-functions:available
:ref-type: myst
:color: primary
:outline:
To the List of Available Functions
```
```{button-ref} prob-input:overview
:ref-type: myst
:color: primary
:outline:
To the Probabilistic Input Modeling
```
:::

::::


::::{grid}
:gutter: 2

:::{grid-item-card} API Reference
:text-align: center
The API reference guide contains a detailed description of high-level entities
(functions, classes, methods, and properties) included in UQTestFuns.
+++
```{button-ref} api-reference:overview
:ref-type: myst
:color: primary
:outline:
To the API Reference
```

:::

:::{grid-item-card} Contributor's Guide
:text-align: center
If you're interested in extending UQTestFuns, be it adding a new test function,
a new distribution, or a new reference results in the docs,
be sure to check out the Contributor's Guide.
+++
```{button-ref} development:overview
:ref-type: myst
:color: primary
:outline:
To the Contributor's Guide
```
:::

::::

