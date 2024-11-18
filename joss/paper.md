---
title: 'UQTestFuns: A Python3 library of uncertainty quantification (UQ) test functions'
tags:
  - Python
  - test functions
  - benchmark
  - uncertainty quantification
  - metamodeling
  - surrogate modeling
  - sensitivity analysis
  - reliability analysis
  - rare event estimation
authors:
  - name: Damar Wicaksono
    orcid: 0000-0001-8587-7730
    affiliation: 1 # (Multiple affiliations must be quoted)
    corresponding: true
  - name: Michael Hecht
    orcid: 0000-0001-9214-8253
    affiliation: 1
affiliations:
 - name: Center for Advanced Systems Understanding (CASUS) - Helmholtz-Zentrum Dresden-Rossendorf (HZDR), Germany
   index: 1
date: 30 June 2023
bibliography: paper.bib
---

# Summary

Researchers are continuously developing novel methods and algorithms
in the field of applied uncertainty quantification (UQ).
During the development phase of a novel method or algorithm,
researchers and developers often rely on test functions
taken from the literature for validation purposes.
Afterward, they employ these test functions as a fair means
to compare the performance of the novel method
against that of the state-of-the-art methods
in terms of accuracy and efficiency measures.

`UQTestFuns` is an open-source Python3 library of test functions
commonly used within the applied UQ community.
Specifically, the package provides:

- an **implementation with minimal dependencies**
  (i.e., NumPy and SciPy) **and a common interface** of many test functions
  available in the UQ literature
- a **single entry point** collecting test functions _and_
  their probabilistic input specifications in a single Python package
- an **opportunity for an open-source contribution**, supporting
  the implementation of new test functions and posting reference results.

`UQTestFuns` aims to save the researchers' and developers' time
from having to reimplement many of the commonly used test functions
themselves.

# Statement of need

The field of uncertainty quantification (UQ) in applied science and engineering
has grown rapidly in recent years.
Novel methods and algorithms for metamodeling (surrogate modeling),
reliability, and sensitivity analysis are being continuously developed.
While such methods are aimed at addressing real-world problems,
often involving large-scale complex computer models&mdash;from nuclear
[@Wicaksono2016] to civil engineering [@Castellon2023],
from physics [@Adelmann2019] to biomedicine [@Eck2015]&mdash;researchers
and developers may prefer to use the so-called UQ test functions
for validation and benchmarking purposes.

UQ test functions are mathematical functions taken as black boxes;
they take a set of input values and produce output values.
In a typical UQ analysis, the input variables are considered _uncertain_
and thus modeled probabilistically.
The results of a UQ analysis, in general, depend not only on the computational
model under consideration but also on the specification of the input variables.
Consequently, a UQ test function consists of both the specification
of the function as well as probabilistic distribution specification
of the inputs.

UQ test functions are widely used in the community for several reasons:

- Test functions are _fast to evaluate_,
  at least _faster_ than their real-world counterparts.
- There are many test functions _available in the literature_
  for various types of analyses.
- Although test functions are taken as black boxes, _their features are known_; 
  this knowledge enables a thorough diagnosis of a UQ method.
- Test functions provide a _fair means_ for comparing the performance
  of various UQ methods in solving the same class of problems. 

Several efforts have been made to provide relevant UQ test functions
to the community.
For instance, researchers may refer to the following online resources
to obtain UQ test functions (the list is by no means exhaustive):

- The Virtual Library of Simulation Experiments (VLSE) [@VLSE:2013]: This site
  is arguably the definitive repository for (but not exclusively) UQ test
  functions. It provides over a hundred test functions
  for numerous applications; each test function is described
  on a dedicated page that includes implementations in MATLAB and R.
- The Benchmark proposals of GdR [@GdR:2008]: The site provides a series of
  documents that contain test function specifications.
- The Benchmark page of UQWorld [@UQWorld:2019]: This community site provides
  a selection of test functions for metamodeling, sensitivity analysis,
  and reliability analysis exercises along with their implementation in MATLAB.
- RPrepo&mdash;a reliability problems repository [@Rozsas:2019]: This
  repository contains numerous reliability analysis test functions implemented
  in Python. It is not, however, a stand-alone Python package.

Using these online resources, one either needs to download each test function 
separately[^rprepo] or implement the functions following
the provided formula (in the programming language of choice).

As an alternative way for obtaining test functions,
UQ analysis packages are often shipped with a selection of test functions
of their own, either for illustration, validation, or benchmarking purposes.
Examples from the applied UQ community in the Python ecosystem are
(the numbers are as of 2023-06-30; once again, the list is non-exhaustive):

- SALib [@Herman2017; @Iwanaga2022]: Six test functions
  mainly for illustrating the package capabilities in the examples.
- PyApprox [@Jakeman2019]: 18 test functions,
  including some non-algebraic functions for benchmarking purposes.
- Surrogate Modeling Toolbox (SMT) [@Bouhlel2019; @Bouhlel2023]:
  11 analytical and engineering problems for benchmarking purposes.
- OpenTURNS [@Baudin2017]: 37 test functions packaged separately
  as `otbenchmark` [@Fekhari2021; @Baudin2021] for benchmarking purposes.

These open-source packages already provide a wide variety of functions
implemented in Python. Except for `otbenchmark`, the problem is that
these functions are part of the respective package. To get access to
the test functions belonging to a package, the whole analysis package
must be installed first. Furthermore, test functions from a given package are
often implemented in such a way that is tightly coupled with the package
itself. To use or extend the test functions belonging to an analysis package,
one may need to first learn some basic usage and specific terminologies
of the package.

`UQTestFuns` aims to solve this problem by collecting UQ test functions
into a single Python package
with a few dependencies (i.e., NumPy [@Harris2020]
and SciPy [@Virtanen2020]).
The package enables researchers
to conveniently access commonly used UQ test functions implemented in Python.
Thanks to a common interface,
researchers can use the available test functions
and extend the package with new test functions with minimal overhead.

Regarding its aim, `UQTestFuns` is mostly comparable
to the package `otbenchmark`.
Both also acknowledge the particularity of UQ test functions that requires
combining a test function and the corresponding probabilistic input
specification.
There are, however, some major differences:

- One of the `otbenchmark`'s main aims is to provide the OpenTURNS development
  team with a tool for helping with the implementation of new algorithms.
  As such, it is built on top of and coupled to OpenTURNS.
  `UQTestFuns`, on the other hand, has fewer dependencies and is leaner 
  in its implementations;
  it is more agnostic with respect to any particular UQ analysis package.
- `UQTestFuns` is more modest in its scope, that is, simply to provide
  a library of UQ test functions implemented in Python
  with a consistent interface and an online reference
  (similar to that of VLSE [@VLSE:2013]),
  and not, as in the case of `otbenchmark`,
  an automated benchmark framework[^benchmark] [@Fekhari2021].

# Package overview

Consider a computational model that is represented as an $M$-dimensional
black-box function:
$$
\mathcal{M}: \mathbf{x} \in \mathcal{D}_{\mathbf{X}} \subseteq \mathbb{R}^M \mapsto y = \mathcal{M}(\mathbf{x}),  
$$
where $\mathcal{D}_{\mathbf{X}}$ and $y$ denote the input domain
and the quantity of interest (QoI), respectively.  

In practice, the exact values of the input variables are not exactly known
and may be considered uncertain.
The ensuing analysis involving uncertain input variables can be formalized
in the uncertainty quantification (UQ) framework following @Sudret2007
as illustrated in \autoref{fig:uq-framework}.

![Uncertainty quantification (UQ) framework, adapted from @Sudret2007.\label{fig:uq-framework}](uq-framework.png){ width=70% }

The framework starts from the center,
with the computational model $\mathcal{M}$ taken as a black box
as defined above.
Then it moves on to the probabilistic modeling
of the (uncertain) input variables.
Under the probabilistic modeling,
the uncertain input variables are replaced by a random vector equipped
with a joint probability density function (PDF)
$f_{\mathbf{X}}: \mathbf{x} \in \mathcal{D}_{\mathbf{X}} \subseteq \mathbb{R}^M \mapsto \mathbb{R}$.

Afterward, the uncertainties of the input variables are propagated through
the computational model $\mathcal{M}$.
The quantity of interest $y$ now becomes a random variable:
$$  
Y = \mathcal{M}(\mathbf{X}),\; \mathbf{X} \sim f_{\mathbf{X}}.  
$$
This leads to various downstream analyses such as _reliability analysis_,
_sensitivity analysis_,
and _metamodeling_ (or _surrogate modeling_).
In `UQTestFuns`, these are currently the three main classifications
of UQ test functions by their applications in the literature[^classifications].

## Reliability analysis

To illustrate the test functions included in `UQTestFuns`,
consider the circular pipe crack reliability problem, a $2$-dimensional
function for testing reliability analysis methods [@Verma2015; @Li2018]:
$$  
g(\mathbf{x}; \mathbf{p}) = \mathcal{M}(\mathbf{x}; t, R) - M = 4 t \sigma_f R^2 \left( \cos{\left(\frac{\theta}{2}\right)} - \frac{1}{2} \sin{(\theta)} \right) - M,
$$  
where $\mathbf{x} = \{ \sigma_f, \theta \}$ is the two-dimensional vector
of input variables probabilistically defined further below;
and $\mathbf{p} = \{ t, R, M \}$ is the vector of (deterministic) parameters.
  
In a reliability analysis problem,
a computational model $\mathcal{M}$ is often combined
with another set of parameters (either uncertain or deterministic)
to define the so-called _performance function_ or _limit-state function_
of a system denoted by $g$.
The task for a reliability analysis method is to estimate the failure
probability of the system defined, following @Sudret2012, as:
\begin{equation}\label{eq:pf}
P_f = \mathbb{P}[g(\mathbf{X}; \mathbf{p}) \leq 0] = \int_{\mathcal{D}_f = \{ \mathbf{x} | g(\mathbf{x}; \mathbf{p}) \leq 0 \}} f_{\mathbf{X}} (\mathbf{x}) \; d\mathbf{x},
\end{equation}
where $g(\mathbf{x}; \mathbf{p}) \leq 0.0$ is defined as a _failure state_.
The difficulty of evaluating the integral above stems
from the fact that the integration domain $D_f$ is defined implicitly.

The circular pipe crack problem can be created in `UQTestFuns` as follows:
```python
>>> import uqtestfuns as uqtf
>>> circular_pipe = uqtf.CircularPipeCrack()
```

The resulting instance is _callable_ and can be called
with a set of valid input values.
The probabilistic input model is an integral part of a UQ test function;
indeed, according to \autoref{eq:pf}, the analysis results depend on it.
Therefore, in `UQTestFuns`, the input model following
the original specification is always attached to the instance
of the test function:
```
>>> print(circular_pipe.prob_input)
Name         : CircularPipeCrack-Verma2015
Spatial Dim. : 2
Description  : Input model for the circular pipe crack problem from Verma...
Marginals    :

  No.   Name     Distribution      Parameters          Description
-----  -------  --------------  -----------------  --------------------
    1  sigma_f      normal      [301.079  14.78 ]   flow stress [MNm]
    2   theta       normal        [0.503 0.049]    half crack angle [-]

Copulas      : None
```
This probabilistic input model instance can be used to transform
a set of values in a given domain (say, the unit hypercube $[0, 1]^M$)
to the domain of the test function.

The limit-state surface (i.e., where $g(\mathbf{x}) = 0$)
for the circular pipe crack problem is shown in \autoref{fig:reliability}
(left plot). In the middle plot, $10^6$ random sample points are overlaid;
each point is classified whether it is in failure (red) or safe domain (blue).
The histogram (right  plot) shows the proportion of points
that fall in the failure and safe domain.

![Illustration of reliability analysis: Circular pipe crack problem.\label{fig:reliability}](reliability.png){ width=90% }

As illustrated in the previous series of plots,
the task for a reliability analysis method is to estimate
the probability where $g(\mathbf{X}) \leq 0$ as accurately
and with as few model evaluations as possible.
`UQTestFuns` includes test functions used in reliability analysis exercises
in various dimensions having different complexities of the limit-state surface.

## Sensitivity analysis

As another illustration, this time in the context of sensitivity analysis,
consider the Sobol'-G function, an established sensitivity analysis
test function [@Saltelli1995] included in `UQTestFuns`:
$$
\mathcal{M}(\mathbf{x}) = \prod_{m = 1}^M \frac{\lvert 4 x_m - 2 \rvert + a_m}{1 + a_m},
$$
where $\mathbf{x} = \{ x_1, \ldots, x_M \}$ is the $M$-dimensional vector
of independent uniform random variables in $[0, 1]^M$;
and $\mathbf{a} = \{ a_m = \frac{m - 1}{2.0}, m = 1, \ldots, M \}$
is the set of (deterministic) parameters.

Unlike the previous test function example,
the Sobol'-G test function is a variable-dimension test function
and can be defined for any given dimension.
For instance, to create a $6$-dimensional Sobol'-G function:
```python  
>>> sobol_g = uqtf.SobolG(spatial_dimension=6)  
```
As before, the probabilistic input model of the function as prescribed
in the original specification is attached to the instance of the test function
(i.e., the `prob_input` property).

The task of a sensitivity analysis method is to ascertain either qualitatively
or quantitatively the most important input variables
(for _factor prioritization_) or the least important input variables
(for _factor fixing/screening_) with as few model evaluations as possible;
for details on this topic, please refer to @Saltelli2007 and @Iooss2015.
`UQTestFuns` includes test functions used in sensitivity analysis exercises
in various dimensions having different complexities
in terms of the interactions between input variables.

## Metamodeling

In practice, the computational model $\mathcal{M}$ is often complex.
Because a UQ analysis typically involves evaluating $\mathcal{M}$
numerous times ($\sim 10^2$ &mdash; $10^6$),
the analysis may become intractable if $\mathcal{M}$ is expensive to evaluate.
As a consequence, in many UQ analyses, a metamodel (surrogate model)
is employed.
Based on a limited number of model ($\mathcal{M}$) evaluations,
such a metamodel should be able to capture the most important aspects
of the input/output mapping but having much less cost per evaluation;
it can, therefore, be used to replace $\mathcal{M}$ in the analysis.

While not a goal of UQ analyses per se,
metamodeling is nowadays an indispensable component
of the UQ framework [@Sudret2017].
`UQTestFuns` also includes test functions from the literature that are used
as test functions in a metamodeling exercise.

## Documentation

The online documentation of `UQTestFuns` is an important aspect of the project.
It includes a detailed description of each of the available UQ test functions,
their references, and when applicable, published results of a UQ analysis
conducted using the test function.
Guides on how to add additional test functions as well as
to update the documentation are also available.

The package documentation is available
on the `UQTestFuns` [readthedocs](https://uqtestfuns.readthedocs.io).

# Authors contribution statement and acknowledgments

The contributions to this paper are listed according to the CRediT
(Contributor Roles Taxonomy). **Damar Wicaksono**: Conceptualization,
methodology, software, validation, and writing - original draft. 
**Michael Hecht**: Conceptualization, writing - review and editing,
project administration, and funding acquisition.

This work was partly funded by the Center for Advanced Systems Understanding
(CASUS) that is financed by Germany's Federal Ministry of Education
and Research (BMBF) and by the Saxony Ministry for Science, Culture
and Tourism (SMWK)
with tax funds on the basis of a budget approved
by the Saxony State Parliament.

# References

[^rprepo]: except for RPrepo, which allows for downloading the whole repository.

[^benchmark]: A fully functional benchmark suite may, however, be in the future
built on top of `UQTestFuns`.

[^classifications]: The classifications are not mutually exclusive;
a given UQ test function may be applied in several contexts.
