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

# Test Functions for Optimization

The table below listed the available test functions typically used
in the comparison of global optimization methods.

|                            Name                             | Spatial Dimension |     Constructor      |
|:-----------------------------------------------------------:|:-----------------:|:--------------------:|
|            {ref}`Ackley <test-functions:ackley>`            |         M         |      `Ackley()`      |

In a Python terminal, you can list all the available functions relevant
for optimization applications using ``list_functions()`` and filter the results
using the ``tag`` parameter:

```{code-cell} ipython3
import uqtestfuns as uqtf

uqtf.list_functions(tag="optimization")
```
