---
title: 'UQTestFuns: A Python3 library of uncertainty quantification (UQ) test functions'
tags:
  - Python
  - uncertainty quantification
  - metamodeling
  - surrogate modeling
  - sensitivity analysis
  - reliability analysis
  - rare-event estimations
authors:
  - name: Damar Wicaksono
    orcid: 0000-0000-0000-0000
    affiliation: 1 # (Multiple affiliations must be quoted)
    corresponding: true
  - name: Michael Hecht
    affiliation: 1
affiliations:
 - name: Center for Advanced Systems Understanding (CASUS) - Helmholzt-Zentrum Dresden-Rossendorf (HZDR), Germany
   index: 1
date: 30 June 2023
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
# aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
# aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary

New methods and algorithms are continously being developed within
the applied uncertainty quantification (UQ) framework whose activities include,
among others, metamodeling, uncertainty propagation, reliability analysis,
and sensitivity analysis.
During the development phase of such methods, researchers and developers often
rely on test functions taken from the literature
to validate a newly proposed method.
Afterward, these test functions are employed as a common ground to benchmark
the performance of the method with other methods in terms of
some accuracy measures with respect to the number of function evaluations.

`UQTestFuns` is an open-source Python3 library of test functions commonly used
within the applied UQ community. Specifically, the package aims to provide:

- a lightweight implementation, with minimal dependencies of many test functions
  available in the UQ literature;
- a single entry point, combining test functions and their probabilistic input
  specifications, to a wide range of test functions;
- an opportunity for an open-source contribution where new test functions
  are implemented and reference results are posted.

All in all, `UQTestFuns` aims to save the reseachers' and developers' time
from reimplementing many of the commonly used test functions and to provide
a summary reference to the test functions and their applications.

# Statement of need

New methods and algorithms for solving a particular type of UQ analyses
(reliability analysis, sensitivity analysis, etc.) are continuously being
developed.
While such methods are eventually aimed at solving real-world problems&mdash;typically
involve a complex expensive-to-evaluate computational model&mdash;researchers
and developers may prefer to initially use the so-called UQ test functions
for validation and benchmarking purposes.

UQ test functions are, in principle, mathematical functions taken as black boxes;
they take a set of input values and produce output values.
However, in a typical UQ analysis, the input variables are considered uncertain
and thus modeled probabilistically.
The results of a UQ analysis, in general, depend not only on the computational
model under consideration but also on the specification of the input variables.
Consequently, a UQ test function consists of both the specification
of the function as well as the probabilistic specification of the inputs.
These test functions are widely used because:

- test functions are _fast to evaluate_, at least _faster_ than their real-world counterparts;
- there are _many of them available_ in the literature for various types of analyses;
- while a UQ analysis usually takes the computational model of interest
  as a black box, the test functions _are known_
  (they are not black boxes per se) such that a thorough diagnosis
  of a newly proposed method can be performed;
- test functions provide _a common ground_ for comparing the performance of
  a given method with that of other available methods
  in solving the same class of problem.

Several online sources provide a wide range of test functions relevant to
the UQ community. For example, and by no means an exhaustive list:

- The Virtual Library of Simulation Experiments (VLSE) [@VLSE:2013]:
  This site is arguably the definitive repository for (but not exclusively) UQ test functions.
  It provides over a hundred test functions for numerous applications; 
  each test function is described in a dedicated page that includes
  implementations in MATLAB and R.
- The Benchmark proposals of GdR [@GdR:2008]:
  The site provides a series of documents that contain test function
  specifications.
- The Benchmark page of UQWorld [@UQWorld:2019]:
  This community site provides a selection of test functions
  in metamodeling, sensitivity analysis, and reliability analysis along 
  with their implementation in MATLAB.
- RPrepo&mdash;a reliability problems repository [@Rozsas:2019]:
  This repository contains numerous reliability analysis test functions
  implemented in Python.

Common to all these online resources (except for RPrepo) are the requirements
to implement the test function oneself following the specification,
or, when available, to download each of the test functions separately.

Alternatively, UQ analysis packages are often shipped
with a selection of test functions either
for illustration, validation, or benchmarking.
Below are some examples from the Python applied UQ community
(the numbers are as of 2023-06-30; once again,
the list is non-exhaustive):

- UncertainPy [@Tennoe:2018a; @Tennoe:2018b] includes 8 test functions (mainly in
  the context of neuroscience) for illustrating the package capabilities.
- PyApprox [@Jakeman2019] includes 18 test functions,
  including some non-algebraic functions for benchmarking purposes.
- Surrogate Modeling Toolbox (SMT) [@Bouhlel2019; @Bouhlel2023] includes 
  11 analytical and engineering problems for benchmarking purposes.
- OpenTURNS [@Baudin2017] has its own separate benchmark package
  called `otbenchmark` [@Fekhari2021; @Baudin2021] that includes
  37 test functions.

These open-source packages already provide a wide variety of functions 
implemented in Python.
The problem is that these functions are part of the respective package.
To get access to the test functions belonging to a package, 
the whole analysis package must be installed first.
Furthermore, test functions from a given package are often implemented in such a way
that is tightly coupled with the package itself. 
To use the test functions belonging to a package,
one may need to learn some basic usage and specific terminologies of the package. 

`UQTestFuns` is mostly comparable to the package `otbenchmark` in its aim.
Both also acknowledge the particularity of UQ test functions
that require combining a test function
and the corresponding probabilistic input specification.
There are, however, some major differences:

- `UQTestFuns` is more lightweight with fewer dependencies,
  while `otbenchmark` is coupled to the package OpenTURNS.
  This is to be expected as one of `otbenchmark`'s main goals
  is to provide the OpenTURNS development team with a tool
  for helping with the implementation of new algorithms.
- `UQTestFuns` is more modest in its scope, that is, simply to provide 
  a library of UQ test functions implemented in Python
  with a consistent interface and an online reference 
  (similar to that of VLSE [@VLSE:2013]), and not,
  as in the case of `otbenchmark`,
  an automated benchmark framework[^benchmark] [@Fekhari2021].

# Package overview

Consider a computational model that is represented as an $M$-dimensional
black-box function:
\begin{equation*}
\mathcal{M}: \boldsymbol{x} \in \mathcal{D}_{\boldsymbol{X}} \subseteq \mathbb{R}^M \mapsto y = \mathcal{M}(\boldsymbol{x}),
\end{equation*}
where $\mathcal{D}_{\boldsymbol{X}}$ and $y$ denote the input domain
and the quantity of interest (QoI), respectively.

In practice, the exact values of the input variables are not exactly known
and may be considered uncertain.
The ensuing analysis involving uncertain input variables can be formalized
in the uncertainty quantification (UQ) framework following @Sudret2007
as illustrated in \autoref{fig:uq-framework}.

![Uncertainty quantification (UQ) framework, adapted from @Sudret2007.\label{fig:uq-framework}](uq-framework.png){ width=80% }

The framework starts with the computational model $\mathcal{M}$
taken as a black box as defined above.
Then, it moves on to the quantification of the input uncertainties.
This uncertainty is modeled probabilistically
such that the input variables are represented as a random vector
equipped with joint probability density function (PDF)
$f_{\boldsymbol{X}} \in \mathcal{D}_{\boldsymbol{X}} \subseteq \mathbb{R}^M$.

Afterward, the uncertainties from the input variables are propagated through
the computational model $\mathcal{M}$.
The quantity of interest $y$, as computed by $\mathcal{M}$,
now becomes as random variable:
$$
Y = \mathcal{M}(\boldsymbol{X}),\; \boldsymbol{X} \sim f_{\boldsymbol{X}}.
$$
This leads to various downstream analyses such as reliability analysis,
sensitivity analysis, and metamodeling.
In `UQTestFuns`, these are currently the three main classifications
of UQ test functions by their applications in the literature[^classifications].

## Reliability analysis

Consider the circular pipe crack reliability test function,
a $2$-dimensional function for testing reliability analysis methods
[@Verma2015; @Li2018]:
$$
g(\boldsymbol{x}; \boldsymbol{p}) = \mathcal{M}(\boldsymbol{x}; t, R) - M  = 4 t \sigma_f R^2 \left( \cos{\left(\frac{\theta}{2}\right)} - \frac{1}{2} \sin{(\theta)} \right) - M
$$
where $\boldsymbol{x} = \{ \sigma_f, \theta \}$ is the two-dimensional vector of
input variables probabilistically defined further below;
and $\boldsymbol{p} = \{ t, R, M \}$ is the vector of (deterministic) parameters.

In a reliability analysis problem,
a computational model $\mathcal{M}$ is often combined with another set of parameters
(either uncertain or deterministic) to define the so-called
_performance function_ or _limit-state function_ of a system denoted by $g$.
The task of reliability analysis methods is to estimate the failure probability
of the system defined as follows [@Sudret2012]:
$$
P_f = \mathbb{P}[g(\boldsymbol{X}; \boldsymbol{p}) \leq 0] = \int_{\mathcal{D}_f = \{ \boldsymbol{x} | g(\boldsymbol{x}; \boldsymbol{p}) \leq 0 \}} f_{\boldsymbol{X}} (\boldsymbol{x}) \; d\boldsymbol{x}
$$
where $g(\boldsymbol{x}) \leq 0.0$ is defined as a _failure state_.
The difficulty of evaluating the integral above stems from the fact
that the integration domain $D_f$ is defined implicitly.

The circular pipe crack problem can be created in `UQTestFuns` as follows:
```python
>>> import uqtestfuns as uqtf
>>> circular_pipe = uqtf.CircularPipeCrack()
```

As explained above, the probabilistic input model is an integral part
of a UQ test function (the results depend on it).
In `UQTestFuns`, the input model according to the original specification is attached
to the instance of the test function:
```
>>> print(circular_pipe.prob_input)
Name         : CircularPipeCrack-Verma2015
Spatial Dim. : 2
Description  : Prob. input model for the circular pipe crack problem from...
Marginals    :
  No.   Name     Distribution      Parameters          Description
-----  -------  --------------  -----------------  --------------------
    1  sigma_f      normal      [301.079  14.78 ]   flow stress [MNm]
    2   theta       normal        [0.503 0.049]    half crack angle [-]

Copulas      : None
```
The probabilistic input model instance can be used, among other things,
to transform a set of values in a given domain (say, the unit hypercube $[0, 1]^M$)
to the domain of the test function.

The limit-state surface (i.e., where $g(\boldsymbol{x}) = 0$)
for the circular pipe crack problem is shown in \autoref{fig:reliability} (left plot).
In the middle, $10^6$ random sample points are overlaid;
each point is classified whether it is in failure (red) or safe domain (blue).
As illustrated in the histogram (right plot),
the task of the analysis is to accurately estimate the probability where $g(\boldsymbol{X}) \leq 0$
(and with as few as function evaluations as possible).

![Illustration of reliability analysis: Circular pipe crack problem.\label{fig:reliability}](reliability.png){ width=90% }

## Sensitivity analysis

Consider the Sobol'-G function,
an $M$-dimensional function commonly used
for testing sensitivity analysis methods [@Saltelli1995]:
$$
\mathcal{M}(\boldsymbol{x}) = \prod_{m = 1}^M \frac{\lvert 4 x_m - 2 \rvert + a_m}{1 + a_m},
$$
where $\boldsymbol{x} = \{ x_1, \ldots, x_M \}$ is the $M$-dimensional vector
of independent uniform random variables in $[0, 1]^M$;
and $\boldsymbol{a} = \{ a_m = \frac{m - 1}{2.0}, m = 1, \ldots, M \}$
is the set of parameters.

The tasks of sensitivity analysis methods are to ascertain
either qualitatively or quantitatively
the most important input variables (for _factor prioritization_)
and/or the least important input variables
(for _factor fixing_).
See @Saltelli2007 and @Iooss2015 for details on the topic.

The Sobol'-G test function can be created in `UQTestFuns`
for any given dimension.
For instance, to create a $6$-dimensional Sobol'-G function:
```python
>>> sobol_g = uqtf.SobolG(spatial_dimension=6)
```
As before, the probabilistic input model of the function as prescribed
in the original specification is attached to the instance of test function
(i.e., the `prob_input` property).

## Metamodeling

In practice, the computational model $\mathcal{M}$ is often complex.
Because a UQ analysis typically involves evaluating $\mathcal{M}$
numerous times ($\sim 10^2$ &mdash; $10^6$),
the analysis may become intractable if $\mathcal{M}$ is expensive to evaluate.
As a consequence, in many UQ analyses, a metamodel (surrogate model) is employed.
With a limited number of full model ($\mathcal{M}$) evaluations,
such a metamodel should be able to capture the most important aspects
of the input/output mapping
and can, therefore, be used to replace $\mathcal{M}$ in the analysis.

While not a goal of UQ analyses per se,
metamodeling is nowadays an indispensable component of the UQ framework [@Sudret2017].
`UQTestFuns` also includes test functions from the literature that are used
as test functions in a metamodeling exercise.

## Documentation

The online documentation of `UQTestFuns` is an important aspect of the project.
It includes a detailed description of each of the available UQ test functions,
their references, and, when applicable, published results of a UQ analysis
conducted using the test function.
Guides on how to add additional test functions as well as
to update the documentation are also available.

The package documentation is available
on the `UQTestFuns` [readthedocs](https://uqtestfuns.readthedocs.io).

# Acknowledgements

This work was partly funded by the Center for Advanced Systems Understanding
(CASUS) that is financed by Germany's Federal Ministry of Education and Research
(BMBF) and by the Saxony Ministry for Science, Culture and Tourism (SMWK)
with tax funds on the basis of budget approved by the Saxony Sate Parliament.

# References

[^benchmark]: A fully functional benchmark suite may, however, be in the future
built on top of `UQTestFuns`.

[^classifications]: The classifications are not mutually exclusive;
a given UQ test function may be applied in several contexts. 