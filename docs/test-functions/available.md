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

The table below lists all the test functions available in UQTestFuns
from the uncertainty quantification (UQ) literature,
regardless of their typical applications.

|                                        Name                                         | Input Dimension |           Constructor           |
|:-----------------------------------------------------------------------------------:|:---------------:|:-------------------------------:|
|                        {ref}`Ackley <test-functions:ackley>`                        |        M        |           `Ackley()`            |
|        {ref}`Alemazkoor & Meidani (2018) 2D <test-functions:alemazkoor-2d>`         |        2        |        `Alemazkoor2D()`         |
|       {ref}`Alemazkoor & Meidani (2018) 20D <test-functions:alemazkoor-20d>`        |       20        |        `Alemazkoor20D()`        |
|                      {ref}`Borehole <test-functions:borehole>`                      |        8        |          `Borehole()`           |
|            {ref}`Bratley et al. (1992) A <test-functions:bratley1992a>`             |        M        |        `Bratley1992a()`         |
|            {ref}`Bratley et al. (1992) B <test-functions:bratley1992b>`             |        M        |        `Bratley1992b()`         |
|            {ref}`Bratley et al. (1992) C <test-functions:bratley1992c>`             |        M        |        `Bratley1992c()`         |
|            {ref}`Bratley et al. (1992) D <test-functions:bratley1992d>`             |        M        |        `Bratley1992d()`         |
|           {ref}`Cantilever Beam (2D) <test-functions:cantilever-beam-2d>`           |        2        |       `CantileverBeam2D `       |
|              {ref}`Cheng and Sandu (2010) 2D <test-functions:cheng2d>`              |        2        |           `Cheng2D `            |
|           {ref}`Circular Pipe Crack <test-functions:circular-pipe-crack>`           |        2        |      `CircularPipeCrack()`      |
|                 {ref}`Coffee Cup Model <test-functions:coffee-cup>`                 |        2        |          `CoffeeCup()`          |
|                   {ref}`Currin Sine <test-functions:currin-sine>`                   |        1        |         `CurrinSine()`          |
|          {ref}`Convex Failure Domain <test-functions:convex-fail-domain>`           |        2        |      `ConvexFailDomain()`       |
|                 {ref}`Damped Cosine <test-functions:damped-cosine>`                 |        1        |        `DampedCosine()`         |
|             {ref}`Damped Oscillator <test-functions:damped-oscillator>`             |        7        |      `DampedOscillator()`       |
| {ref}`Damped Oscillator Reliability <test-functions:damped-oscillator-reliability>` |        8        | `DampedOscillatorReliability()` |
|                         {ref}`Flood <test-functions:flood>`                         |        8        |            `Flood()`            |
|              {ref}`Forrester et al. (2008) <test-functions:forrester>`              |        1        |        `Forrester2008()`        |
|                   {ref}`Four-branch <test-functions:four-branch>`                   |        2        |         `FourBranch()`          |
|                    {ref}`(1st) Franke <test-functions:franke-1>`                    |        2        |           `Franke1()`           |
|                    {ref}`(2nd) Franke <test-functions:franke-2>`                    |        2        |           `Franke2()`           |
|                    {ref}`(3rd) Franke <test-functions:franke-3>`                    |        2        |           `Franke3()`           |
|                    {ref}`(4th) Franke <test-functions:franke-4>`                    |        2        |           `Franke4()`           |
|                    {ref}`(5th) Franke <test-functions:franke-5>`                    |        2        |           `Franke5()`           |
|                    {ref}`(6th) Franke <test-functions:franke-6>`                    |        2        |           `Franke6()`           |
|                  {ref}`Friedman (6D) <test-functions:friedman-6d>`                  |        6        |         `Friedman6D()`          |
|                 {ref}`Friedman (10D) <test-functions:friedman-10d>`                 |       10        |         `Friedman10D()`         |
|                    {ref}`Gayton Hat <test-functions:gayton-hat>`                    |        2        |          `GaytonHat()`          |
|              {ref}`Genz (Continuous) <test-functions:genz-continuous>`              |        M        |       `GenzContinuous()`        |
|             {ref}`Genz (Corner Peak) <test-functions:genz-corner-peak>`             |        M        |       `GenzCornerPeak()`        |
|                {ref}`Genz (Gaussian) <test-functions:genz-gaussian>`                |        M        |        `GenzGaussian()`         |
|             {ref}`Genz (Oscillatory) <test-functions:genz-oscillatory>`             |        M        |       `GenzOscillatory()`       |
|            {ref}`Genz (Product Peak) <test-functions:genz-product-peak>`            |        M        |       `GenzProductPeak()`       |
|           {ref}`Gramacy (2007) 1D Sine <test-functions:gramacy-1d-sine>`            |        1        |        `Gramacy1DSine()`        |
|               {ref}`Hyper-sphere Bound <test-functions:hyper-sphere>`               |        2        |         `HyperSphere()`         |
|                      {ref}`Ishigami <test-functions:ishigami>`                      |        3        |          `Ishigami()`           |
|        {ref}`Lim et al. (2002) Non-Polynomial <test-functions:lim-non-poly>`        |        2        |         `LimNonPoly()`          |
|            {ref}`Lim et al. (2002) Polynomial <test-functions:lim-poly>`            |        2        |           `LimPoly()`           |
|                     {ref}`McLain S1 <test-functions:mclain-s1>`                     |        2        |          `McLainS1()`           |
|                     {ref}`McLain S2 <test-functions:mclain-s2>`                     |        2        |          `McLainS2()`           |
|                     {ref}`McLain S3 <test-functions:mclain-s3>`                     |        2        |          `McLainS3()`           |
|                     {ref}`McLain S4 <test-functions:mclain-s4>`                     |        2        |          `McLainS4()`           |
|                     {ref}`McLain S5 <test-functions:mclain-s5>`                     |        2        |          `McLainS5()`           |
|                    {ref}`Moon (2010) 3D <test-functions:moon3d>`                    |        3        |           `Moon3D()`            |
|               {ref}`Morris et al. (2006) <test-functions:morris2006>`               |        M        |         `Morris2006()`          |
|            {ref}`Oakley & O'Hagan (2002) 1D <test-functions:oakley-1d>`             |        1        |          `Oakley1D()`           |
|                   {ref}`OTL Circuit <test-functions:otl-circuit>`                   |     6 / 20      |         `OTLCircuit()`          |
|                  {ref}`Piston Simulation <test-functions:piston>`                   |     7 / 20      |           `Piston()`            |
|             {ref}`Simple Portfolio Model <test-functions:portfolio-3d>`             |        3        |         `Portfolio3D()`         |
|                     {ref}`Robot Arm <test-functions:robot-arm>`                     |        8        |          `RobotArm()`           |
|              {ref}`RS - Circular Bar <test-functions:rs-circular-bar>`              |        2        |        `RSCircularBar()`        |
|                 {ref}`RS - Quadratic <test-functions:rs-quadratic>`                 |        2        |         `RSQuadratic()`         |
|               {ref}`SaltelliLinear <test-functions:saltelli-linear>`                |        M        |       `SaltelliLinear()`        |
|                      {ref}`Sobol'-G <test-functions:sobol-g>`                       |        M        |           `SobolG()`            |
|                   {ref}`Sobol'-G* <test-functions:sobol-g-star>`                    |        M        |         `SobolGStar()`          |
|                {ref}`Sobol'-Levitan <test-functions:sobol-levitan>`                 |        M        |        `SobolLevitan()`         |
|                 {ref}`Solar Cell Model <test-functions:solar-cell>`                 |        5        |          `SolarCell()`          |
|           {ref}`Speed Reducer Shaft <test-functions:speed-reducer-shaft>`           |        5        |      `SpeedReducerShaft()`      |
|                        {ref}`Sulfur <test-functions:sulfur>`                        |        9        |           `Sulfur()`            |
|           {ref}`Undamped Oscillator <test-functions:undamped-oscillator>`           |        6        |     `UndampedOscillator()`      |
|             {ref}`Webster et al. (1996) 2D <test-functions:webster-2d>`             |        2        |          `Webster2D()`          |
|                {ref}`Welch et al. (1992) <test-functions:welch1992>`                |       20        |          `Welch1992()`          |
|                   {ref}`Wing Weight <test-functions:wing-weight>`                   |       10        |         `WingWeight()`          |

In a Python terminal, you can list all the available functions
along with the corresponding constructor using ``list_functions()``
(shown below in the HTML format):

```{code-cell} ipython3
:tags: ["output_scroll"]

import uqtestfuns as uqtf

uqtf.list_functions(tablefmt="html")
```
