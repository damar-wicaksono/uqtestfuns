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

|                              Name                              | Spatial Dimension |     Constructor      |
|:--------------------------------------------------------------:|:-----------------:|:--------------------:|
|             {ref}`Ackley <test-functions:ackley>`              |         M         |      `Ackley()`      |
|           {ref}`Borehole <test-functions:borehole>`            |         8         |     `Borehole()`     |
|  {ref}`Bratley et al. (1992) A <test-functions:bratley1992a>`  |         M         |   `Bratley1992a()`   |
|  {ref}`Bratley et al. (1992) B <test-functions:bratley1992b>`  |         M         |   `Bratley1992b()`   |
|  {ref}`Bratley et al. (1992) C <test-functions:bratley1992c>`  |         M         |   `Bratley1992c()`   |
|  {ref}`Bratley et al. (1992) D <test-functions:bratley1992d>`  |         M         |   `Bratley1992d()`   |
|  {ref}`Damped Oscillator <test-functions:damped-oscillator>`   |         7         | `DampedOscillator()` |
|              {ref}`Flood <test-functions:flood>`               |         8         |      `Flood()`       |
|   {ref}`Forrester et al. (2008) <test-functions:forrester>`    |         1         |  `Forrester2008()`   |
|         {ref}`(1st) Franke <test-functions:franke-1>`          |         2         |     `Franke1()`      |
|         {ref}`(2nd) Franke <test-functions:franke-2>`          |         2         |     `Franke2()`      |
|         {ref}`(3rd) Franke <test-functions:franke-3>`          |         2         |     `Franke3()`      |
|         {ref}`(4th) Franke <test-functions:franke-4>`          |         2         |     `Franke4()`      |
|         {ref}`(5th) Franke <test-functions:franke-5>`          |         2         |     `Franke5()`      |
|         {ref}`(6th) Franke <test-functions:franke-6>`          |         2         |     `Franke6()`      |
|         {ref}`Gayton Hat <test-functions:gayton-hat>`          |         2         |    `GaytonHat()`     |
| {ref}`Gramacy (2007) 1D Sine <test-functions:gramacy-1d-sine>` |         1         |  `Gramacy1DSine()`   |
|           {ref}`Ishigami <test-functions:ishigami>`            |         3         |     `Ishigami()`     |
| {ref}`Oakley and O'Hagan (2002) 1D <test-functions:oakley-1d>` |         1         |     `Oakley1D()`     |
|        {ref}`OTL Circuit <test-functions:otl-circuit>`         |      6 / 20       |    `OTLCircuit()`    |
|          {ref}`McLain S1 <test-functions:mclain-s1>`           |         2         |     `McLainS1()`     |
|          {ref}`McLain S2 <test-functions:mclain-s2>`           |         2         |     `McLainS2()`     |
|          {ref}`McLain S3 <test-functions:mclain-s3>`           |         2         |     `McLainS3()`     |
|          {ref}`McLain S4 <test-functions:mclain-s4>`           |         2         |     `McLainS4()`     |
|          {ref}`McLain S5 <test-functions:mclain-s5>`           |         2         |     `McLainS5()`     |
|        {ref}`Piston Simulation <test-functions:piston>`        |      7 / 20       |      `Piston()`      |
|            {ref}`Sobol'-G <test-functions:sobol-g>`            |         M         |      `SobolG()`      |
|             {ref}`Sulfur <test-functions:sulfur>`              |         9         |      `Sulfur()`      |
|          {ref}`Welch1992 <test-functions:welch1992>`           |        20         |    `Welch1992()`     |
|        {ref}`Wing Weight <test-functions:wing-weight>`         |        10         |    `WingWeight()`    |

In a Python terminal, you can list all the available functions
along with the corresponding constructor using ``list_functions()``:

```{code-cell} ipython3
:tags: ["output_scroll"]

import uqtestfuns as uqtf

uqtf.list_functions()
```
