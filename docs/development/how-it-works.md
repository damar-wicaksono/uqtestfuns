(development:how-it-works)=
# How UQTestFuns Works

This page gives contributors the rough idea of how UQTestFuns is put
together internally, which may be helpful when they need to change it.

The first part follows the path from a YAML specification
to a `UQTestFun` instance.
The second part then looks at where the pieces actually live
and how they relate to each other.

(development:how-it-works:flow)=
## From YAML to a UQTestFun instance

Two things describe all built-in test functions:

- a function inside a Python module (e.g., `borehole.py`) that supplies
  the evaluation logic of a test function
- a YAML specification file (e.g., `borehole.yaml`) that declares everything
  else, including the function's name, description, tags, input dimensions,
  probabilistic input specifications, etc.

Getting from such a pair to a usable instance happens in three stages:

1. **Scan**, when the package is imported. A central `Registry` scans this
   directory, parses every specification file, and validates its
   structure and discovery metadata. Each valid entry becomes a
   lightweight, in-memory record for discovery: the path to its
   specification file and the metadata needed to list and describe the
   function (e.g., name, dimensions, tags). At this stage, the paired Python 
   module isn't imported yet and no `UQTestFun` instance is constructed.

2. **Factory creation**, when a function is looked up for the first time by its name.
   Looking up a name, whether through `uqtestfuns.create("Borehole")` or the
   shorthand `uqtestfuns.Borehole()`[^resolution],
   parses that specification in full and builds a factory specific to that entry.
   The factory is cached, so repeated requests reuse the cached factory
   instead of parsing the specification again.

3. **Instantiation**, when the factory is called. First, it imports the paired 
   Python module to get the evaluation function. Then it
   builds a `ProbInput` from the selected input specification,
   and, if applicable, a `Parameters` set.
   Finally, these three objects are combined into a `UQTestFun` instance.

   Both `ProbInput` and `Parameters` default to what the specification declares; 
   users can discover alternatives with `list_inputs()` and `list_parameters()`.
   
This lazy pipeline keeps importing `uqtestfuns` reasonably lightweight
as the number of built-in functions grows, and lets `list_functions()`,
`list_parameters()`, and `list_inputs()` report on the built-ins without
constructing any of the instances.

```{note}
The last two stages are rarely visible as separate steps,
because calling `uqtestfuns.<function-name>()` builds
the function factory and calls it in one expression.
```

(development:how-it-works:layout)=
## Package layout

Structurally, the pieces introduced in the previous section fall into three
parts of the source code (i.e., `src/uqtestfuns/`) illustrated below.

```{mermaid}
flowchart TD
    init["__init__.py<br/>uqtestfuns.Borehole()"]
    api["api.py<br/>create(), list_functions(), ..."]
    core["core/<br/>object model + registry"]
    tf["test_functions/<br/>YAML + Python specs"]

    init -->|"attribute lookup"| core
    api -->|"calls / returns a UQTestFun"| core
    core -->|"scans at import, reads specs on demand"| tf
```

- **`api.py`** is the user-facing surface: a set of top-level discovery
  functions (`list_functions()`, `list_parameters()`, `list_inputs()`)
  and a construction function (`create()`). While new top-level convenience
  functions may be implemented here, this part of the package is expected to
  stay thin.

```{note}
The shorthand `uqtestfuns.Borehole()` resolves through a module-level
`__getattr__` in the top-level `__init__.py`, not through `api.py`,
which is why no per-function name is written down anywhere in the
package.
```

- **`core/`** is where the object models (`Marginal`, `ProbInput`,
  `UQTestFun`, `Parameters`) and the registry/parsing pipeline
  (`core/registry/`) live. New modeling capabilities (e.g., new
  probability distributions) or new kinds of test function
  representation would be implemented here. This part is expected to
  grow in depth.

- **`test_functions/`** is where a specific function is defined. As a
  general rule, one YAML specification file is paired with one Python
  module of the same name. For a family of functions (e.g., `franke/`,
  `genz/`), each member still gets its own YAML file, but they point
  at a shared Python module and a shared input specification. This
  part is expected to grow in count, with new entries following the
  same pattern.

New functionality should generally fit within these boundaries
rather than introducing another layer[^never].

```{note}
The pairing is a convention rather than a constraint. A specification
can point at a different module through the `evaluate:` field, which
is how the variants in a family share one implementation. There is
always exactly one specification file per test function, though,
since that file is what the registry keys on.
```

[^resolution]: both of these approaches resolve through the same registry lookup
[^never]: We, however, never say never