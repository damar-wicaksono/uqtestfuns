(development:yaml-specification)=
# YAML Specification Reference

This page provides a complete reference for the YAML specification file
that goes with every built-in test function's Python module.
For a walkthrough of writing a YAML file for a single function,
see {ref}`development:adding-test-function-implementation`.
For how the YAML file gets discovered and turned into a `UQTestFun` instance,
see {ref}`development:how-it-works`.

## A minimal example

A minimal specification of a test function looks like this:
a one-dimensional function with a single input specification and no parameters.

```{note}
This example is the actual specification for the built-in
{ref}`Forrester <test-functions:forrester-1d>` function.
You can open the files `forrester_1d.yaml` and `forrester_1d.py`
in the directory `src/uqtestfuns/test_functions`
```

```{code-block} yaml
:caption: forrester_1d.yaml

name: Forrester1D
description: One-dimensional multimodal function from Forrester et al. (2008)
tags:
  - optimization
  - metamodeling

dimensions:
  input: 1
  output: 1

inputs:
  Forrester2008:
    description: Search domain from Forrester et al. (2008)
    marginals:
      - name: x
        distribution: uniform
        parameters: [0.0, 1.0]
    copulas: null
```

```{code-block} python
:caption: forrester_1d.py (shown here without its docstring, for brevity)

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    return (6 * xx[:, 0] - 2) ** 2 * np.sin(12 * xx[:, 0] - 4)
```

The function is discoverable via `uqtestfuns.list_functions()` and
instantiable via `uqtestfuns.Forrester1D()`
or `uqtestfuns.create("Forrester1D")`.

## Schema overview

A YAML spec file consists of up to six named elements:

| Element                | Required  | Purpose                                                  |
|:-----------------------|:---------:|:---------------------------------------------------------|
| The preamble           |    yes    | Identity, description, categories                        |
| The dimensions         |    yes    | Input/output shape of the function                       |
| The evaluate directive |    no     | Override for the evaluation function                     |
| The inputs section     |    yes    | Probabilistic input specifications (including marginals) |
| The default input      | sometimes | Which input specification to use by default              |
| The parameters section |    no     | Function parameter specifications                        |

## The preamble

This element contains three mandatory fields that identify the function
for discovery and provenance.

```yaml
name: Alemazkoor2D
description: >-
  Two-dimensional high-degree polynomial from Alemazkoor and Meidani (2018)
tags:
  - metamodeling
```

### `name`

`name` is the registry lookup key and the identifier users type to
instantiate the function, for example `uqtf.Alemazkoor2D()`
(see {ref}`Alemazkoor2D <test-functions:alemazkoor-2d>`). It must
be unique across all spec files.

### `description`

`description` is a one-line summary of the function, shown in
`uqtf.list_functions()` and in generated documentation. The `>-` block
scalar folds multiple lines into one, which is useful for longer
descriptions.

```{tip}
Although not enforced by the schema, it's good practice for
`description` to end with a citation-style provenance indicator in the
form "from Author(s) (Year)", e.g. "from Alemazkoor and Meidani
(2018)". Nearly every built-in function follows this convention, and
it gives a reader an immediate pointer to the primary source without
opening the module docstring.
```

### `tags`

`tags` is a list of category tags, drawn from a fixed set:
`sensitivity`, `optimization`, `metamodeling`, `reliability`,
`integration`. A function can have multiple tags.

## The dimensions

`dimensions` describes the shape of the function: how many inputs it
takes and how many outputs it produces.

```yaml
dimensions:
  input: 6
  output: 1
```

### `input`

`input` is required, and is either a positive integer (fixed-dimension
function) or the string `variable` (variable-dimension function).

When `input` is an integer, the function has a fixed number of input
variables, and users instantiate it without specifying a dimension:
`uqtf.OTLCircuit()` (see {ref}`OTLCircuit <test-functions:otl-circuit>`).

```yaml
# Fixed-dimension: exactly 6 inputs
dimensions:
  input: 6
  output: 1
```

When `input` is `variable`, the function accepts any number of input
dimensions, and users must provide the dimension at instantiation:
`uqtf.Ackley(5)` (see {ref}`Ackley <test-functions:ackley>`).

```yaml
# Variable-dimension: user chooses
dimensions:
  input: variable
  output: 1
```

### `output`

`output` is optional and defaults to 1. It's the number of output
values the function returns, and only needs to be specified when the
function returns a vector output.

For example, the {ref}`coffee cup model <test-functions:coffee-cup>`
declares `output: 150`, because its evaluation function returns the
temperature as a function of time rather than a single value.

## The evaluate directive

`evaluate` is optional, and overrides the default convention for
locating the evaluation function.

By default, the framework looks for a function called `evaluate` in
the `.py` file with the same stem name as the YAML file. For example,
`ishigami.yaml` (the spec for {ref}`Ishigami <test-functions:ishigami>`)
has no `evaluate` key at all, so UQTestFuns expects a counterpart
`ishigami.py` containing a function named `evaluate`, which is
what it finds. This default covers the vast majority of cases, and
most contributors never need this element.

Override it when the function has a different name:

```yaml
evaluate: my_special_func
```

This looks for `my_special_func` in the same-stem `.py` file.

Override it when the function lives in a different module:

```yaml
evaluate: otl_circuit.evaluate
```

This looks for `evaluate` in `otl_circuit.py` in the same directory,
which is how {ref}`OTLCircuit20D <test-functions:otl-circuit-20d>`'s
`otl_circuit_20d.yaml` reuses `otl_circuit.py`'s evaluation function
instead of duplicating it.

```{tip}
Whichever `.py` file this resolves to must exist on disk before the
function is first looked up (though it doesn't need to be complete or
even importable yet). If you're writing the YAML first, create the
`.py` file as a stub:

    def evaluate(xx):
        raise NotImplementedError
```

## The inputs section

`inputs` defines the probabilistic input model for the function, the
core of what makes it a *UQ* test function,
because without uncertain inputs it's just an ordinary function.

Each entry in `inputs` is a named input specification containing a
`description` and a `marginals` definition.
The inputs section of the {ref}`OTLCircuit <test-functions:otl-circuit>`
specification appears below, with two of its six marginals included:

```yaml
inputs:
  BenAri2007:
    description: Input model from Ben-Ari and Steinberg (2007)
    marginals:
      - name: Rb1
        distribution: uniform
        parameters: [50.0, 150.0]
        description: Resistance b1 [kOhm]
      - name: Rb2
        distribution: uniform
        parameters: [25.0, 70.0]
        description: Resistance b2 [kOhm]
      # ... four more marginals
```

An input specification can also declare a `copulas` key, describing
dependence between the marginals. Only the independence copula is
supported for now, so `copulas` should be either `null` or omitted
altogether.

(development:yaml-specification:multiple-input-specs)=
### Multiple input specifications

Some functions have alternative input specifications from different
publications, because different authors may choose different
distributions or bounds for the same variables. `inputs` accommodates
this by listing them side by side, each under its own ID.
The {ref}`Borehole <test-functions:borehole>` function specification
in `borehole.yaml` has two input specifications:

```yaml
default_input: Harper1983

inputs:
  Harper1983:
    description: Probabilistic input model from Harper and Gupta (1983)
    marginals:
      # ...
  Morris1993:
    description: >-
      Probabilistic input model from Morris et al. (1993),
      rw and r replaced with uniform distributions
    marginals:
      # ...
```

Each input specification is self-contained: every marginal carries its
own name, distribution, parameters, and description, so the same
variable can be described differently across specifications. In
Borehole, `rw` and `r` are normal/lognormal-distributed in
`Harper1983`, but uniform-distributed in `Morris1993`.

### Shared inputs across function families

When multiple related functions share the same input specification,
point `inputs` at a separate file instead of duplicating the block in
every function's spec. The `genz/` family does this: all six
Genz functions (e.g., {ref}`Genz Continuous <test-functions:genz-continuous>`)
declare

```yaml
inputs: inputs.yaml
```

which points at `inputs.yaml` in the same directory. The content of the file
starts directly at the ID level (and not wrapped in another `inputs:` key):

```yaml
Genz1984:
  description: >-
    Independent uniform random variables from Genz (1984)
  marginals:
    distribution: uniform
    parameters: [0.0, 1.0]
    name: X_$idx
  copulas: null
```

The path is resolved relative to the YAML file's own directory, and
the registry automatically excludes shared input files from function
scanning, so `inputs.yaml` itself never gets registered as a function
in its own right. A file is treated as a shared input spec, not a
function, if its name matches one of these patterns:

- `inputs.yaml`, the default name for a family's shared input spec
- `inputs_<suffix>.yaml`, for example `inputs_ishigami.yaml`
- `<prefix>_inputs.yaml`, for example `sobol_g_inputs.yaml`

## Marginals

The parser for the `marginals` field accepts one of three forms:
an explicit list, a template, or a factory reference. Whichever form
you use, `distribution` must be one of the
{ref}`available marginal distributions <prob-input:available-marginal-distributions>`.

### Explicit list

Each marginal is spelled out individually. This is the most common
format, used when each input variable has its own distribution.

```yaml
marginals:
  - name: Rb1
    distribution: uniform
    parameters: [50.0, 150.0]
    description: Resistance b1 [kOhm]
  - name: Rb2
    distribution: uniform
    parameters: [25.0, 70.0]
    description: Resistance b2 [kOhm]
```

Each entry allows exactly five keys; no other keys are allowed:

| Key            | Required | Notes                        |
|:---------------|:--------:|:-----------------------------|
| `distribution` |   yes    | Distribution name            |
| `parameters`   |   yes    | Distribution parameters      |
| `name`         |    no    | Variable symbol (e.g., X1)   |
| `description`  |    no    | What the variable represents |
| `repeat`       |    no    | Replicate this entry N times |

To replicate several identical marginals without writing each one out,
add a `repeat` key. {ref}`OTLCircuit20D <test-functions:otl-circuit-20d>`'s
`otl_circuit_20d.yaml` extends the original 6-marginal OTL circuit
shown above with 14 additional "inert" variables:

```yaml
      - name: beta
        distribution: uniform
        parameters: [50.0, 300.0]
        description: Current gain [A]
      - distribution: uniform
        parameters: [100.0, 200.0]
        name: Inert$idx
        description: Inert input [-]
        repeat: 14
```

This produces 20 marginals in total: the six named ones plus 14 more,
named `Inert1` through `Inert14`, matching `dimensions: input: 20`.
The `$idx` placeholder in `name` (and in `description`, if used there)
is substituted with a counter starting at 1.

Each `repeat` block counts independently, and always starts at 1; a
second `repeat` entry in the same list doesn't continue where the
first left off. There's also no way to configure a different starting
number; if you need specific numbering, spell out the entries
individually or use a factory instead.

### Template

`marginals` can also be a single dictionary defining a uniform pattern
applied to every variable, used when every input variable has the
same distribution. {ref}`Ackley <test-functions:ackley>`'s
`ackley.yaml` uses this template:

```yaml
marginals:
  distribution: uniform
  parameters: [-32.768, 32.768]
  name: X$idx
```

Only four keys are available here, exactly `Marginal`'s constructor
parameters: `distribution` and `parameters` (required), plus optional
`name` and `description`. Unlike the explicit-list shape, `repeat`
isn't among them; a template already expands to fill every dimension,
one marginal each.

The `$idx` placeholder is substituted with a counter, starting at 1,
when the marginals are expanded at build time.

```{important}
A template is a mapping, not a list. Writing

    marginals:
      - distribution: uniform
        parameters: [-32.768, 32.768]
        name: X$idx

(with the leading `-`) is a one-item explicit list, not a template: it
produces exactly one marginal, always, regardless of `input_dimension`.
Drop the list dash to get the template that expands to every variable.
```

### Factory

`marginals` can also be a dictionary containing a `factory` key, whose
value is an identifier for a callable that programmatically generates
the marginals. Use it when the parameters follow a rule too complex
for a template, such as one that depends on each variable's index.

A factory and a template are both represented as YAML mappings.
A mapping containing a `factory` key is treated as a, well, factory;
otherwise it is treated as a template.

```yaml
marginals:
  factory: create_marginals
```

{ref}`Saltelli Linear <test-functions:saltelli-linear>`'s
`saltelli_linear.yaml` declares it this way. The
`factory` value names a Python function, by default in the same-stem
`.py` file; use dot notation for a different module, for example
`factory: helpers.create_marginals`. Extra keys beyond `factory` are
passed through as keyword arguments to the function.

Here is the factory function from `saltelli_linear.py`, with its
docstring omitted for brevity:

```python
def create_marginals(input_dimension: int) -> list:
    marginals = []
    for i in range(input_dimension):
        mid = 3**i
        delta = 0.5 * mid
        marginals.append({
            "name": f"X{i + 1}",
            "distribution": "uniform",
            "parameters": [mid - delta, mid + delta],
            "description": None,
        })

    return marginals
```

Each variable gets a uniform distribution centered on $3^{i-1}$ with a
half-width of $0.5 \times 3^{i-1}$, depending on the variable's index,
exactly the kind of per-variable logic a template can't express.

```{note}
Naming the first argument `input_dimension` is how a factory receives
the dimension; omit it and the factory is called with no arguments.
Factories can also be used with fixed-dimension functions
whenever the marginal definitions are complex enough to warrant one;
in that case, `input_dimension` is usually omitted from the signature.
```

(development:yaml-specification:default-input)=
## The default input

`default_input` is a top-level key naming which input specification
to use when a function offers more than one, and no `input_id` is
given explicitly when a function is constructed (e.g.,
`uqtf.Borehole(input_id="Morris1993")` picks a specific one instead of
the default). It's only needed in that case; with a single
specification, which one to use is unambiguous, and the key can be
omitted entirely.

```yaml
default_input: Harper1983
```

See {ref}`Multiple input specifications <development:yaml-specification:multiple-input-specs>`
above for a complete worked example.

## The parameters section

`parameters` is optional, needed only when the evaluation function
takes additional fixed values beyond the input array.
{ref}`Ishigami <test-functions:ishigami>`'s `ishigami.yaml` has a
complete `parameters` block:

```yaml
parameters:
  keyword_descriptions:
    a: X2 main effect amplitude
    b: X1-X3 interaction amplitude
  sets:
    Ishigami1991:
      a: 7.0
      b: 0.1
      description: Parameter set from Ishigami and Homma (1991)
    Sobol1999:
      a: 7.0
      b: 0.05
      description: Parameter set from Sobol' and Levitan (1999)

  default_parameters: Ishigami1991
```

and the signature of the `evaluate()` function in `ishigami.py`:

```python
def evaluate(xx: np.ndarray, a: float, b: float) -> np.ndarray:
    ...
```

The keywords in each set, `a` and `b`, match `evaluate()`'s parameter
names exactly (after `xx` is stripped). Notice `description` never
appears as one of `evaluate()`'s parameters: it's a reserved key,
providing a human-readable label for the set itself, not a value
passed to the function.

`parameters` contains up to three sub-elements: a
`keyword_descriptions` block, a `sets` block, and `default_parameters`.

### `keyword_descriptions`

`keyword_descriptions` is optional, and describes what each parameter
keyword means, shared across every set: `a` means "X2 main effect
amplitude" regardless of whether its value is 7.0 or 3.0. If omitted,
parameters simply have no descriptions.

```{note}
A marginal is self-contained: name, distribution, and description all
travel together, since different input specifications may describe
the same variable differently. A parameter keyword's meaning, by
contrast, is shared across every set, only its value changes, which is
why `keyword_descriptions` exists here with no equivalent under
`inputs`.
```

### `sets`

`sets` is required whenever `parameters` is present and contains one
or more named parameter sets, each mapping keywords to values, as
already shown for Ishigami above.

Most parameter values are plain literals: numbers, strings, lists, or
nested mappings, passed through to `evaluate()` as-is. A literal can
itself be a `$()` expression instead of a bare number, covered in
{ref}`Named constants and expressions <development:yaml-specification:named-constants>`
below.

When a value must be computed by more complex logic, however,
use a factory instead as in the case of complex marginals: a dictionary
containing a `factory` key is resolved to a callable, while a
dictionary without one is treated as a literal.
{ref}`Sobol' G <test-functions:sobol-g>`'s `sobol_g.yaml` exemplifies:

```yaml
sets:
  Saltelli1995-2:
    aa:
      factory: get_aa_saltelli1995_2
    description: >-
      First two inputs most important, third moderately important,
      rest non-influential; example 2 from Saltelli and Sobol' (1995)
```

and here is the factory function from `sobol_g.py`, again without
its docstring:

```python
def get_aa_saltelli1995_2(input_dimension: int) -> np.ndarray:
    yy = np.zeros(input_dimension)

    if input_dimension > 1:
        yy[1] = 0

    if input_dimension > 2:
        yy[2] = 3

    if input_dimension > 3:
        yy[3:] = 9

    return yy
```

The factory function follows the same contract as a marginals factory:
`input_dimension` is injected as the first positional argument only if
it appears in the function's signature; otherwise the factory is called
with none.

### `default_parameters`

`default_parameters` plays the same role for parameter sets that
{ref}`default_input <development:yaml-specification:default-input>`
plays for input specifications, except that it's nested inside
`parameters` rather than living at the top level. It's required only
when `sets` contains more than one parameter set, like
Ishigami's example above, which has two (`Ishigami1991` and
`Sobol1999`) and therefore needs `default_parameters: Ishigami1991` to
say which one applies by default.

(development:yaml-specification:named-constants)=
## Named constants and expressions

Distribution parameters and literal parameter values can use `$()` to
write mathematical constants and expressions instead of bare numbers.
{ref}`Ishigami <test-functions:ishigami>`'s `ishigami.yaml` uses this
for its three marginals' bounds:

```yaml
parameters: [$(-pi), $(pi)]
```

Without the `$()` delimiter, `pi` would just be the literal string
`"pi"`, not the constant. The three supported named constants are
`pi`, `e`, and `inf`, all case-sensitive (`$(Pi)` doesn't work).

`$()` isn't limited to bare constants.
It can also evaluate a basic arithmetic expression
(`+`, `-`, `*`, `/`, `**`, unary `+`/`-`).
For instance, {ref}`Ackley <test-functions:ackley>`'s
`ackley.yaml` uses it for one of its parameter set's values:

```yaml
sets:
  Ackley1987:
    c: $(2 * pi)
```

Finally, a set of common mathematical functions is also available, listed below.

| Function                     | Description                                                                                |
|:-----------------------------|:-------------------------------------------------------------------------------------------|
| `sqrt`                       | Square root                                                                                |
| `log`                        | Natural log; `log(x, base)` for an arbitrary base                                          |
| `log2`                       | Base-2 log                                                                                 |
| `log10`                      | Base-10 log                                                                                |
| `exp`                        | Exponential                                                                                |
| `sin`, `cos`, `tan`          | Trigonometric functions                                                                    |
| `abs`                        | Absolute value                                                                             |
| `gumbel_max_mu(mean, std)`   | Convert a mean and standard deviation into the Gumbel (max.) distribution's `mu` parameter |
| `gumbel_max_beta(std)`       | Convert a standard deviation into the Gumbel (max.) distribution's `beta` parameter        | 
| `lognormal_mu(mean, std)`    | Convert a mean and standard deviation into the log-normal distribution's `mu` parameter    |
| `lognormal_sigma(mean, std)` | Convert a mean and standard deviation into the log-normal distribution's `sigma` parameter |

{ref}`Damped Oscillator <test-functions:damped-oscillator>`'s
`damped_oscillator.yaml` uses two of these to convert a mean and
standard deviation into the log-normal distribution's own
parameterization:

```yaml
parameters:
  - $(lognormal_mu(1.5, 0.1 * 1.5))
  - $(lognormal_sigma(1.5, 0.1 * 1.5))
```

```{note}
Evaluation goes through a restricted AST walker, not Python's `eval`,
so only the operators, functions, and named constants listed above are
allowed. Attribute access, unknown names or functions, and anything
else outside this whitelist raises a `SpecValidationError` rather than
silently failing or executing arbitrary code.
```

## Quick reference

Copy-paste the following skeleton (showing every available field)
as a starting point:

```yaml
# --- The preamble ---
name: str                          # REQUIRED
description: str                   # REQUIRED
tags: [str, ...]                   # REQUIRED

# --- The dimensions ---
dimensions:                        # REQUIRED
  input: int | variable            #   integer for fixed-dim, "variable" for variable-dim
  output: int                      #   OPTIONAL, default 1

# --- The evaluate directive ---
evaluate: str                      # OPTIONAL, default: evaluate in <stem>.py

# --- The inputs section ---
inputs:                            # REQUIRED, at least one entry
  <InputID>:
    description: str
    marginals:                     # One of three shapes:
      [list of marginals]          #   Explicit list (most common)
      {distribution, parameters}   #   Template (all marginals identical)
      {factory: fn_name, ...}      #   Factory (programmatic)

# --- The default input ---
default_input: str                 # REQUIRED if multiple input specs

# --- The parameters section ---
parameters:                        # OPTIONAL
  keyword_descriptions:            #   OPTIONAL: shared keyword descriptions
    <param>: description
  sets:                            #   REQUIRED if parameters present
    <SetID>:
      <param>: value               #   Literal or {factory: fn_name, ...}
      description: str             #   OPTIONAL, reserved key
  default_parameters: str          #   REQUIRED if multiple parameter sets
```
