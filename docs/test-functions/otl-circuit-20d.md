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

(test-functions:otl-circuit-20d)=
# Twenty-dimensional OTL Circuit Model from Moon (2010)

```{code-cell} ipython3
import numpy as np
import uqtestfuns as uqtf
```

The `OTLCircuit20D` function is a nominally twenty-dimensional variant of the
{ref}`OTLCircuit <test-functions:otl-circuit>` function introduced in
{cite}`Moon2010` for sensitivity analysis.
It extends the original six-dimensional formulation
by adding 14 inert input variables, none of which affect the output.

For the full description, probabilistic input, and reference results,
refer to the {ref}`OTLCircuit <test-functions:otl-circuit>` page.

```{note}
The 14 additional inert input variables are independent uniform random
variables on $[100, 200]$. Being inert, they do not affect the output
of the function.
```

## Test function instance

To create a default instance of the `OTLCircuit20D` function:

```{code-cell} ipython3
my_testfun = uqtf.OTLCircuit20D()
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
