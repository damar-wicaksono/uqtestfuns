(development:setting-up-dev-env)=
# Setting Up a Development Environment

This guide helps you set up a development environment in your local machine
so you can start contributing to UQTestFuns.

We assume you're familiar with basic command line operations as well as the 
Git version control system.

## Forking the repository

If you plan to eventually make a pull request of your code change to UQTestFuns
repository, you have to create a fork of the repository to your own GitHub account.
Afterward, clone your fork to your local machine:

```bash
$ git clone https://github.com/<your-github-username>/uqtestfuns.git
```

Then, work the changes in this (cloned) fork.

If you want to keep the fork up-to-date with the main UQTestFuns repository,
set up multiple remotes for your repository.

Add an upstream repository that points to the main UQTestFuns repository:

```bash
git remote add upstream https://github.com/damar-wicaksonop/uqtestfuns
```

This way you have access to the main repository.
To fetch the changes in the upstream (main) repository, execute:

```bash
$ git fetch upstream
```

To have a local branch that mirrored the main repository `dev` branch, execute:

```bash
$ git checkout -b uqtestfuns-upstream-dev upstream/dev
```

## Obtaining the source

We recommend you get the latest source
as the starting point of your contribution.
Get the source code
from the [GitHub](https://github.com/damar-wicaksono/uqtestfuns)
repository:

```bash
$ git clone https://github.com/damar-wicaksono/uqtestfuns.git
```

The default branch is the `dev` branch.

Be sure to always pull the latest commit:

```bash
$ git pull origin dev
```

## Project organization

Once you cloned the UQTestFuns repository into your local system,
you should be able to see the following directory structure:

```text
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

## Virtual environments

Following a best practice in Python development,
we strongly encourage you to create and use virtual environments 
for development runs.
A virtual environment encapsulates the package and all its dependencies
without messing up your other Python installations.

Do this before you install the package.

There are many ways of setting up a virtual environment within the Python community.
Below we give examples using [`venv`](https://docs.python.org/3/tutorial/venv.html)
the built-in virtual environment manager for Python
as well as [`conda`](https://conda.io/projects/conda/en/latest/index.html)
a popular open-source package and environment management system.

We assume that all the example commands given below are executed from the UQTestFuns
root source directory.

#### Using `venv`

Since v3.5, Python includes `venv` module to create and manage virtual environments.
To set up a virtual environment using the `venv` module:

1. Create a virtual environment:
   ```bash
   $ python -m venv <your_venv_name>
   ```
   Replace `<you_venv_name>` with an environment name of your choice.

2. Activate the environment you just created:
    ```bash
    $ source <your_venv_name>/bin/activate
    ```
    as before replace `<you_venv_name>` with the environment name.

3. To deactivate the virtual environment, type:
    ```bash
    $ deactivate
    ```

#### Using `conda`

You may also create a virtual environment via [`conda`](https://conda.io/projects/conda/en/latest/index.html)
which is included in the [Anaconda distribution of Python](https://www.anaconda.com/).
The following assumed that you've successfully installed `conda` in your system:

1. Create a virtual environment using `conda`:
   
   ```bash
   $ conda env create -n <your_env_name>
   ```   

   Replace `<your_env_name>` with an environment name of your choice.
 
2. Activate the new environment with:
    
   ```bash
   $ conda activate <your_env_name>
   ```
 
   As before, replace `<your_env_name>` with the environment name chosen in the first step.

3. To deactivate the `conda` environment, type (from anywhere):

    ```bash
    $ conda deactivate
    ```

## Installing UQTestFuns from the source

To install UQTestFuns, we recommend using [pip](https://pip.pypa.io/en/stable/)
from within a virtual environment.
To install UQTestFuns from the source, type:

```bash
$ pip install -e .[all,dev,docs]
```

where the flag `-e` means the package is directly linked to the Python site-packages.
The options `[all,dev,docs]` refer to the requirements defined
in the `options.extras_require` section in `setup.cfg`.

## Testing

Running the test suite requires a specific set of dependencies.
If you install UQTestFuns using either the option `[dev]` or `[all]`,
these dependencies are satisfied.

UQTestFuns project uses [pytest](https://docs.pytest.org/en/6.2.x/)
to run the test suite.
The test suite is located inside the `tests` directory;
all future tests must be placed inside this directory.

To run all tests, type:

```bash
$ pytest
```

from within the UQTestFuns source directory.

## Building the documentation

Building the docs from the source requires additional dependencies.
If you install UQTestFuns using either the option `[docs]` or `[all]`
these dependencies are satisfied.

We use [Jupyter Book](https://jupyterbook.org/en/stable/intro.html)
to build the UQTestFuns docs.
To build the docs in HTML format, execute the following command:

```bash
$ jupyter-book build docs
```

from within the UQTestFuns root source directory.

The command builds the docs and stores them in `docs/_build`.
You may open the docs locally using a web browser of your choice
by opening the file `docs/_build/html/index.html`.

The source files for the docs are stored in the `docs` directory.
Here is what the directory structure should look like:

```text
.
│   glossary.md                    <- Well, the glossary
│   index.md                       <- The landing page of the docs
│   references.bib                 <- Bibliography file (BibTeX format)
│   _config.yml                    <- Jupyter book configuration file
│   _toc.yml                       <- Jupyter book table of contents file
│
├───api/                           <- API references to all exposed interfaces
├───development/                   <- The Contributor's Guide
├───fundamentals/                  <- Fundamentals Guide
├───getting-started/               <- Getting Started Guide
├───prob-input/                    <- Probabilistic input modeling
│   │   ...
│   │
│   └───univariate-distributions/  <- Docs for each univariate distribution
│
└───test-functions/                <- Docs for each UQ test function
``` 
