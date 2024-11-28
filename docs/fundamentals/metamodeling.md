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

(fundamentals:metamodeling)=
# Test Functions for Metamodeling

The table below listed the available test functions typically used
in the comparison of metamodeling approaches.

|                                  Name                                  | Input Dimension |      Constructor       |
|:----------------------------------------------------------------------:|:---------------:|:----------------------:|
|                 {ref}`Ackley <test-functions:ackley>`                  |        M        |       `Ackley()`       |
|  {ref}`Alemazkoor & Meidani (2018) 2D <test-functions:alemazkoor-2d>`  |        2        |    `Alemazkoor2D()`    |
| {ref}`Alemazkoor & Meidani (2018) 20D <test-functions:alemazkoor-20d>` |       20        |   `Alemazkoor20D()`    |
|               {ref}`Borehole <test-functions:borehole>`                |        8        |      `Borehole()`      |
|       {ref}`Cheng and Sandu (2010) 2D <test-functions:cheng2d>`        |        2        |       `Cheng2D`        |
|          {ref}`Coffee Cup Model <test-functions:coffee-cup>`           |        2        |     `CoffeeCup()`      |
|     {ref}`Currin et al. (1988) Sine <test-functions:currin-sine>`      |        1        |     `CurrinSine()`     |
|          {ref}`Damped Cosine <test-functions:damped-cosine>`           |        1        |    `DampedCosine()`    |
|      {ref}`Damped Oscillator <test-functions:damped-oscillator>`       |        7        |  `DampedOscillator()`  |
|                  {ref}`Flood <test-functions:flood>`                   |        8        |       `Flood()`        |
|       {ref}`Forrester et al. (2008) <test-functions:forrester>`        |        1        |   `Forrester2008()`    |
|             {ref}`(1st) Franke <test-functions:franke-1>`              |        2        |      `Franke1()`       |
|             {ref}`(2nd) Franke <test-functions:franke-2>`              |        2        |      `Franke2()`       |
|             {ref}`(3rd) Franke <test-functions:franke-3>`              |        2        |      `Franke3()`       |
|             {ref}`(4th) Franke <test-functions:franke-4>`              |        2        |      `Franke4()`       |
|             {ref}`(5th) Franke <test-functions:franke-5>`              |        2        |      `Franke5()`       |
|             {ref}`(6th) Franke <test-functions:franke-6>`              |        2        |      `Franke6()`       |
|           {ref}`Friedman (6D) <test-functions:friedman-6d>`            |        6        |     `Friedman6D()`     |
|          {ref}`Friedman (10D) <test-functions:friedman-10d>`           |       10        |    `Friedman10D()`     |
|      {ref}`Genz (Corner Peak) <test-functions:genz-corner-peak>`       |        M        |   `GenzCornerPeak()`   |
|     {ref}`Gramacy (2007) 1D Sine <test-functions:gramacy-1d-sine>`     |        1        |   `Gramacy1DSine()`    |
|         {ref}`Higdon (2002) Sine <test-functions:higdon-sine>`         |        1        |     `HigdonSine()`     |
|   {ref}`Holsclaw et al. (2013) Sine <test-functions:holsclaw-sine>`    |        1        |    `HolsclawSine()`    |
| {ref}`Lim et al. (2002) Non-Polynomial <test-functions:lim-non-poly>`  |        2        |     `LimNonPoly()`     |
|     {ref}`Lim et al. (2002) Polynomial <test-functions:lim-poly>`      |        2        |      `LimPoly()`       |
|              {ref}`McLain S1 <test-functions:mclain-s1>`               |        2        |      `McLainS1()`      |
|              {ref}`McLain S2 <test-functions:mclain-s2>`               |        2        |      `McLainS2()`      |
|              {ref}`McLain S3 <test-functions:mclain-s3>`               |        2        |      `McLainS3()`      |
|              {ref}`McLain S4 <test-functions:mclain-s4>`               |        2        |      `McLainS4()`      |
|              {ref}`McLain S5 <test-functions:mclain-s5>`               |        2        |      `McLainS5()`      |
|      {ref}`Oakley & O'Hagan (2002) 1D <test-functions:oakley-1d>`      |        1        |      `Oakley1D()`      |
|            {ref}`OTL Circuit <test-functions:otl-circuit>`             |     6 / 20      |     `OTLCircuit()`     |
|            {ref}`Piston Simulation <test-functions:piston>`            |     7 / 20      |       `Piston()`       |
|              {ref}`Robot Arm <test-functions:robot-arm>`               |        8        |      `RobotArm()`      |
|          {ref}`Solar Cell Model <test-functions:solar-cell>`           |        5        |     `SolarCell()`      |
|                 {ref}`Sulfur <test-functions:sulfur>`                  |        9        |       `Sulfur()`       |
|    {ref}`Undamped Oscillator <test-functions:undamped-oscillator>`     |        6        | `UndampedOscillator()` |
|      {ref}`Webster et al. (1996) 2D <test-functions:webster-2d>`       |        2        |     `Webster2D()`      |
|         {ref}`Welch et al. (1992) <test-functions:welch1992>`          |       20        |     `Welch1992()`      |
|            {ref}`Wing Weight <test-functions:wing-weight>`             |       10        |     `WingWeight()`     |

In a Python terminal, you can list all the available functions relevant
for metamodeling applications using ``list_functions()``
and filter the results using the ``tag`` parameter
(shown below in the HTML format):

```{code-cell} ipython3
:tags: ["output_scroll"]

import uqtestfuns as uqtf

uqtf.list_functions(tag="metamodeling", tablefmt="html")
```

## About metamodeling

In practice, the computational model $\mathcal{M}$ (see {ref}`fundamentals:overview`)
is typically complex.
Since an uncertainty quantification (UQ) analysis usually require numerous
evaluations of $\mathcal{M}$ ($\sim 10^2$---$10^6$ or more!), the process
may become computationally intractable if $\mathcal{M}$ is expensive to evaluate.

To address this challenge, many UQ analyses employ a metamodel (surrogate model).
Constructed on a limited number of model $\mathcal{M}$ evaluations,
such a metamodel should be able to capture the most important aspects
of the input/output mapping while being significantly cheaper to evaluate.
This metamodel can then replace $\mathcal{M}$ in the analysis,
providing a significant reduction in computational cost without
sacrificing the accuracy of the analysis much.

While not a goal of UQ analyse per se, metamodeling is nowadays an indispensable
component of the UQ framework {cite}`Sudret2012, Sudret2017`.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```
