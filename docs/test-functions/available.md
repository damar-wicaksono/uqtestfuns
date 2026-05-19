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

|              Name               | Input Dimension |                                           Description                                            |
|:-------------------------------:|:---------------:|:------------------------------------------------------------------------------------------------:|
|           ``Ackley``            |        M        |                           {ref}`Ackley (1987) <test-functions:ackley>`                           |
|        ``Alemazkoor2D``         |        2        |              {ref}`Alemazkoor and Meidani (2018) 2D <test-functions:alemazkoor-2d>`              |
|        ``Alemazkoor20D``        |       20        |             {ref}`Alemazkoor and Meidani (2018) 20D <test-functions:alemazkoor-20d>`             |
|          ``Borehole``           |        8        |                            {ref}`Borehole <test-functions:borehole>`                             |
|        ``Bratley1992a``         |        M        |                    {ref}`Bratley et al. (1992) A <test-functions:bratley-a>`                     |
|        ``Bratley1992b``         |        M        |                    {ref}`Bratley et al. (1992) B <test-functions:bratley-b>`                     |
|        ``Bratley1992c``         |        M        |                    {ref}`Bratley et al. (1992) C <test-functions:bratley-c>`                     |
|        ``Bratley1992d``         |        M        |                    {ref}`Bratley et al. (1992) D <test-functions:bratley-d>`                     |
|      ``CantileverBeam2D``       |        2        | {ref}` Rajashekhar and Ellingwood (1993) Cantilever Beam 2D <test-functions:cantilever-beam-2d>` |
|           ``Cheng2D``           |        2        |                    {ref}`Cheng and Sandu (2010) 2D <test-functions:cheng2d>`                     |
|          ``CoffeeCup``          |        2        |                {ref}`Tennøe et al. (2018) Coffee Cup <test-functions:coffee-cup>`                |
|      ``ConvexFailDomain``       |        2        |                 {ref}`Convex Failure Domain <test-functions:convex-fail-domain>`                 |
|         ``CurrinSine``          |        1        |                  {ref}`Currin et al. (1988) Sine <test-functions:currin-sine>`                   |
|        ``DampedCosine``         |        1        |            {ref}`Santner et al. (2018) Damped Cosine <test-functions:damped-cosine>`             |
|      ``DampedOscillator``       |        7        |                   {ref}`Damped Oscillator <test-functions:damped-oscillator>`                    |
| ``DampedOscillatorReliability`` |        8        |       {ref}`Damped Oscillator Reliability <test-functions:damped-oscillator-reliability>`        |
|           ``Dette8D``           |        3        |                 {ref}`Dette and Pepelyshev (2010) 8D <test-functions:dette-8d>`                  |
|         ``DetteCurved``         |        3        |             {ref}`Dette and Pepelyshev (2010) Curved <test-functions:dette-curved>`              |
|          ``DetteExp``           |        3        |            {ref}`Dette and Pepelyshev (2010) Exponential <test-functions:dette-exp>`             |
|            ``Flood``            |        8        |                  {ref}`Iooss and Lemaître (2015) Flood <test-functions:flood>`                   |
|         ``Forrester1D``         |        1        |                 {ref}`Forrester et al. (2008) 1D <test-functions:forrester-1d>`                  |
|         ``FourBranch``          |        2        |           {ref}`Katsuki and Frangopol (1994) Four-Branch <test-functions:four-branch>`           |
|           ``Franke1``           |        2        |                        {ref}`Franke (1979) 1st <test-functions:franke-1>`                        |
|           ``Franke2``           |        2        |                        {ref}`Franke (1979) 2nd <test-functions:franke-2>`                        |
|           ``Franke3``           |        2        |                        {ref}`Franke (1979) 3rd <test-functions:franke-3>`                        |
|           ``Franke4``           |        2        |                        {ref}`Franke (1979) 4th <test-functions:franke-4>`                        |
|           ``Franke5``           |        2        |                        {ref}`Franke (1979) 5th <test-functions:franke-5>`                        |
|           ``Franke6``           |        2        |                        {ref}`Franke (1979) 6th <test-functions:franke-6>`                        |
|         ``Friedman6D``          |        6        |                  {ref}`Friedman et al. (1983) 6D <test-functions:friedman-6d>`                   |
|         ``Friedman10D``         |       10        |                     {ref}`Friedman (1991) 10D <test-functions:friedman-10d>`                     |
|          ``GaytonHat``          |        2        |                {ref}`Echard et al. (2013) Gayton Hat <test-functions:gayton-hat>`                |
|       ``GenzContinuous``        |        M        |                  {ref}`Genz (1984) Continuous <test-functions:genz-continuous>`                  |
|       ``GenzCornerPeak``        |        M        |                 {ref}`Genz (1984) Corner Peak <test-functions:genz-corner-peak>`                 |
|      ``GenzDiscontinuous``      |        M        |               {ref}`Genz (1984) Discontinuous <test-functions:genz-discontinuous>`               |
|        ``GenzGaussian``         |        M        |                    {ref}`Genz (1984) Gaussian <test-functions:genz-gaussian>`                    |
|       ``GenzOscillatory``       |        M        |                 {ref}`Genz (1984) Oscillatory <test-functions:genz-oscillatory>`                 |
|       ``GenzProductPeak``       |        M        |                {ref}`Genz (1984) Product Peak <test-functions:genz-product-peak>`                |
|         ``GramacySine``         |        1        |                     {ref}`Gramacy (2007) Sine <test-functions:gramacy-sine>`                     |
|         ``HigdonSine``          |        1        |                      {ref}`Higdon (2002) Sine <test-functions:higdon-sine>`                      |
|        ``HolsclawSine``         |        1        |                {ref}`Holsclaw et al. (2013) Sine <test-functions:holsclaw-sine>`                 |
|         ``HyperSphere``         |        2        |                     {ref}`Hyper-sphere Bound <test-functions:hyper-sphere>`                      |
|          ``Ishigami``           |        3        |                            {ref}`Ishigami <test-functions:ishigami>`                             |
|         ``LimNonPoly``          |        2        |              {ref}`Lim et al. (2002) Non-Polynomial <test-functions:lim-non-poly>`               |
|           ``LimPoly``           |        2        |                  {ref}`Lim et al. (2002) Polynomial <test-functions:lim-poly>`                   |
|     ``LinkletterDecCoeffs``     |       10        |  {ref}`Linkletter et al. (2006) Decreasing Coefficients <test-functions:linkletter-dec-coeffs>`  |
|       ``LinkletterInert``       |       10        |             {ref}`Linkletter et al. (2006) Inert <test-functions:linkletter-inert>`              |
|      ``LinkletterLinear``       |       10        |            {ref}`Linkletter et al. (2006) Linear <test-functions:linkletter-linear>`             |
|       ``LinkletterSine``        |       10        |              {ref}`Linkletter et al. (2006) Sine <test-functions:linkletter-sine>`               |
|          ``McLainS1``           |        2        |                        {ref}`McLain (1974) S1 <test-functions:mclain-s1>`                        |
|          ``McLainS2``           |        2        |                        {ref}`McLain (1974) S2 <test-functions:mclain-s2>`                        |
|          ``McLainS3``           |        2        |                        {ref}`McLain (1974) S3 <test-functions:mclain-s3>`                        |
|          ``McLainS4``           |        2        |                        {ref}`McLain (1974) S4 <test-functions:mclain-s4>`                        |
|          ``McLainS5``           |        2        |                        {ref}`McLain (1974) S5 <test-functions:mclain-s5>`                        |
|           ``Moon3D``            |        3        |                          {ref}`Moon (2010) 3D <test-functions:moon3d>`                           |
|           ``MorrisM``           |        M        |                    {ref}`Morris et al. (2006) M <test-functions:morris2006>`                     |
|          ``Oakley1D``           |        1        |                  {ref}`Oakley and O'Hagan (2002) 1D <test-functions:oakley-1d>`                  |
|         ``OTLCircuit``          |        6        |           {ref}`Ben-Ari and Steinberg (2007) OTL Circuit <test-functions:otl-circuit>`           |
|        ``OTLCircuit20D``        |       20        |               {ref}`Moon (2010) OTL Circuit 20D <test-functions:otl-circuit-20d>`                |
|           ``Piston``            |        7        |                {ref}`Ben-Ari and Steinberg (2007) Piston <test-functions:piston>`                |
|          ``Piston20D``          |       20        |                      {ref}`Moon (2010) Piston 20D <test-functions:piston>`                       |
|         ``Portfolio3D``         |        3        |             {ref}`Saltelli et al. (2004) Portfolio 3D <test-functions:portfolio-3d>`             |
|          ``RobotArm``           |        8        |                  {ref}`An and Owen (2001) Robot Arm <test-functions:robot-arm>`                  |
|         ``Rosenbrock``          |        M        |                       {ref}`Rosenbrock (1960) <test-functions:rosenbrock>`                       |
|        ``RSCircularBar``        |        2        |           {ref}`Verma et al. (2015) RS Circular Bar <test-functions:rs-circular-bar>`            |
|     ``RSCircularPipeCrack``     |        2        |    {ref}`Verma et al. (2015) RS Circular Pipe Crack <test-functions:rs-circular-pipe-crack>`     |
|         ``RSQuadratic``         |        2        |                 {ref}`Waarts (2000) RS Quadratic <test-functions:rs-quadratic>`                  |
|       ``SaltelliLinear``        |        M        |              {ref}`Saltelli et al. (2008) Linear <test-functions:saltelli-linear>`               |
|           ``SobolG``            |        M        |                   {ref}`Saltelli and Sobol' (1995) G <test-functions:sobol-g>`                   |
|         ``SobolGStar``          |        M        |                  {ref}`Saltelli et al. (2010) G* <test-functions:sobol-g-star>`                  |
|        ``SobolLevitan``         |        M        |                   {ref}`Sobol'-Levitan (1999) <test-functions:sobol-levitan>`                    |
|          ``SolarCell``          |        5        |             {ref}`Constantine et al. (2015) Solar Cell <test-functions:solar-cell>`              |
|      ``SpeedReducerShaft``      |        5        |                 {ref}`Speed Reducer Shaft <test-functions:speed-reducer-shaft>`                  |
|           ``Sulfur``            |        9        |                   {ref}`Charlson et al. (1992) Sulfur <test-functions:sulfur>`                   |
|     ``UndampedOscillator``      |        6        |       {ref}`Gayton et al. (2003) Undamped Oscillator <test-functions:undamped-oscillator>`       |
|          ``Webster2D``          |        2        |                   {ref}`Webster et al. (1996) 2D <test-functions:webster-2d>`                    |
|           ``Welch2D``           |       20        |                    {ref}`Welch et al. (1992) 20D <test-functions:welch1992>`                     |
|         ``WingWeight``          |       10        |             {ref}`Forrester et al. (2008) Wing Weight <test-functions:wing-weight>`              |

In a Python terminal, you can list all the available functions
along with the corresponding constructor using ``list_functions()``
(shown below in the HTML format):

```{code-cell} ipython3
:tags: ["output_scroll"]

import uqtestfuns as uqtf

uqtf.list_functions(tablefmt="html")
```
