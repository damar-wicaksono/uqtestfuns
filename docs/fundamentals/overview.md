(fundamentals:overview)=
# Uncertainty Quantification Framework

```{margin}
For a gentler, example-driven introduction to what UQ test functions are,
see {ref}`About UQ Test Functions <getting-started:about-uq-test-functions>`.
```

Consider a computational model represented as an $M$-dimensional
black-box function:

$$
\mathcal{M}: \boldsymbol{x} \in \mathcal{D}_{\boldsymbol{X}} \subseteq \mathbb{R}^M \to \boldsymbol{y} = \mathcal{M}(\boldsymbol{x}) \subseteq \mathbb{R}^P,
$$

where $\mathcal{D}_{\boldsymbol{X}}$, $\boldsymbol{y}$, $P$ denote
the input domain, the quantity of interest (QoI), and the dimensionality of
the output space, respectively.

In practice, the exact values of the input variables are often not known
exactly and may be considered _uncertain_.
The ensuing analysis involving uncertain input variables can be formalized
in the uncertainty quantification (UQ) framework following {cite}`Sudret2007`
as illustrated in {numref}`uq-framework`.

```{figure} ./uq-framework.png
:name: uq-framework

Uncertainty quantification (UQ) framework, adapted from {cite}`Sudret2007`.
```

The framework starts from the center,
with the computational model $\mathcal{M}$ taken as a black-box
as defined earlier.
Then it moves on to the probabilistic modeling of the (uncertain) input
variables.
Under the probabilistic modeling, the uncertain input variables are represented
by a random vector equipped with a joint probability density function
(PDF)

$$
f_{\boldsymbol{X}}: \boldsymbol{x} \in \mathcal{D}_{\boldsymbol{X}} \subseteq \mathbb{R}^M \to \mathbb{R}.
$$

```{note}
See {ref}`Probabilistic Input Modeling <prob-input:overview>` for how this
is specified in UQTestFuns.
```

Subsequently, the uncertainties of the input variables are propagated through
the computational model $\mathcal{M}$. As a result, the quantity of interest
$\boldsymbol{y}$ now itself becomes a random vector[^random-vector]:

$$
\boldsymbol{Y} = \mathcal{M}(\boldsymbol{X}), \boldsymbol{X} \sim f_{\boldsymbol{X}}.
$$

This leads to various downstream analyses such as:

- {ref}`reliability analysis <fundamentals:reliability>`:
  Estimating the probability of small or rare failure events.
- {ref}`sensitivity analysis <fundamentals:sensitivity>`:
  Quantifying the contribution of the input uncertainties to output uncertainty.
- {ref}`metamodeling <fundamentals:metamodeling>`:
  Constructing a fast surrogate approximation for a typically expensive
  computational model.

In UQTestFuns, these analyses form the primary categories of 
UQ test functions based on their applications in the literature[^classifications].
Additionally, many global sensitivity analysis problems reduce to solving
an {ref}`integration <fundamentals:integration>` problem, which explains the
extra category.
For completeness, UQTestFuns also includes test functions commonly
used for benchmarking and testing
{ref}`optimization <fundamentals:optimization>` methods.

## From framework to UQTestFuns

This framework maps directly onto {ref}`three objects <api-reference:overview>`.
The computational model $\mathcal{M}$ is a {ref}`UQTestFun <api_reference_uqtestfun>` instance,
called directly to evaluate $\boldsymbol{y} = \mathcal{M}(\boldsymbol{x})$.
The probabilistic input $f_{\boldsymbol{X}}$ is a
{ref}`ProbInput <api_reference_probabilistic_input>` instance,
composed of one-dimensional {ref}`Marginal <api_reference_marginal_distribution>`
distributions. Sampling $\boldsymbol{X} \sim f_{\boldsymbol{X}}$ is
`get_sample()`.

See the {ref}`Create Built-in Test Functions <getting-started:tutorial-built-in-functions>`
tutorial for a hands-on walkthrough of using these objects in code.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^random-vector]: or in the case of a single output (i.e., $P = 1$): random
variable.
[^classifications]: These categories are not mutually exclusive; a given UQ
test function may be applied in several contexts.