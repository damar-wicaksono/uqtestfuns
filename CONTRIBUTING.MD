# Contribution Guidelines

First of all, thank you very much for taking the time to contribute
to the UQTestFuns project!

This document provides guidelines for contributing to the UQTestFuns project,
its codebase and documentation. 
These guidelines are mostly, well, guidelines;
they are not rules written on stone.
In case of doubt, use your best judgment.
Don't hesitate to propose changes to this document via an issue or 
in a pull request.

#### Table Of Contents

- [Code of Conduct](#code-of-conduct)
- [Installation](#installation)
  - [Obtaining the source](#obtaining-the-source)
  - [Virtual environments](#virtual-environments)
  - [Installing from source](#installing-from-source)
- [Testing](#testing)
- [Documentation](#documentation)
  - [Install dependencies](#install-dependencies)
  - [Building the documentation](#building-the-documentation)
  - [Design of the docs](#design-of-the-docs)
- [Project organization](#project-organization) 

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](./CODE-OF-CONDUCT.md).
By participating, you are expected to uphold this code.

## Installation

This installation guide is focused on development.
To install UQTestFuns in production runs,
please refer to the [README](./README.md).

### Obtaining the source

To get the source of the latest development,
clone the UQTestFuns repository
from [GitHub](https://github.com/damar-wicaksono/uqtestfuns):

```bash
$ git clone https://github.com/damar-wicaksono/uqtestfuns.git
```

By default, the cloned branch is the `dev` branch.

We recommend to always pull the latest commit:

```bash
$ git pull origin dev
```

### Virtual environments

Following a best practice in Python development,
we strongly encourage you to create and use virtual environments
for development and production runs.
A virtual environment encapsulates the package and all its dependencies
without messing up your other Python installations.

The following instructions should be executed
from the UQTestFuns source directory.

#### Using [venv](https://docs.python.org/3/tutorial/venv.html)

Since v3.5, Python includes `venv` module to create virtual environments.
To create a virtual environment using the `venv` module:

1. Build a virtual environment:

  ```bash
  python -m venv <your_venv_name>
  ```

   Replace `<you_venv_name>` with an environment name of your choice.

2. Activate the environment you just created:

    ```bash
    source <your_venv_name>/bin/activate
    ```

    as before replace `<you_venv_name>` with the environment name.

3. To deactivate the virtual environment, type:

    ```bash
    deactivate
    ```

#### Using [conda](https://conda.io/projects/conda/en/latest/index.html)

You may also create a virtual environment via `conda` which is included in
the Anaconda distribution of Python.
The following assumed that you've successfully installed `conda`:

1. Create a virtual environment using [conda]https://conda.io/projects/conda/en/latest/index.html)
   
   ```bash
   conda env create -n <your_env_name>
   ```   

   Replace `<your_env_name>` with an environment name of your choice.
 
2. Activate the new environment with:
    
   ```bash
   conda activate <your_env_name>
   ```
 
   As before, replace `<your_env_name>` with the environment name chosen in the first step.

3. To deactivate the conda environment, type:

    ```bash
    conda deactivate
    ```

### Installing from source 

To install UQTestFuns, we recommend using [pip](https://pip.pypa.io/en/stable/)
from within a virtual environment.
To install UQTestFuns from source, type:

```bash
$ pip install -e .[all,dev,docs]
```

where the flag `-e` means the package is directly linked into the Python site-packages.
The options `[all,dev,docs]` refer to the requirements defined
in the `options.extras_require` section in `setup.cfg`.

## Testing

Running the test suite requires a specific set of dependencies.
If you install UQTestFuns using either the option `[dev]` or `[all]`,
these dependencies are satisfied.

UQTestFuns project uses [pytest](https://docs.pytest.org/en/6.2.x/)
to run the test suite.
The test suite are located inside the `tests` directory;
all future tests must be placed inside this directory.

To run all tests, type:

```bash
$ pytest
```

from within the UQTestFuns source directory.

## Documentation

This section provides some information about contributing to the docs.

### Install dependencies

Building the docs from source requires additional dependencies.
If you install UQTestFuns using either the option `[docs]` or `[all]`
these dependencies are satisfied.

### Building the documentation

We use [Jupyter Book](https://jupyterbook.org/en/stable/intro.html)
to build the UQTestFuns docs.
To build the docs in HTML format, run the following command:

```bash
jupyter-book build docs
```

from within the UQTestFuns source directory.

The command builds the docs and stores it in `docs/_build`.
You may open the docs locally using a web browser of your choice
by opening the file `docs/_build/html/index.html`.

### Design of the docs

The source files for the docs are stored in the `docs` directory.
The Jupyter Book configuration file is `docs/_config.yml`
and the table of contents file is `docs/_toc.yml`.

The docs itself contains six different main sections:

- The landing page of the docs (`docs/index.md`)
- The Getting Started Guide (`docs/getting-started`)
- The Available Test Functions (`docs/test-functions`)
  contains the documentation for each of the available test functions
  in UQTestFuns. Each test function has its own documentation file.
- The Fundamentals (`docs/fundamentals`) contains explanations
  on the main uncertainty quantification (UQ) activities.
  This is related to how the test functions are classified based
  on their applications.
- The Contributor's Guide (`docs/development`) contains the information
  on UQTestFuns development and how to contribute to the project.
- The API Reference (`docs/api`) contains the reference
  to all exposed components of UQTestFuns (functions, classes, etc.).

Additionally, the `docs` directory also includes `references.bib`
(the bibliography file) and `glossary.md` (well, the glossary).

## Project organization

```
.
├── .github/                <- The GitHub actions specifications.
├── .gitignore              <- List of ignored files/directories if `git add/commit`
├── .readthedocs.yml        <- Configuration for readthedocs
├── AUTHORS.md              <- List of developers and maintainers
├── CODE-OF-CONDUCT.md      <- Code of conduct adopted by the project.
├── CONTRIBUTING.md         <- (Brif) contribution guidelines
├── docs                    <- The docs (*.md or *.rst files)
├── LICENSE                 <- The license file
├── MANIFEST.in             <- Keep track of (minimal) source distribution files
├── pyproject.toml          <- Specification build requirements
├── README.md               <- The top-level README
├── setup.cfg               <- Declarative configuration of your project
├── src
│   └── uqtestfuns          <- Actual Python package where the main functionality goes
└── tests                   <- Test suite which can be run with `pytest`
```
