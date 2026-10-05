# Obtaining and Installing UQTestFuns

```{note}
UQTestFuns requires **Python 3.10 or newer**.
```

You can obtain UQTestFuns directly from PyPI using `pip`:

```bash
$ pip install uqtestfuns
```

Alternatively, you can install the latest version directly from the source,
including changes not yet published to PyPI:

```bash
$ pip install git+https://github.com/damar-wicaksono/uqtestfuns.git
```

```{note}
UQTestFuns is developed very actively between releases: the command above
installs from the `dev` branch, which is often ahead of the version on
PyPI. See the
[CHANGELOG](https://github.com/damar-wicaksono/uqtestfuns/blob/dev/CHANGELOG.md)
for what has changed since the last release.
```

```{important}
UQTestFuns is currently a work in progress,
therefore the interfaces are subject to change, at least until v1.0.0
is finally released.
```

It's a good idea to install the package in an isolated virtual environment;
see {ref}`Setting Up a Development Environment <development:setting-up-dev-env>`
for `venv`/`conda` instructions (the same steps apply whether or not you
plan to contribute).

To verify the installation, run:

```bash
$ python -c "import uqtestfuns; print(uqtestfuns.__version__)"
```

which should print the installed version number.
