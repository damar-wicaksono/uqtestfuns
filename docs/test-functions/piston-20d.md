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

(test-functions:piston-20d)=
# Twenty-dimensional Piston Simulation Model from Moon (2010)

```{code-cell} ipython3
import numpy as np
import uqtestfuns as uqtf
```

The Piston20D function is a nominally twenty-dimensional variant of the
{ref}`Piston <test-functions:piston>` function introduced in
{cite}`Moon2010` for sensitivity analysis. It extends the original
seven-dimensional formulation by adding 13 inert input variables, none of
which affect the output.

For the full description, probabilistic input, and reference results,
refer to the {ref}`Piston <test-functions:piston>` page.

```{note}
The 13 additional inert input variables are independent uniform random
variables on $[100, 200]$. Being inert, they do not affect the output
of the function.
```

## Test function instance

To create a default instance of the Piston20D function:

```{code-cell} ipython3
my_testfun = uqtf.Piston20D()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Probabilistic input

The default input specification contains twenty independent
uniform random variables with ranges shown in the table below.

```{code-cell} ipython3
:tags: [hide-input, output_scroll]

print(my_testfun.prob_input)
```

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```
