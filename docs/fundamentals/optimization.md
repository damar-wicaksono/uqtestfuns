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

(fundamentals:optimization)=
# Test Functions for Optimization

The table below lists the available test functions typically used
in the comparison of global optimization methods.

|      Name       | Input Dimension |                              Description                              |
|:---------------:|:---------------:|:---------------------------------------------------------------------:|
|   ``Ackley``    |        M        |             {ref}`Ackley (1987) <test-functions:ackley>`              |
| ``Forrester1D`` |        1        |    {ref}`Forrester et al. (2008) 1D <test-functions:forrester-1d>`    |
| ``Rosenbrock``  |        M        |             {ref}`Rosenbrock <test-functions:rosenbrock>`             |

In a Python terminal, you can list all the available functions relevant
for optimization applications using ``list_functions()``
and filter the results using the ``tag`` parameter:

```python
import uqtestfuns as uqtf

uqtf.list_functions(tag="optimization")
```

## About optimization

Unlike reliability, sensitivity, and integration, optimization test
functions don't reduce to the same probabilistic framework.
As {ref}`fundamentals:overview` notes, they're included "for completeness"
rather than as a core UQ analysis[^opt-scope1].
UQTestFuns still wraps them in the same `ProbInput`/`Marginal` machinery
as every other function, but here the "distribution"
typically just encodes the search space's box constraints (a uniform range),
not genuine input uncertainty[^opt-scope2].

The closest connection to the rest of the framework is with metamodeling.
What makes a good optimization test function, a deliberately deceptive
landscape with multiple local optima or a narrow curved valley, is also
what makes a good metamodeling stress test: a surrogate has to capture the
same difficult features an optimizer has to navigate.
For example, Ackley's {cite}`Ackley1987` function
and Rosenbrock's {cite}`Rosenbrock1960` function
are both tagged for metamodeling and optimization in UQTestFuns.
The connection runs deeper still:
fitting many metamodeling techniques is itself an optimization problem,
such as tuning a Gaussian process's kernel hyperparameters by maximizing the
likelihood. Optimization is thus perhaps quietly embedded in UQ analyses
far more often than the "for completeness" framing above might suggest.

[^opt-scope1]: Specifically, these are classical, deterministic global
optimization benchmarks. Reliability-based design optimization and other
forms of optimization under uncertainty are a related but distinct topic,
not currently covered by UQTestFuns.

[^opt-scope2]: In optimization under uncertainty problems, the input
(or part of it) is genuinely probabilistic,
unlike the box-constraint search spaces used here.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```
