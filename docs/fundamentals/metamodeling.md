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

# Test Functions for Metamodeling

The table below listed the available test functions typically used
in the comparison of metamodeling approaches.

|                              Name                              | Spatial Dimension |     Constructor      |
|:--------------------------------------------------------------:|:-----------------:|:--------------------:|
|             {ref}`Ackley <test-functions:ackley>`              |         M         |      `Ackley()`      |
|           {ref}`Borehole <test-functions:borehole>`            |         8         |     `Borehole()`     |
|  {ref}`Damped Oscillator <test-functions:damped-oscillator>`   |         7         | `DampedOscillator()` |
|              {ref}`Flood <test-functions:flood>`               |         8         |      `Flood()`       |
|   {ref}`Forrester et al. (2008) <test-functions:forrester>`    |         1         |  `Forrester2008()`   |
|         {ref}`(1st) Franke <test-functions:franke-1>`          |         2         |     `Franke1()`      |
|         {ref}`(2nd) Franke <test-functions:franke-2>`          |         2         |     `Franke2()`      |
|         {ref}`(3rd) Franke <test-functions:franke-3>`          |         2         |     `Franke3()`      |
|         {ref}`(4th) Franke <test-functions:franke-4>`          |         2         |     `Franke4()`      |
|         {ref}`(5th) Franke <test-functions:franke-5>`          |         2         |     `Franke5()`      |
|         {ref}`(6th) Franke <test-functions:franke-6>`          |         2         |     `Franke6()`      |
| {ref}`Gramacy (2007) 1D Sine <test-functions:gramacy-1d-sine>` |         1         |  `Gramacy1DSine()`   |
| {ref}`Oakley and O'Hagan (2002) 1D <test-functions:oakley-1d>` |         1         |     `Oakley1D()`     |
|        {ref}`OTL Circuit <test-functions:otl-circuit>`         |      6 / 20       |    `OTLCircuit()`    |
|          {ref}`McLain S1 <test-functions:mclain-s1>`           |         2         |     `McLainS1()`     |
|          {ref}`McLain S2 <test-functions:mclain-s2>`           |         2         |     `McLainS2()`     |
|          {ref}`McLain S3 <test-functions:mclain-s3>`           |         2         |     `McLainS3()`     |
|          {ref}`McLain S4 <test-functions:mclain-s4>`           |         2         |     `McLainS4()`     |
|          {ref}`McLain S5 <test-functions:mclain-s5>`           |         2         |     `McLainS5()`     |
|        {ref}`Piston Simulation <test-functions:piston>`        |      7 / 20       |      `Piston()`      |
|             {ref}`Sulfur <test-functions:sulfur>`              |         9         |      `Sulfur()`      |
|          {ref}`Welch1992 <test-functions:welch1992>`           |        20         |    `Welch1992()`     |
|        {ref}`Wing Weight <test-functions:wing-weight>`         |        10         |    `WingWeight()`    |

In a Python terminal, you can list all the available functions relevant
for metamodeling applications using ``list_functions()`` and filter the results
using the ``tag`` parameter:

```{code-cell} ipython3
:tags: ["output_scroll"]

import uqtestfuns as uqtf

uqtf.list_functions(tag="metamodeling")
```
