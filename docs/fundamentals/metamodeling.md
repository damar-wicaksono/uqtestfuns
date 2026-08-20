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

The table below lists the available test functions typically used
in the comparison of metamodeling approaches.

|          Name           | Input Dimension |                                          Description                                           |
|:-----------------------:|:---------------:|:----------------------------------------------------------------------------------------------:|
|       ``Ackley``        |        M        |                          {ref}`Ackley (1987) <test-functions:ackley>`                          |
|    ``Alemazkoor2D``     |        2        |              {ref}`Alemazkoor & Meidani (2018) 2D <test-functions:alemazkoor-2d>`              |
|    ``Alemazkoor20D``    |       20        |             {ref}`Alemazkoor & Meidani (2018) 20D <test-functions:alemazkoor-20d>`             |
|      ``Borehole``       |        8        |                           {ref}`Borehole <test-functions:borehole>`                            |
|       ``Cheng2D``       |        2        |                   {ref}`Cheng and Sandu (2010) 2D <test-functions:cheng2d>`                    |
|      ``CoffeeCup``      |        2        |                      {ref}`Coffee Cup Model <test-functions:coffee-cup>`                       |
|     ``CurrinSine``      |        1        |                 {ref}`Currin et al. (1988) Sine <test-functions:currin-sine>`                  |
|    ``DampedCosine``     |        1        |                      {ref}`Damped Cosine <test-functions:damped-cosine>`                       |
|  ``DampedOscillator``   |        7        |                  {ref}`Damped Oscillator <test-functions:damped-oscillator>`                   |
|       ``Dette8D``       |        3        |                 {ref}`Dette & Pepelyshev (2010) 8D <test-functions:dette-8d>`                  |
|     ``DetteCurved``     |        3        |             {ref}`Dette & Pepelyshev (2010) Curved <test-functions:dette-curved>`              |
|      ``DetteExp``       |        3        |            {ref}`Dette & Pepelyshev (2010) Exponential <test-functions:dette-exp>`             |
|        ``Flood``        |        8        |                              {ref}`Flood <test-functions:flood>`                               |
|     ``Forrester1D``     |        1        |                {ref}`Forrester et al. (2008) 1D <test-functions:forrester-1d>`                 |
|       ``Franke1``       |        2        |                         {ref}`(1st) Franke <test-functions:franke-1>`                          |
|       ``Franke2``       |        2        |                         {ref}`(2nd) Franke <test-functions:franke-2>`                          |
|       ``Franke3``       |        2        |                         {ref}`(3rd) Franke <test-functions:franke-3>`                          |
|       ``Franke4``       |        2        |                         {ref}`(4th) Franke <test-functions:franke-4>`                          |
|       ``Franke5``       |        2        |                         {ref}`(5th) Franke <test-functions:franke-5>`                          |
|       ``Franke6``       |        2        |                         {ref}`(6th) Franke <test-functions:franke-6>`                          |
|     ``Friedman6D``      |        6        |                       {ref}`Friedman (6D) <test-functions:friedman-6d>`                        |
|     ``Friedman10D``     |       10        |                      {ref}`Friedman (10D) <test-functions:friedman-10d>`                       |
|   ``GenzCornerPeak``    |        M        |                  {ref}`Genz (Corner Peak) <test-functions:genz-corner-peak>`                   |
|     ``GramacySine``     |        1        |                    {ref}`Gramacy (2007) Sine <test-functions:gramacy-sine>`                    |
|     ``HigdonSine``      |        1        |                     {ref}`Higdon (2002) Sine <test-functions:higdon-sine>`                     |
|    ``HolsclawSine``     |        1        |               {ref}`Holsclaw et al. (2013) Sine <test-functions:holsclaw-sine>`                |
|     ``LimNonPoly``      |        2        |             {ref}`Lim et al. (2002) Non-Polynomial <test-functions:lim-non-poly>`              |
|       ``LimPoly``       |        2        |                 {ref}`Lim et al. (2002) Polynomial <test-functions:lim-poly>`                  |
| ``LinkletterDecCoeffs`` |       10        | {ref}`Linkletter et al. (2006) Decreasing Coefficients <test-functions:linkletter-dec-coeffs>` |
|  ``LinkletterLinear``   |       10        |           {ref}`Linkletter et al. (2006) Linear <test-functions:linkletter-linear>`            |
|   ``LinkletterSine``    |       10        |             {ref}`Linkletter et al. (2006) Sine <test-functions:linkletter-sine>`              |
|      ``McLainS1``       |        2        |                          {ref}`McLain S1 <test-functions:mclain-s1>`                           |
|      ``McLainS2``       |        2        |                          {ref}`McLain S2 <test-functions:mclain-s2>`                           |
|      ``McLainS3``       |        2        |                          {ref}`McLain S3 <test-functions:mclain-s3>`                           |
|      ``McLainS4``       |        2        |                          {ref}`McLain S4 <test-functions:mclain-s4>`                           |
|      ``McLainS5``       |        2        |                          {ref}`McLain S5 <test-functions:mclain-s5>`                           |
|      ``Oakley1D``       |        1        |                  {ref}`Oakley & O'Hagan (2002) 1D <test-functions:oakley-1d>`                  |
|     ``OTLCircuit``      |        6        |                      {ref}`OTL Circuit (6D) <test-functions:otl-circuit>`                      |
|       ``Piston``        |        7        |                     {ref}`Piston Simulation (7D) <test-functions:piston>`                      |
|      ``RobotArm``       |        8        |                 {ref}`An and Owen (2001) Robot Arm <test-functions:robot-arm>`                 |
|     ``Rosenbrock``      |        M        |                         {ref}`Rosenbrock <test-functions:rosenbrock>`                          |
|      ``SolarCell``      |        5        |            {ref}`Constantine et al. (2015) Solar Cell <test-functions:solar-cell>`             |
|       ``Sulfur``        |        9        |                  {ref}`Charlson et al. (1992) Sulfur <test-functions:sulfur>`                  |
| ``UndampedOscillator``  |        6        |                {ref}`Undamped Oscillator <test-functions:undamped-oscillator>`                 |
|      ``Webster2D``      |        2        |                  {ref}`Webster et al. (1996) 2D <test-functions:webster-2d>`                   |
|      ``Welch20D``       |       20        |                   {ref}`Welch et al. (1992) 20D <test-functions:welch1992>`                    |
|     ``WingWeight``      |       10        |                        {ref}`Wing Weight <test-functions:wing-weight>`                         |

In a Python terminal, you can list all the available functions relevant
for metamodeling applications using ``list_functions()``
and filter the results using the ``tag`` parameter:

```python
import uqtestfuns as uqtf

uqtf.list_functions(tag="metamodeling")
```

## About metamodeling

In practice, the computational model $\mathcal{M}$ (see {ref}`fundamentals:overview`)
is typically complex.
Since an uncertainty quantification (UQ) analysis usually requires many
evaluations of $\mathcal{M}$ ($\sim 10^2$---$10^6$ or more!), the process
may become computationally intractable if $\mathcal{M}$ is expensive to evaluate.

To address this challenge, many UQ analyses turn to **metamodeling**: the
activity of constructing a metamodel (or surrogate model) from a limited
number of evaluations of the full computational model $\mathcal{M}$.
Such a metamodel should be able to capture the most important aspects
of the input/output mapping while being significantly cheaper to evaluate.
It can then replace $\mathcal{M}$ in the analysis,
providing a significant reduction in computational cost without
significantly sacrificing the accuracy of the analysis.

While not a goal of UQ analysis per se, metamodeling is nowadays an indispensable
component of the UQ framework {cite}`Sudret2012, Sudret2017`.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```
