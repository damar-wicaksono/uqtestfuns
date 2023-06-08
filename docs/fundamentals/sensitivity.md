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

# Test Functions for Sensitivity Analysis

The table below listed the available test functions typically used
in the comparison of sensitivity analysis methods.

|                            Name                             | Spatial Dimension |     Constructor      |
|:-----------------------------------------------------------:|:-----------------:|:--------------------:|
|          {ref}`Borehole <test-functions:borehole>`          |         8         |     `Borehole()`     |
| {ref}`Damped Oscillator <test-functions:damped-oscillator>` |         7         | `DampedOscillator()` |
|             {ref}`Flood <test-functions:flood>`             |         8         |      `Flood()`       |
|          {ref}`Ishigami <test-functions:ishigami>`          |         3         |     `Ishigami()`     |
|       {ref}`OTL Circuit <test-functions:otl-circuit>`       |      6 / 20       |    `OTLCircuit()`    |
|      {ref}`Piston Simulation <test-functions:piston>`       |      7 / 20       |      `Piston()`      |
|          {ref}`Sobol'-G <test-functions:sobol-g>`           |         M         |      `SobolG()`      |
|            {ref}`Sulfur <test-functions:sulfur>`            |         9         |      `Sulfur()`      |
|    {ref}`Welch et al. (1992) <test-functions:welch1992>`    |        20         |    `Welch1992()`     |
|       {ref}`Wing Weight <test-functions:wing-weight>`       |        10         |    `WingWeight()`    |

In a Python terminal, you can list all the available functions relevant
for metamodeling applications using ``list_functions()`` and filter the results
using the ``tag`` parameter:

```{code-cell} ipython3
import uqtestfuns as uqtf

uqtf.list_functions(tag="sensitivity")
```
