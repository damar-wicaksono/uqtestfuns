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

The table below lists the available test functions typically used
in the comparison of sensitivity analysis methods.

|           Name           | Input Dimension  |                                                    Description                                                    |
|:------------------------:|:----------------:|:-----------------------------------------------------------------------------------------------------------------:|
|       ``Borehole``       |        8         |                                     {ref}`Borehole <test-functions:borehole>`                                     |
|       ``BratleyA``       |        M         |                             {ref}`Bratley et al. (1992) A <test-functions:bratley-a>`                             |
|       ``BratleyB``       |        M         |                             {ref}`Bratley et al. (1992) B <test-functions:bratley-b>`                             |
|       ``BratleyC``       |        M         |                             {ref}`Bratley et al. (1992) C <test-functions:bratley-c>`                             |
|       ``BratleyD``       |        M         |                             {ref}`Bratley et al. (1992) D <test-functions:bratley-d>`                             |
|   ``DampedOscillator``   |        7         |                            {ref}`Damped Oscillator <test-functions:damped-oscillator>`                            |
|        ``Flood``         |        8         |                                        {ref}`Flood <test-functions:flood>`                                        |
|      ``Friedman6D``      |        6         |                                 {ref}`Friedman (6D) <test-functions:friedman-6d>`                                 |
|    ``GenzCornerPeak``    |        M         |                            {ref}`Genz (Corner Peak) <test-functions:genz-corner-peak>`                            |
|  ``GenzDiscontinuous``   |        M         |                          {ref}`Genz (Discontinuous) <test-functions:genz-discontinuous>`                          |
|       ``Ishigami``       |        3         |                                     {ref}`Ishigami <test-functions:ishigami>`                                     |
| ``LinkletterDecCoeffs``  |        10        |          {ref}`Linkletter et al. (2006) Decreasing Coefficients <test-functions:linkletter-dec-coeffs>`           |
|   ``LinkletterInert``    |        10        |                      {ref}`Linkletter et al. (2006) Inert <test-functions:linkletter-inert>`                      |
|   ``LinkletterLinear``   |        10        |                     {ref}`Linkletter et al. (2006) Linear <test-functions:linkletter-linear>`                     |
|    ``LinkletterSine``    |        10        |                       {ref}`Linkletter et al. (2006) Sine <test-functions:linkletter-sine>`                       |
|        ``Moon3D``        |        3         |                                   {ref}`Moon (2010) 3D <test-functions:moon3d>`                                   |
|       ``MorrisM``        |        M         |                              {ref}`Morris et al. (2006) <test-functions:morris2006>`                              |
|      ``OTLCircuit``      |        6         |                               {ref}`OTL Circuit (6D) <test-functions:otl-circuit>`                                |
|    ``OTLCircuit20D``     |        20        |                             {ref}`OTL Circuit (20D) <test-functions:otl-circuit-20d>`                             |
|        ``Piston``        |        7         |                               {ref}`Piston Simulation (7D) <test-functions:piston>`                               |
|      ``Piston20D``       |        20        |                            {ref}`Piston Simulation (20D) <test-functions:piston-20d>`                             |
|     ``Portfolio3D``      |        3         |                            {ref}`Simple Portfolio Model <test-functions:portfolio-3d>`                            |
|    ``SaltelliLinear``    |        M         |                              {ref}`SaltelliLinear <test-functions:saltelli-linear>`                               |
|        ``SobolG``        |        M         |                                     {ref}`Sobol'-G <test-functions:sobol-g>`                                      |
|      ``SobolGStar``      |        M         |                                  {ref}`Sobol'-G* <test-functions:sobol-g-star>`                                   |
|     ``SobolLevitan``     |        M         |                               {ref}`Sobol'-Levitan <test-functions:sobol-levitan>`                                |
|      ``SolarCell``       |        5         |                      {ref}`Constantine et al. (2015) Solar Cell <test-functions:solar-cell>`                      |
|        ``Sulfur``        |        9         |                           {ref}`Charlson et al. (1992) Sulfur <test-functions:sulfur>`                            |
|       ``Welch20D``       |        20        |                             {ref}`Welch et al. (1992) 20D <test-functions:welch1992>`                             |
|      ``WingWeight``      |        10        |                                  {ref}`Wing Weight <test-functions:wing-weight>`                                  |

In a Python terminal, you can list all the available functions relevant
for sensitivity analysis applications using ``list_functions()``
and filter the results  using the ``tag`` parameter:

```python
import uqtestfuns as uqtf

uqtf.list_functions(tag="sensitivity")
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

- **Identifying input variables that primarily drive the output uncertainty**:
  This knowledge enables _factor prioritization_, where efforts are concentrated
  on reducing the uncertainty of the most influential inputs (if possible)
  to significantly decrease the uncertainty of the outputs
- **Identifying non-influential input variables**:
  This knowledge enables _factor fixing/screening_, where non-influential
  inputs are fixed to arbitrary value without 
  affecting significantly (or at all) the uncertainty of the outputs.
  In essence, factor fixing reduces the dimensionality of the problem.

Sensitivity analysis within the UQ framework is typically carried out in
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
