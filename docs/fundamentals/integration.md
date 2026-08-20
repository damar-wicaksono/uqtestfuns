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

(fundamentals:integration)=
# Test Functions for Numerical Integration

The table below lists the available test functions typically used
in the testing and comparison of numerical integration method.

|          Name          | Input Dimension |                            Description                             |
|:----------------------:|:---------------:|:------------------------------------------------------------------:|
|      ``BratleyA``      |        M        |     {ref}`Bratley et al. (1992) A <test-functions:bratley-a>`      |
|      ``BratleyB``      |        M        |     {ref}`Bratley et al. (1992) B <test-functions:bratley-b>`      |
|      ``BratleyC``      |        M        |     {ref}`Bratley et al. (1992) C <test-functions:bratley-c>`      |
|      ``BratleyD``      |        M        |     {ref}`Bratley et al. (1992) D <test-functions:bratley-d>`      |
|   ``GenzContinuous``   |        M        |     {ref}`Genz (Continuous) <test-functions:genz-continuous>`      |
|   ``GenzCornerPeak``   |        M        |    {ref}`Genz (Corner Peak) <test-functions:genz-corner-peak>`     |
| ``GenzDiscontinuous``  |        M        |  {ref}`Genz (Discontinuous) <test-functions:genz-discontinuous>`   |
|    ``GenzGaussian``    |        M        |       {ref}`Genz (Gaussian) <test-functions:genz-gaussian>`        |
|  ``GenzOscillatory``   |        M        |    {ref}`Genz (Oscillatory) <test-functions:genz-oscillatory>`     |
|  ``GenzProductPeak``   |        M        |   {ref}`Genz (Product Peak) <test-functions:genz-product-peak>`    |
|       ``SobolG``       |        M        |              {ref}`Sobol'-G <test-functions:sobol-g>`              |
|      ``Welch20D``      |       20        |     {ref}`Welch et al. (1992) 20D <test-functions:welch1992>`      |

In a Python terminal, you can list all the available functions relevant
for integration applications using ``list_functions()``
and filter the results using the ``tag`` parameter:

```python
import uqtestfuns as uqtf

uqtf.list_functions(tag="integration")
```

## About integration

Two of the other analyses in this framework are themselves integration
problems in disguise. The failure probability $P_f$ in
{ref}`reliability analysis <fundamentals:reliability>` is defined as an
integral of the joint {term}`PDF` over the (implicitly defined) failure domain,
and variance-based sensitivity measures in
{ref}`sensitivity analysis <fundamentals:sensitivity>` are moments of
$\mathcal{M}$ computed as integrals over the input distribution
{cite}`Sobol1993`. Framing these as integration problems opens them up to a
common set of numerical techniques, from classical quadrature to Monte
Carlo and its variants.

What sets UQTestFuns' integration test functions apart from the rest of the
collection is that their integrals over the input domain are (usually) known
analytically. This makes them suited for benchmarking the accuracy of a
numerical integration scheme directly, rather than only comparing methods
against each other {cite}`Genz1984`.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```
