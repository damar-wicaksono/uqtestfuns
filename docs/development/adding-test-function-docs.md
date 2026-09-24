---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(development:adding-test-function-docs)=
# Adding a New Test Function Documentation

Each of the uncertainty quantification (UQ) test functions in UQTestFuns
has a dedicated page in the documentation detailing its description,
probabilistic input specification, parameters (when applicable),
reference results (when available), and bibliographic citations.
In this guide, we will explain how to create
and add new test function documentation into the UQTestFuns codebase.

```{note}
Before moving on, make sure you've set up a local development environment
for building the documentation as explained {ref}`here <development:setting-up-dev-env>`.
```

The walkthrough below picks up where we {ref}`left off <development:adding-test-function-implementation>`,
after adding a new test function (the Branin function) to the codebase.
We are now ready to create the documentation for it.

## Step 0: Putting things in the right place

Test function documentation in UQTestFuns is written as a
[MyST-NB](https://myst-nb.readthedocs.io/en/latest/) file, a
[Jupyter Book](https://jupyterbook.org/en/stable/intro.html) document
that stores a notebook's cells as a plain-text `.md` file rather than
a JSON `.ipynb`, so it's easy to edit in a text editor while still
being executable like a real notebook. Unlike a `.ipynb` file, though,
cell output is never stored in the file itself; it's regenerated every
time the documentation is built.

Test function documentation is stored inside `docs/test-functions`
(with respect to the source root directory). If you have a look at
the directory, you'll see the following
(or something similar as things may have developed a bit):

```text
docs/test-functions/              <- Documentation for every UQ test function
├── ackley.md                     <- Documentation for the Ackley function
├── ...
└── wing-weight.md                <- Documentation for the wing weight function
```

For the Branin function, add `branin.md` to this directory (good
naming, by the way).

## Step 1: Writing the documentation

Now you're ready to write the actual documentation for the Branin test function.
Here are the elements of a documentation source file, in the order we'll walk through them:

- Top-matter
- Title
- Opening paragraph
- Package imports
- (Optional) Illustration plots
- Test function instance
- Description
- (Probabilistic) Input
- Parameters
- Reference results
- References

### Top-matter

To tell Jupyter Book that your markdown file is a MyST-NB document,
specify the top-matter, an embedded YAML snippet, at the very top of
the file:

```yaml
---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---
```

### Title

Right after the top-matter comes the title.
Pick one that's appropriate for the test function;
be straightforward and use your common sense.
For the Branin function, a simple title is a good choice:

```text
(test-functions:branin)=
# Branin Function
```

Notice the MyST-NB labeling of the document (`(test-functions:branin)=`).
This label is used to cross-reference the document from somewhere else.
The general format for the label adopted by UQTestFuns is:

```text
(test-functions:<test-function-name>)=
```

where `<test-function-name>` is the function's name in lowercase,
hyphenated form, not necessarily the same as the document title. A
few examples from the codebase:

| Function name | Document title                                                   | Label                         |
|:--------------|:-----------------------------------------------------------------|:------------------------------|
| `Borehole`    | Borehole Function                                                | `test-functions:borehole`     |
| `Ackley`      | Ackley Function                                                  | `test-functions:ackley`       |
| `SobolG`      | Sobol'-G Function                                                | `test-functions:sobol-g`      |
| `OTLCircuit`  | OTL Circuit Model from Ben-Ari and Steinberg (2007)              | `test-functions:otl-circuit`  |
| `Forrester1D` | One-dimensional Multimodal Function from Forrester et al. (2008) | `test-functions:forrester-1d` |

```{tip}
Crediting the source in the title itself isn't a hard requirement.
A well-known function like Ackley, Sobol'-G, or Borehole is
recognizable by name alone, while a less prominent one can benefit from
a citation-style title that also states where it came from.

Again, this is not a hard requirement.
```

### Opening paragraph

The opening paragraph should provide a one- or two-sentence summary about the test function.
Here's an example for the Branin function:

```{admonition} Opening paragraph
:class: tip

The Branin (also Branin-Hoo) function is a two-dimensional scalar-valued function.
The function was first introduced in {cite}`Dixon1978` as an optimization test function.
```

A few best practices, drawn from examples already in the documentation:

- State the function's dimensionality and output type up front, e.g.
  "a three-dimensional scalar-valued function."
- Cite where it was first introduced, and, if relevant, where it was
  later revisited, generalized, or renamed; see
  {ref}`Ishigami <test-functions:ishigami>` or
  {ref}`Sobol' G <test-functions:sobol-g>` for functions with a longer
  history.
- Mention the context it's typically used in (optimization,
  sensitivity analysis, metamodeling, etc.) if that adds useful
  orientation beyond the citation itself.
- Keep it to one or two sentences; save the details for the
  Description section.

### Package imports

After the opening paragraph, import the required Python packages.
Remember that the documentation is executable and doubles as a usage example.
The code snippets that appear in the document will be executed
when the whole documentation is built.

Import the common packages as follows:

````
```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```
````

Note that any executable code snippets in the documentation must be enclosed inside a _code cell_ directive block with `ipython3` as the argument.

### (Optional) Illustration plots

If the test function is either one-dimensional or two-dimensional,
include a plot of the function in its domain.
For two-dimensional functions, provide a surface and contour plot.
See, for example, the {ref}`Forrester1D <test-functions:forrester-1d>` function
and the {ref}`(1st) Franke <test-functions:franke-1>` function.

You can put the code to create the plot directly in the document,
but don't show the code in the rendered output.
To do that, put `:tags: [remove-input]` at the beginning of the code-cell block.

### Test function instance

Show how to create an instance of the test function.
Then print it as a quick sanity check.

`````{admonition} Test function instance
:class: tip

To create a default instance of the Branin function:

````
```{code-cell} ipython3
my_testfun = uqtf.Branin()
```
````

Check if it has been correctly instantiated:

````
```{code-cell} ipython3
print(my_testfun)
```
````
`````

### Description

Then describe the test function briefly in its own section.
When available, provide the analytical formula of the function.

```{admonition} Description
:class: tip

The analytical expression of the Branin function is given below:

$$
\mathcal{M}(x_1, x_2) = a \left( x_2 - b x_1^2 + c x_1 - r \right)^2 + s \left(1 - t \right) \cos{(x_1)} + s
$$

where $x_1$ and $x_2$ are the input variables
and $\{ a, b, c, r, s, t \}$ are the parameters.
```

### (Probabilistic) Input

Provide the specification of the inputs in its own section after the description.
By convention, for traditional optimization test functions, we name the section simply as **Input**
(as opposed to **Probabilistic input** for other UQ test functions).
This is because for such a function, the input specification defines a search space rather than a meaningful probability distribution, so the marginals' distributions don't matter as much.

Printing the test function's attached `ProbInput` instance renders it
as a tabulated summary of its marginals.

`````{admonition} Input
:class: tip

The default search domain of the Branin function is given in the table below.

````
```{code-cell} ipython3
print(my_testfun.prob_input)
```
````
`````

### Parameters

If the test function is parametrized, provide the values and their references in this section.

````{admonition} Parameters
:class: tip

The Branin function requires six additional parameters to complete the specification.
The recommended (and default) values are
$a = 1.0$, $b = \frac{5.1}{(2 \pi)^2}$, $c = \frac{5}{\pi}$, $r = 6$, $s = 10$, and $t = \frac{1}{8 \pi}$ {cite}`Dixon1978`.
```` 

### Reference results

Add the available reference results in a new section.
For an optimization test function like the Branin function,
the optimum value(s) and their location(s) are typically given.
For other test functions, estimated/analytical moments,
the convergence of metamodeling exercises, etc. may be of interest.

```{admonition} Reference results
:class: tip

The Branin function has global optima of the same value at three different locations:

$$
\begin{align}
  \mathcal{M}(\boldsymbol{x}^*) & = 0.397887 \\
  \boldsymbol{x}^*_1  & = (-\pi, 12.275) \\
  \boldsymbol{x}^*_2  & = (\pi, 2.275)\\
  \boldsymbol{x}^*_3  & = (9.42478, 2.475)\\
\end{align}
$$
```

### References

Finally, put the list of references at the end of the document.

The code:

````text
```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```
````

will be rendered as:

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

## Step 2: Registering the documentation

Once you're done writing the document,
make it available in the documentation by modifying these files:

- `docs/_toc.yml`
- `docs/test-functions/available.md`
- `docs/fundamentals/[metamodeling, optimization, sensitivity, reliability, integration].md`,
  whichever is relevant for the test function
- `docs/references.bib`, if the function's references aren't already there

Follow the example of other test functions already in the documentation.

## Step 3: Building the documentation

You're now ready to build your updated documentation.
Assuming you've set up the development environment
for building the documentation, execute:

```bash
$ jupyter-book build docs
```

from the UQTestFuns source root directory.

Check the terminal output for warnings, a broken `{ref}`/`{cite}` link,
a citation-key typo, unrendered LaTeX, or a failed code cell all show
up there. Then open the newly built page,
`docs/_build/html/test-functions/branin.html`, in a browser and
confirm it looks right: the formula renders, the plot (if any)
appears, and the References section lists the citation you used.

---

Congratulations!

You've successfully written and added documentation
for a new test function to the codebase.

If you want to make the new test function and its documentation available
to everybody, don't hesitate to make a pull request on the main UQTestFuns
repository.
This {ref}`guide <development:making-a-pull-request>` will help you with that.
