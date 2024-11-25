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

(test-functions:robot-arm)=
# Robot Arm Function

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The robot arm function is an eight-dimensional, scalar-valued test function
that calculates the distance between a fixed origin and the tip
of a four-segment robot arm.

The function is commonly used in metamodeling exercises; for example,
see {cite}`An2001, Bouhlel2019`. Due to its complexity, the function is
challenging to approximate using polynomials and has therefore been studied 
extensively in the neural network literature {cite}`An2001`.

## Test function instance

To create a default instance of the robot arm test function:

```{code-cell} ipython3
my_testfun = uqtf.RobotArm()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

Consider a four-segment robot arm, with its shoulder fixed at the origin
in the $(x, y)$-plane.
The segments have lengths $L_1, L_2, L_3$ and $L_4$.
The position of the end of the robot arm is given by:

$$
\begin{aligned}
x_* (\boldsymbol{x}) & = \sum_{i = 1}^4 L_i \, \cos{\left( \sum_{j = 1}^i \theta_j \right)} \\
y_* (\boldsymbol{x}) & = \sum_{i = 1}^4 L_i \, \sin{\left( \sum_{j = 1}^i \theta_j \right)},
\end{aligned}
$$

where:

- $\theta_1$ is the angle formed by the first segment and the horizontal axis, and
- $\theta_2, \theta_3, \theta_4$ are the angles formed by consecutive segments
  with the previous segments, i.e., the 2nd and 1st, 3rd and 2nd,
  and 4th and 3rd segments, respectively.

The robot arm function computes the Euclidean distance between the tip
of the robot arm and the fixed origin, expressed as[^location]

$$
\mathcal{M}(\boldsymbol{x}) = \sqrt{x_*^2(\boldsymbol{x}) + y_*^2(\boldsymbol{x})},
$$

where $\boldsymbol{x} = \left( L_1, L_2, L_3, L_4, \theta_1, \theta_2, \theta_3, \theta_4 \right)$
is the eight-dimensional vector of input variables further defined below.

## Probabilistic input

The probabilistic input model for the robot arm function consists of eight
independent uniform random variables with the ranges shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.prob_input)
```

## Reference results

This section provides several reference results of typical UQ analyses involving
the test function.

### Sample histogram

Shown below is the histogram of the output based on $1'000'000$ random points:

```{code-cell} ipython3
:tags: [hide-input]

my_testfun.prob_input.reset_rng(42)
xx_test = my_testfun.prob_input.get_sample(1000000)
yy_test = my_testfun(xx_test)

plt.hist(yy_test, bins="auto", color="#8da0cb");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel("$\mathcal{M}(\mathbf{X})$");
plt.gcf().set_dpi(150);
```

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: see Section 6.2, pp. 600-601 in {cite}`An2001`.