(prob-input:concepts-and-notations)=
# Probability Concepts and Notations

This page is intended to provide the definitions of the basic concepts
in probability and the notational conventions relevant to UQTestFuns.
It is not intended to be an exhaustive treatment of the subject.

In the current version of UQTestFuns, we are concerned only
with continuous input variables.
Consequently, the discussion below is restricted to continuous random variables.

```{note}
Random variables are special mathematical objects[^random-variable].
A common convention is to write a random variable in upper case ($X$, $Y$, etc.)
and the particular values of the random variable in lower case ($x$, $y$, etc.).
But this convention is not always maintained here.
For instance, some physical constants appearing in UQ test functions are denoted by capital letters (also by convention).
Clearly, in this context, they are not random variables.

We would appeal to your wisdom in making the distinction between these notations.
```

(prob-input:concepts-and-notations:cdf)=
## Cumulative distribution function (CDF)

A continuous random variable $X$ distributed according to a (univariate)
_cumulative distribution function_ (CDF) $F_X: \mathcal{D}_X \mapsto [0, 1]$
is written as:

$$
X \sim F_X (x).
$$

The symbol $\mathcal{D}_X$ above denotes the _support_ of the random variable;
that is, the set of all possible values of $X$.

The CDF of $X$ is by definition:

$$
F_X (x) \equiv \mathbb{P}[X \leq x]
$$

The distribution of $X$ is uniquely determined by its CDF.

(prob-input:concepts-and-notations:pdf)=
## Probability density function (PDF)

The derivative of the cumulative distribution function, if it exists,
is called the (univariate) probability density function (PDF) of $X$,
denoted by $f_X(x)$.
Specifically, if it exists, the PDF value at $x$ is defined as follows:

$$
f_X(x) \equiv \frac{d F_X(x)}{dx} = \lim_{\Delta x \to 0} \frac{F_X(x + \Delta x) - F_X(x)}{\Delta x} 
$$

When this condition applies, then the PDF is also unique and we may also write:

$$
X \sim f_X(x).
$$

It is important to realize that for a continuous random variable,
the density value at a given $x$ is not a probability.
In fact, the probability of $X$ taking a particular value $x$ is $0$.
You can, however, think of the quantity $f_X(x) \, dx$ as a probability;
it's the probability of $X$ having a value in an infinitesimal interval around $x$. 

With the PDF given we can define the support of a continuous random variable
more precisely:

$$
\mathcal{D}_X \equiv \{ x \in \mathbb{R} | f_X (x) > 0 \}.
$$

Using the PDF, we can write the CDF as follows:

$$
F_X (x) = \int_{\mathcal{D}^-_X}^x f_X (t) \, dt,
$$

where $\mathcal{D}^-_X$ denotes the lower bound of the support.

(prob-input:concepts-and-notations:icdf)=
## Inverse cumulative distribution function (ICDF)

The inverse cumulative distribution function (ICDF) of a random variable $X$
is the function $F_X^{-1}: [0, 1] \mapsto \mathcal{D}_X$.
In other words, the function takes a probability value $p$
and returns the corresponding quantile value of the random variable
such that $F_X (x) = \mathbb{P}[X \leq x] = p$.

Some would refer to ICDF as the _quantile function_ or _percent point function_ (PPF).

## Parametric distributions

The distribution of a random variable may be one of the commonly known parametric distributions
like the normal (Gaussian) distribution, the beta distribution, the Gumbel distribution, etc.
As an example, if $X$ is a normally distributed random variable, we write:

$$
X \sim \mathcal{N}(\mu, \sigma)
$$

where $\mu$ and $\sigma$ are the parameters of the normal distributions
(that is the mean and the standard deviation, respectively).
Given the values of the parameters, a particular (parametric) distribution
is completely and uniquely specified.

## Random vectors

A multi-dimensional probabilistic input model is, in principle, a
_random vector_, sometimes called a "multivariate random variable"[^imprecise].
A random vector consists of individual random variables grouped together
under some dependency structure.

An $M$-dimensional random vector is denoted by
$\boldsymbol{X} = (X_1, \ldots, X_M )^T$
with a _joint_ cumulative distribution function (CDF)
$F_{\boldsymbol{X}}: \mathcal{D}_{\boldsymbol{X}} \subseteq \mathbb{R}^M \mapsto [0, 1]$
and, if it exists, a _joint_ probability density function (PDF) 
$f_{\boldsymbol{X}}: \mathcal{D}_{\boldsymbol{X}} \subseteq \mathbb{R}^M \mapsto \mathbb{R}_{\geq 0}$.

A common assumption (though in no way general) is the independence between
all the component random variables in the random vector.
Under independence, the CDF of an $M$-dimensional random vector $\boldsymbol{X}$
can be written as follows:

$$
F_{\boldsymbol{X}} (x_1, \ldots, x_M) = \prod_{m = 1}^M F_{X_m} (x_m), 
$$

where $F_{X_m}$, the _marginal_ CDF of $X_m$, is the univariate CDF of a
component random variable.
If it exists, the PDF can be written accordingly:

$$
f_{\boldsymbol{X}} (x_1, \ldots, x_M) = \prod_{m = 1}^M f_{X_m} (x_m),
$$

where $f_{X_m}$ is the univariate PDF of a component random variable.

[^random-variable]: it's neither random
(at least, not in _completely unpredictable_ sense)
nor a variable (it's a function).
[^imprecise]: "multivariate random variable" is, however, a less precise term,
since a random variable is, strictly speaking, always univariate.