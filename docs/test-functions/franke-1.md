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

(test-functions:franke-1)=
# (First) Franke Function

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The (first) Franke function is a two-dimensional scalar-valued function.
The function was first introduced in {cite}`Franke1979` in the context of
interpolation problem and was used in {cite}`Haaland2011` in the context of
metamodeling.

The Franke's original report {cite}`Franke1979` contains in total
six two-dimensional test functions.
The first function that appeared is commonly known simply as
the "Franke function".

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable

my_fun = uqtf.Franke1()

# --- Create 2D data
xx_1d = np.linspace(0.0, 1.0, 1000)[:, np.newaxis]
mesh_2d = np.meshgrid(xx_1d, xx_1d)
xx_2d = np.array(mesh_2d).T.reshape(-1, 2)
yy_2d = my_fun(xx_2d)

# --- Create two-dimensional plots
fig = plt.figure(figsize=(10, 5))

# Surface
axs_1 = plt.subplot(121, projection='3d')
axs_1.plot_surface(
    mesh_2d[0],
    mesh_2d[1],
    yy_2d.reshape(1000,1000),
    linewidth=0,
    cmap="plasma",
    antialiased=False,
    alpha=0.5
)
axs_1.set_xlabel("$x_1$", fontsize=14)
axs_1.set_ylabel("$x_2$", fontsize=14)
axs_1.set_zlabel("$\mathcal{M}(x_1, x_2)$", fontsize=14)
axs_1.set_title("Surface plot of (1st) Franke", fontsize=14)

# Contour
axs_2 = plt.subplot(122)
cf = axs_2.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(1000, 1000), cmap="plasma"
)
axs_2.set_xlabel("$x_1$", fontsize=14)
axs_2.set_ylabel("$x_2$", fontsize=14)
axs_2.set_title("Contour plot of (1st) Franke", fontsize=14)
divider = make_axes_locatable(axs_2)
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(cf, cax=cax, orientation='vertical')
axs_2.axis('scaled')

fig.tight_layout(pad=3.0)
plt.gcf().set_dpi(75);
```

As shown in the plots above, the surface consists of two Gaussian peaks and
a Gaussian dip on a surface sloping down toward the upper right boundary
(i.e., $[1.0, 1.0]$).

## Test function instance

To create a default instance of the Franke function:

```{code-cell} ipython3
my_testfun = uqtf.Franke1()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The Franke function is defined as follows:

$$
\begin{align}
	\mathcal{M}(\boldsymbol{x}) = & 0.75 \exp{\left( -0.25 \left( (x_1 - 2)^2 + (x_2 - 2)^2 \right) \right) } \\
                                  & + 0.75 \exp{\left( -1.00 \left( \frac{(x_1 + 1)^2}{49} + \frac{(x_2 + 1)^2}{10} \right) \right)} \\
								  & + 0.50 \exp{\left( -0.25 \left( (x_1 - 7)^2 + (x_2 - 3)^2 \right) \right)} \\
								  & - 0.20 \exp{\left( -1.00 \left( (x_1 - 4)^2 + (x_2 - 7)^2 \right) \right)} \\
\end{align}
$$
where $\boldsymbol{x} = \{ x_1, x_2 \}$
is the two-dimensional vector of input variables further defined below.

## Probabilistic input

Based on {cite}`Franke1979`, the probabilistic input model
for the function consists of two independent random variables as shown below.

```{code-cell} ipython3
my_testfun.prob_input
```

## Reference results

This section provides several reference results of typical UQ analyses involving
the test function.

### Sample histogram

Shown below is the histogram of the output based on $100'000$ random points:

```{code-cell} ipython3
:tags: [hide-input]

xx_test = my_testfun.prob_input.get_sample(100000)
yy_test = my_testfun(xx_test)

plt.hist(yy_test, bins="auto", color="#8da0cb");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel("$\mathcal{M}(\mathbf{X})$");
plt.gcf().set_dpi(150);
```

## References

```{bibliography}
:style: plain
:filter: docname in docnames
```