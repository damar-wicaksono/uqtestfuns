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

(fundamentals:sensitivity)=
# Test Functions for Sensitivity Analysis

The table below listed the available test functions typically used
in the comparison of sensitivity analysis methods.

|                             Name                             | Input Dimension |     Constructor      |
|:------------------------------------------------------------:|:---------------:|:--------------------:|
|          {ref}`Borehole <test-functions:borehole>`           |        8        |     `Borehole()`     |
| {ref}`Bratley et al. (1992) A <test-functions:bratley1992a>` |        M        |   `Bratley1992a()`   |
| {ref}`Bratley et al. (1992) B <test-functions:bratley1992b>` |        M        |   `Bratley1992b()`   |
| {ref}`Bratley et al. (1992) C <test-functions:bratley1992c>` |        M        |   `Bratley1992c()`   |
| {ref}`Bratley et al. (1992) D <test-functions:bratley1992d>` |        M        |   `Bratley1992d()`   |
| {ref}`Damped Oscillator <test-functions:damped-oscillator>`  |        7        | `DampedOscillator()` |
|             {ref}`Flood <test-functions:flood>`              |        8        |      `Flood()`       |
|      {ref}`Friedman (6D) <test-functions:friedman-6d>`       |        6        |    `Friedman6D()`    |
| {ref}`Genz (Corner Peak) <test-functions:genz-corner-peak>`  |        M        |  `GenzCornerPeak()`  |
|          {ref}`Ishigami <test-functions:ishigami>`           |        3        |     `Ishigami()`     |
|        {ref}`Moon (2010) 3D <test-functions:moon3d>`         |        3        |      `Moon3D()`      |
|   {ref}`Morris et al. (2006) <test-functions:morris2006>`    |        M        |    `Morris2006()`    |
|       {ref}`OTL Circuit <test-functions:otl-circuit>`        |     6 / 20      |    `OTLCircuit()`    |
|       {ref}`Piston Simulation <test-functions:piston>`       |     7 / 20      |      `Piston()`      |
| {ref}`Simple Portfolio Model <test-functions:portfolio-3d>`  |        3        |   `Portfolio3D()`    |
|    {ref}`SaltelliLinear <test-functions:saltelli-linear>`    |        M        |  `SaltelliLinear()`  |
|           {ref}`Sobol'-G <test-functions:sobol-g>`           |        M        |      `SobolG()`      |
|        {ref}`Sobol'-G* <test-functions:sobol-g-star>`        |        M        |    `SobolGStar()`    |
|     {ref}`Sobol'-Levitan <test-functions:sobol-levitan>`     |        M        |   `SobolLevitan()`   |
|     {ref}`Solar Cell Model <test-functions:solar-cell>`      |        5        |    `SolarCell()`     |
|            {ref}`Sulfur <test-functions:sulfur>`             |        9        |      `Sulfur()`      |
|    {ref}`Welch et al. (1992) <test-functions:welch1992>`     |       20        |    `Welch1992()`     |
|       {ref}`Wing Weight <test-functions:wing-weight>`        |       10        |    `WingWeight()`    |

In a Python terminal, you can list all the available functions relevant
for metamodeling applications using ``list_functions()``
and filter the results  using the ``tag`` parameter
(shown below in the HTML format):

```{code-cell} ipython3
:tags: ["output_scroll"]

import uqtestfuns as uqtf

uqtf.list_functions(tag="sensitivity", tablefmt="html")
```

## About sensitivity analysis

**Sensitivity analysis** is a class of model inference techniques
whose overarching aim is to _understand the input-output relationship_
of a complex (perhaps, even a black-box) computational model.
Within the uncertainty quantification (UQ) framework
(see {ref}`fundamentals:overview`), this aim is reframed as determining
how the uncertainty of the model output(s) is affected
by the uncertainty of the inputs.

While understanding the input-output relationship is valuable on its own[^model-building],
sensitivity analysis often focuses on more practical tasks, including:

- **Identifying of input variables that primarily drives the output uncertainty**:
  This knowledge enables _factor prioritization_, where efforts are concentrated
  on reducing the uncertainty of the most influential inputs (if possible)
  to significantly decrease the uncertainty of the outputs
- **Identifying of non-influential input variables**:
  This knowledge enables _factor fixing/screening_, where non-influential
  inputs are fixed to arbitrary value without 
  affecting significantly (or at all) the uncertainty of the outputs.
  In essence, factor fixing reduces the dimensionality of the problem.

Sensitivity analysis within the UQ framework are typically carried out in
a black-box manner, relying solely on model evaluations at carefully
selected input points.
The goal is then to achieve the aforementioned tasks with as few model
evaluations as possible.

For detailed discussions on this topic, see {cite}`Saltelli2007, Iooss2015`.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^model-building]: especially during model building and the ensuing verification
and validation activities.
