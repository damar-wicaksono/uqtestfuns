(development:making-a-pull-request)=
# Making a Pull Request

Whether you add a new test function or fix a typo in the docs,
you should make your code contributions to UQTestFuns via the pull requests (PR) mechanism to the `dev` branch on GitHub.

Your pull request must be made from a forked repository in your own account.
Please refer to {ref}`development:setting-up-dev-env` for more details on setting up the fork.

Please keep a PR as compact as possible; each contains only an enhancement or a fix at a time.
However, adding a test function, the documentation, and the corresponding tests should be a single PR.

To ensure a minimum coding standard you should conform to the adopted code linting and formatter of the project.
Make sure you run these tools on the updated code before you make a pull request.

## Before making a pull request

We use [Flake8](https://github.com/PyCQA/flake8) as our code linter.
The tool is made available if you installed the package with `pip` using `.[dev]` or `.[all]` flag.

Execute `flake8` from the source root directory:

```bash
$ flake8 src tests
```

and fix any issues that it raised.

We also use [Black](https://github.com/psf/black) as our code formatter.
It is also made available if you installed the package using `.[dev]` or `.[all]` flag.

We usually avoid allowing Black to directly modify the source code.
Instead, we ask it to check and make the recommendations and run it as follows:

```bash
$ black --check --diff src tests
```

Fix any formatting issues that Black raised manually.

Finally, make sure you run `pytest` and resolve any issues before making the pull request.

## Creating a Pull-Request

Once you're happy with the local development and would like to make a pull request for it,
push all the local changes to your own remote repository on GitHub:

```bash
$ git push origin <my-development-branch>
```

where it is assumed that you've been making the changes in a separate branch called `my-development-branch`.

Create the PR via the GitHub interface and use the `dev` branch of the main repository as the target branch.
Don't forget to briefly explain your PR.

---

That’s it! You've made your PR! Please wait until someone handles it.
