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

(fundamentals:integration)=
# Test Functions for Numerical Integration

The table below listed the available test functions typically used
in the testing and comparison of numerical integration method.

|                                    Name                                     | Input Dimension |     Constructor     |
|:---------------------------------------------------------------------------:|:---------------:|:-------------------:|
|        {ref}`Bratley et al. (1992) A <test-functions:bratley1992a>`         |        M        |  `Bratley1992a()`   |
|        {ref}`Bratley et al. (1992) B <test-functions:bratley1992b>`         |        M        |  `Bratley1992b()`   |
|        {ref}`Bratley et al. (1992) C <test-functions:bratley1992c>`         |        M        |  `Bratley1992c()`   |
|        {ref}`Bratley et al. (1992) D <test-functions:bratley1992d>`         |        M        |  `Bratley1992d()`   |
|         {ref}`Genz (Corner Peak) <test-functions:genz-corner-peak>`         |        M        | `GenzCornerPeak()`  |
|                  {ref}`Sobol'-G <test-functions:sobol-g>`                   |        M        |     `SobolG()`      |
|            {ref}`Welch et al. (1992) <test-functions:welch1992>`            |       20        |    `Welch1992()`    |

In a Python terminal, you can list all the available functions relevant
for metamodeling applications using ``list_functions()`` and filter the results
using the ``tag`` parameter:

```{code-cell} ipython3
:tags: ["output_scroll"]

import uqtestfuns as uqtf

uqtf.list_functions(tag="integration", tablefmt="html")
```
