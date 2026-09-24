(development:making-a-pull-request)=
# Making a Pull Request

Whether you add a new test function or fix a typo in the documentation,
you should make your code contributions to UQTestFuns
via the pull request (PR) mechanism to the `dev` branch on GitHub.

Your pull request must be made from a forked repository in your own account.
Please refer to {ref}`development:setting-up-dev-env`
for more details on setting up the fork.

Please keep a PR as compact as possible;
each contains only an enhancement or a fix at a time.
However, adding a test function, the documentation,
and the corresponding tests should be a single PR.

## Before making a pull request

To ensure a minimum coding standard, we use
[Flake8](https://github.com/PyCQA/flake8) as our code linter,
[Black](https://github.com/psf/black) as our code formatter, and
[mypy](https://mypy-lang.org/) for static type checking. All three are
made available if you installed the package with `pip` using the
`dev` or `all` extra. Make sure you run them on the updated code
before you make a pull request.

Execute `flake8` from the source root directory:

```bash
$ flake8 src tests
```

and fix any issues that it raised.

We usually avoid allowing Black to directly modify the source code.
Instead, we ask it to check and make the recommendations and run it as follows:

```bash
$ black --check --diff src tests
```

Fix any formatting issues that Black raised manually.

Execute `mypy` from the source root directory:

```bash
$ mypy --ignore-missing-imports src tests
```

and fix any type errors that it raised.

Finally, make sure you run `pytest` and resolve any issues
before making the pull request.

## Creating a pull request

Once you're happy with your local changes and ready to make a pull request,
push them to your own remote repository on GitHub:

```bash
$ git push origin <my-development-branch>
```

where it is assumed that you've been making the changes
in a separate branch called `my-development-branch`.

Create the PR via the GitHub interface and use the `dev` branch
of the main repository as the target branch.
Remember to briefly explain your PR.

---

That’s it! You've made your PR! Please wait until someone handles it.
