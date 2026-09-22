(development:how-it-works)=
# How UQTestFuns Works

This page gives contributors the rough shape of how UQTestFuns is put
together internally, for when they need to change it.

It does this in two passes. The first pass follows what actually happens
when a built-in test function is requested, from a YAML file on disk to
a ready-to-use `UQTestFun` instance. The second pass then opens this
process up further, mapping where the pieces actually live.

(development:how-it-works:flow)=
## From YAML to a UQTestFun instance

Every built-in test function is described by a YAML specification file
under `src/uqtestfuns/test_functions/` (e.g., `borehole.yaml`), paired
with a Python module of the same name (`borehole.py`) that supplies only
the evaluation logic. The YAML file declares everything else: the
function's name, description, tags, input dimensions, one or more
probabilistic input specifications (each a list of marginal
distributions), and, if the function is parameterized, one or more
parameter sets.

Getting from such a pair to a usable instance takes three stages:

1. **Scan**, at `import uqtestfuns`. A central `Registry` scans this
   directory, parses every specification file, and validates its
   structure and discovery metadata. Each valid entry becomes a
   lightweight, in-memory record for discovery: the path to its
   specification file and the metadata needed to list and describe the
   function (e.g., name, dimensions, tags). Nothing more happens at
   this stage; the paired Python module isn't imported yet, and no
   `UQTestFun` instance is built.
2. **Factory creation**, at the first lookup of a name. Looking up a
   name, whether through `uqtestfuns.create("Borehole")` or the
   shorthand `uqtestfuns.Borehole()` (both resolve through the same
   registry lookup), parses that specification in full, imports the
   paired Python module to get the evaluation function, and builds a
   factory specific to that entry. The factory is cached, so a given
   function pays for this once.
3. **Instantiation**, when the factory is called. The factory composes
   the parts into a `UQTestFun` instance: a `ProbInput` built from the
   selected input specification, and a `Parameters` set if the function
   declares any. Both default to what the specification declares, and
   callers who want one of the other available sets pick it here, which
   is what `list_inputs()` and `list_parameters()` are for.

This lazy pipeline keeps importing `uqtestfuns` reasonably lightweight
as the number of built-in functions grows, and lets `list_functions()`,
`list_parameters()`, and `list_inputs()` report on the built-ins without
constructing any of them. The last two stages are rarely visible as
separate steps, since `uqtestfuns.Borehole()` builds the factory and
calls it in one expression, but the boundary between them is where a
malformed specification surfaces, and where the second construction of
a function saves the work of the first.

(development:how-it-works:layout)=
## Package layout

Structurally, the pieces from the previous section fall into three
parts of `src/uqtestfuns/`. The three-way split is meant to be stable;
what grows over time is what sits inside each part, not the boundaries
between them.

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
  and a construction function (`create()`). New top-level convenience
  functions may land here, but this part of the package is expected to
  stay thin.

  The shorthand `uqtestfuns.Borehole()` resolves through a module-level
  `__getattr__` in the top-level `__init__.py`, not through `api.py`,
  which is why no per-function name is written down anywhere in the
  package.
- **`core/`** is where the object models and registry logic live:
  probabilistic input modeling (`Marginal` and `ProbInput` today,
  copulas once they're supported), the test function representation
  itself (`UQTestFun`, `Parameters`), and the registry and parsing
  pipeline in `core/registry/` that builds them from a YAML
  specification. New modeling capabilities (e.g., new probabilistic
  distributions) or new kinds of test function representation would
  land here. This part is expected to grow in depth.
- **`test_functions/`** is where a specific function is defined: as a
  rule, one YAML specification file and one Python module of the same
  name per built-in function, plus a handful of subpackages (`franke/`,
  `genz/`, and others) for function families that share a common input
  specification. This part is expected to grow in count, but not in
  kind, with new entries following the same pattern.

```{note}
The pairing is a convention rather than a constraint. A specification
can point at a different module through the `evaluate:` field, which
is how the variants in a family share one implementation. There is
always exactly one specification file per test function, though,
since that file is what the registry keys on.
```

To summarize: the YAML specification and its Python module live in
`test_functions/`; scanning, parsing, and the factory all happen in
`core/registry/`; the constructed `UQTestFun`, `ProbInput`, `Marginal`,
and `Parameters` objects are defined also in `core/`; and `api.py` is
where that whole pipeline gets triggered from.