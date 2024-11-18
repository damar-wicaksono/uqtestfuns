(prob-input:available-marginal-distributions)=
# Available One-Dimensional Marginal Distributions

The table below lists all the available one-dimensional marginal distribution
types used to construct ``Marginal`` instances.
``Marginal`` instances are used to represent the one-dimensional marginals
of a (possibly, multivariate) probabilistic input model.

|                                        Name                                         | Keyword value for `distribution` |                     Notation                      |             Support              | Number of parameters |
|:-----------------------------------------------------------------------------------:|:--------------------------------:|:-------------------------------------------------:|:--------------------------------:|:--------------------:|
|                {ref}`Beta <prob-input:marginal-distributions:beta>`                 |             `"beta"`             |       $\mathrm{Beta}(\alpha, \beta, a, b)$        | $[a, b], \; a, b \in \mathbb{R}$ |          4           |
|         {ref}`Exponential <prob-input:marginal-distributions:exponential>`          |         `"exponential"`          |              $\mathcal{E}(\lambda)$               |          $[0, \infty)$           |          1           |
|           {ref}`Gumbel (max.) <prob-input:marginal-distributions:gumbel>`           |            `"gumbel"`            |           $\mathrm{Gumbel}(\mu, \beta)$           |       $(-\infty, \infty)$        |          2           |
|         {ref}`Logit-Normal <prob-input:marginal-distributions:logitnormal>`         |         `"logitnormal"`          |    $\mathcal{N}_{\mathrm{logit}}(\mu, \sigma)$    |             $(0, 1)$             |          2           |
|           {ref}`Log-Normal <prob-input:marginal-distributions:lognormal>`           |          `"lognormal"`           |    $\mathcal{N}_{\mathrm{log}} (\mu, \sigma)$     |          $(0, \infty)$           |          2           |
|         {ref}`Normal (Gaussian) <prob-input:marginal-distributions:normal>`         |            `"normal"`            |            $\mathcal{N}(\mu, \sigma)$             |       $(-\infty, \infty)$        |          2           |
|          {ref}`Triangular <prob-input:marginal-distributions:triangular>`           |          `"triangular"`          |             $\mathcal{T}_r(a, b, c)$              | $[a, b], \; a, b \in \mathbb{R}$ |          3           |
|   {ref}`Truncated Gumbel (max.) <prob-input:marginal-distributions:trunc-gumbel>`   |         `"trunc-gumbel"`         | $\mathrm{Gumbel}_{\mathrm{Tr}}(\mu, \beta, a, b)$ | $[a, b], \; a, b \in \mathbb{R}$ |          4           |
| {ref}`Truncated Normal (Gaussian) <prob-input:marginal-distributions:trunc-normal>` |         `"trunc-normal"`         |  $\mathcal{N}_{\mathrm{Tr}}(\mu, \sigma, a, b)$   | $[a, b], \; a, b \in \mathbb{R}$ |          4           |
|             {ref}`Uniform <prob-input:marginal-distributions:uniform>`              |           `"uniform"`            |                $\mathcal{U}(a, b)$                | $[a, b], \; a, b \in \mathbb{R}$ |          2           |
