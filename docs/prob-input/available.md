# Available Univariate Distributions

The table below lists all the available univariate distribution type used
to construct ``UnivariateInput`` instance.

|                                         Name                                          |     Keyword      |                      Notation                      |              Support              | Number of parameters |
|:-------------------------------------------------------------------------------------:|:----------------:|:--------------------------------------------------:|:---------------------------------:|:--------------------:|
|                {ref}`Beta <prob-input:univariate-distributions:beta>`                 |     `"beta"`     |                                                    | $[a, b], \; a, b \in \mathbb{R}$  |          4           |
|           {ref}`Gumbel (max.) <prob-input:univariate-distributions:gumbel>`           |    `"gumbel"`    |           $\mathrm{Gumbel}(\mu, \beta)$            |        $(-\infty, \infty)$        |          2           |
|         {ref}`Logit-Normal <prob-input:univariate-distributions:logitnormal>`         | `"logitnormal"`  |                                                    |                                   |                      |
|           {ref}`Log-Normal <prob-input:univariate-distributions:lognormal>`           |  `"lognormal"`   |                                                    |                                   |                      |
|         {ref}`Normal (Gaussian) <prob-input:univariate-distributions:normal>`         |    `"normal"`    |             $\mathcal{N}(\mu, \sigma)$             |        $(-\infty, \infty)$        |          2           |
|          {ref}`Triangular <prob-input:univariate-distributions:triangular>`           |  `"triangular"`  |    $X \sim \mathcal{T}_r (a, b, c)$                | $[a, b], \; a, b \in \mathbb{R}$  |          3           |
|   {ref}`Truncated Gumbel (max.) <prob-input:univariate-distributions:trunc-gumbel>`   | `"trunc-gumbel"` | $\mathrm{Gumbel}_{\mathrm{Tr}} (\mu, \beta, a, b)$ | $[a, b], \; a, b \in \mathbb{R}$  |          4           |
| {ref}`Truncated Normal (Gaussian) <prob-input:univariate-distributions:trunc-normal>` | `"trunc-normal"` |  $\mathcal{N}_{\mathrm{Tr}} (\mu, \sigma, a, b)$   | $[a, b], \; a, b \in \mathbb{R}$  |          4           |
|             {ref}`Uniform <prob-input:univariate-distributions:uniform>`              |   `"uniform"`    |                $\mathcal{U}(a, b)$                 | $[a, b], \; a, b \in \mathbb{R}$  |          2           |
