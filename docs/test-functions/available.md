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

# All Available Functions

This table below lists all the available _classic_ test functions from the literature
available in the current UQTestFuns, regardless of their typical applications.

|                            Name                             | Spatial Dimension |     Constructor      |
|:-----------------------------------------------------------:|:-----------------:|:--------------------:|
|          {ref}`Borehole <test-functions:borehole>`          |         8         |     `Borehole()`     |
| {ref}`Damped Oscillator <test-functions:damped-oscillator>` |         7         | `DampedOscillator()` |
|             {ref}`Flood <test-functions:flood>`             |         8         |      `Flood()`       |
|          {ref}`Ishigami <test-functions:ishigami>`          |         3         |     `Ishigami()`     |
|       {ref}`OTL Circuit <test-functions:otl-circuit>`       |      6 / 20       |    `OTLCircuit()`    |
|      {ref}`Piston Simulation <test-functions:piston>`       |      7 / 20       |      `Piston()`      |
|       {ref}`Wing Weight <test-functions:wing-weight>`       |        10         |    `WingWeight()`    |

In a Python terminal, you can list all the available functions
along with the corresponding constructor using ``list_functions()``:

```{code-cell} ipython3
import uqtestfuns as uqtf

uqtf.list_functions()
```
