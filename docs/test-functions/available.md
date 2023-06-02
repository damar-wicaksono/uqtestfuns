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

(test-functions:available)=
# All Available Functions

The table below lists all the available _classic_ test functions from the literature
available in the current UQTestFuns, regardless of their typical applications.

|                            Name                             | Spatial Dimension |     Constructor      |
|:-----------------------------------------------------------:|:-----------------:|:--------------------:|
|            {ref}`Ackley <test-functions:ackley>`            |         M         |      `Ackley()`      |
|          {ref}`Borehole <test-functions:borehole>`          |         8         |     `Borehole()`     |
| {ref}`Damped Oscillator <test-functions:damped-oscillator>` |         7         | `DampedOscillator()` |
|             {ref}`Flood <test-functions:flood>`             |         8         |      `Flood()`       |
|        {ref}`(1st) Franke <test-functions:franke-1>`        |         2         |     `Franke1()`      |
|        {ref}`(2nd) Franke <test-functions:franke-2>`        |         2         |     `Franke2()`      |
|        {ref}`(3rd) Franke <test-functions:franke-3>`        |         2         |     `Franke3()`      |
|          {ref}`Ishigami <test-functions:ishigami>`          |         3         |     `Ishigami()`     |
| {ref}`Oakley-O'Hagan 1D <test-functions:oakley-ohagan-1d>`  |         1         |  `OakleyOHagan1D()`  |
|       {ref}`OTL Circuit <test-functions:otl-circuit>`       |      6 / 20       |    `OTLCircuit()`    |
|         {ref}`McLain S1 <test-functions:mclain-s1>`         |         2         |     `McLainS1()`     |
|         {ref}`McLain S2 <test-functions:mclain-s2>`         |         2         |     `McLainS2()`     |
|         {ref}`McLain S3 <test-functions:mclain-s3>`         |         2         |     `McLainS3()`     |
|         {ref}`McLain S5 <test-functions:mclain-s5>`         |         2         |     `McLainS5()`     |
|      {ref}`Piston Simulation <test-functions:piston>`       |      7 / 20       |      `Piston()`      |
|          {ref}`Sobol'-G <test-functions:sobol-g>`           |         M         |      `SobolG()`      |
|            {ref}`Sulfur <test-functions:sulfur>`            |         9         |      `Sulfur()`      |
|       {ref}`Wing Weight <test-functions:wing-weight>`       |        10         |    `WingWeight()`    |

In a Python terminal, you can list all the available functions
along with the corresponding constructor using ``list_functions()``:

```{code-cell} ipython3
import uqtestfuns as uqtf

uqtf.list_functions()
```
