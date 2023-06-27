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

# Test Functions for Reliability Analysis

The table below listed the available test functions typically used
in the comparison of reliability analysis methods.

|                                        Name                                         | Spatial Dimension |           Constructor           |
|:-----------------------------------------------------------------------------------:|:-----------------:|:-------------------------------:|
| {ref}`Damped Oscillator Reliability <test-functions:damped-oscillator-reliability>` |         8         | `DampedOscillatorReliability()` |
|                    {ref}`Gayton Hat <test-functions:gayton-hat>`                    |         2         |          `GaytonHat()`          |
|               {ref}`Hyper-sphere Bound <test-functions:hyper-sphere>`               |         2         |         `HyperSphere()`         |

In a Python terminal, you can list all the available functions relevant
for metamodeling applications using ``list_functions()`` and filter the results
using the ``tag`` parameter:

```{code-cell} ipython3
:tags: ["output_scroll"]

import uqtestfuns as uqtf

uqtf.list_functions(tag="reliability")
```
