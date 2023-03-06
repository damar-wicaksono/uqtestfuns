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

```{margin}
A UQ test function without a corresponding documentation page does not exist
```

Each of the uncertainty quantification (UQ) test functions in UQTestFuns
has a dedicated page in the docs detailing their description, probabilistic input specification,
parameters (when applicable), reference results (when available), and bibliographic citations.
In this guide, we will explain how to create and add a new test function documentation into the UQTestFuns code base.

```{note}
Before moving on, make sure you've set up a local development environment
for building the docs as explained {ref}`here <development:setting-up-dev-env>`.
```

The walkthrough below picks up where we {ref}`left off <development:adding-test-function-implementation>`, 
after implementing a new test function (the Branin function) to the code base.
We are now ready to create the documentation for it.

## Step 0: Putting things in the right place

The UQTestFuns docs is built using [Jupyter Book](https://jupyterbook.org/en/stable/intro.html).
A test function documentation in UQTestFuns is written
in a [MyST-NB](https://myst-nb.readthedocs.io/en/latest/) text-based notebook file (with an `.md` extension).
This allows you to embed Python code directly into a markdown text file;
you can edit such a file easily in a text editor (it's not a JSON file) but readily run in a Python environment just like a Jupyter notebook.
Unlike a Jupyter notebook,
the output of the executed codes you put in the document will not be stored in the document itself.

The test function documentation is stored inside the `docs/test-functions` directory (with respect to the source root directory).
If you have a look at the directory you'll see the following (or something similar):

```text
docs/
├── ...
└── test-functions              <- Directory that contains all test functions documentation
    ├── ackley.md               <- Documentation for the Ackley function
    ├── ...
    └── wing_weight.py          <- Documentation for the wing weight function
```

Let's assume you've named the documentation file explaining the Branin function as `branin.md` (good naming).
You need to put that file inside this directory (that is, `docs/test-functions`)

## Step 1: Writing the documentation

Now you're ready to write the actual documentation for the Branin test function.
We suggest the following structure for the documentation:

- Opening paragraph
- Test function instance
- Description
- (Probabilistic) Input
- Parameters
- Reference results
- References

### Top-matter

MyST-NB is a special text document; it stores a Jupyter notebook inside a (markdown) text file but without the output.
To tell Jupyter Book that your markdown text file is indeed a MyST-NB document you need to specify the top-matter
(basically an embedded YAML snippet):

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
Pick one that's appropriate for the test function; be simple and use your common sense. 
If the documentation is about the Branin function,
it might be a good idea to title your document:

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

Replace `<test-function-name>` with the actual name of the test function.

### Opening paragraph

The opening paragraph should provide a one- or two-sentence summary about the test function.
Give a reference to where it was first introduced and some records of its usage in the literature.
Here's an example of the Branin function:

```{admonition} Opening paragraph
:class: tip

The Branin (also Branin-Hoo) function is a two-dimensional scalar-valued function.
The function was first introduced in {cite}`Dixon1978` as an optimization test function.
```

### Package imports

After the opening paragraph, import the required Python packages.
Remember that the documentation is an executable document that serves as an example document.
The code snippets that appear in the document will be executed when the whole docs is built.

Import the common packages as follows:

````
```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```
````

Note that any executable code snippets in the docs must be enclosed inside a _code cell_ directive block with `ipython3` as the argument.

### (Optional) Illustration plots

If the test function is either one-dimensional or two-dimensional,
include a plot of the function in its domain.
For two-dimensional functions, provide a surface and contour plot.

You can put directly the code to create the plot in the document,
but don't show the code in the rendered document.
To do that, put `:tags: [remove-input]` at the beginning of the code-cell block.

For example:

````
```{code-cell} ipython3
:tags: [remove-input]

# Do the plotting here
```
````

### Test function instance

Provide an example of how an instance of the particular test function can be instantiated.
Print the test function instance afterward as a simple verification step.

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
\mathcal{M}(x_1, x_2) = a \left( x_2 - b x_1^2 + c x_1 - r \right)^2 + s \left(1 - t \right) \cos{(x_1}) + s
$$

where $x_1$ and $x_2$ are the input variables
and $\{ a, b, c, r, s, t \}$ are the parameters.
```

### (Probabilistic) Input

Provide the specification of the inputs in its own section after the description.
By convention, for traditional optimization test functions, we name the section simply as **Input**
(as opposed to **Probabilistic input** for other UQ test functions).
This is because for such a function the input specification is actually a search space specification and the distributions don't usually matter.

If you call the attached `ProbInput` instance of the test function in the Jupyter Python terminal,
HTML output will be automatically printed out.

`````{admonition} Input
:class: tip

The default search domain of the Branin function is given in the table below.

````
```{code-cell} ipython3
my_testfun.prob_input
```
````
`````

### Parameters

If the test function is parametrized, provide the values and their references in this section.

````{admonition} Parameters
:class: tip

The Branin function requires six additional parameters to complete the specification.
The recommended (and default) values are
$a = 1.0$, $b = \frac{5.1}{(2 \pi)^2}$, $c = \frac{5}{\pi}$, $r = 6$, $s = 10$, and $\frac{1}{8 \pi}$ {cite}`Dixon1978`.
```` 

### Reference results

Add the available reference results in a new section.
For an optimization test function like the Branin function,
the optimum value(s) and its location(s) are typically given.
For other test functions, estimated/analytical moments, the convergence of metamodeling exercises, etc. may be of interest.

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
:style: plain
:filter: docname in docnames
```
````

will be rendered as:

```{bibliography}
:style: plain
:filter: docname in docnames
```

## Step 2: Adding the documentation

Once you're done writing the document,
make it available in the docs by modifying these files:

- `docs/_toc.yml`
- `docs/test-functions/available.md`
- `docs/fundamentals/[metamodeling, optimization, sensitivity].md` whichever relevant for the test functions

Follow the example of the other test function already in the docs.

## Step 3: Building the documentation

You're now ready to build your updated documentation.
Assuming you've set up the development environment for building the docs,
execute:

```bash
$ jupyter-book build docs
```

from the UQTestFuns source root directory.

---

Congratulations!
You've successfully created and added a new test function documentation to the code base.

If you want to make the new test function and its documentation available
to everybody, don't hesitate to make a pull request on the main UQTestFuns
repository. This {ref}`guide <development:making-a-pull-request>` will help you with that.
