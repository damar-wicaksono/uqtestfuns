(api-reference:overview)=
# UQTestFuns API Reference Guide

This reference guide contains a detailed description of the most important
elements of the UQTestFuns package.

To make sense of how the objects in UQTestFuns are organized,
let's start from the top, the {ref}`built-in test functions <test-functions:available>`:

- Each of the built-in UQ test functions is a concrete implementation of the
  abstract base classes: {ref}`UQTestFunFixDimABC <api_reference_uqtestfun_fix_dim_abc>`
  (for UQ test functions with fixed dimension) or
  {ref}`UQTestFunVarDimABC <api_reference_uqtestfun_var_dim_abc>`
  (for UQ test functions with variable dimension).
- Both of those abstract classes are derived from {ref}`UQTestFunABC <api_reference_uqtestfun_abc>`.
  This base class, in turn, is derived 
  from {ref}`UQTestFunBareABC <api_reference_uqtestfun_bare_abc>`).
  Therefore, all the instances share the same underlying interfaces.
  In particular, all instances share, among other things, the ``evaluate()`` 
  method, the ``prob_input`` property, and the ``parameters`` property [^essence].
- The ``prob_input`` property stores the underlying probabilistic input model 
  of the instance. This in turn is represented
  by the {ref}`ProbInput <api_reference_probabilistic_input>` class.
  In principle, an instance of the class is a multivariate random variable that 
  represents the input of an uncertainty quantification (UQ) test function.
- An instance of the ``ProbInput`` class consists mainly of the one-dimensional
  marginals and a copula specification (not yet supported). Each one-dimensional
  marginal comes is represented
  by the {ref}`Marginal <api_reference_marginal_distribution>` class. 
- An instance of the ``Marginal`` class has a (parametric) probability
  distribution. Although different instances may have different
  probability distributions, they are all instances of the same class.

```{note}
To facilitate the creation of a custom UQ test function
in runtime or within a running Python session, UQTestFuns also includes
the concrete {ref}`api_reference_uqtestfun` class.
You can see the usage {ref}`here <getting-started:tutorial-custom-functions>`.
```

Additionally, there is currently one top-level convenient function used to
{ref}`list all available built-in functions <api_reference_list_functions>`.
The function can return both a table on the terminal or a list of constructors
ready to be called.

[^essence]: These three are the defining elements of a UQ test function.
