(development:overview)=
# UQTestFuns Contributor's Guide

Contributions to UQTestFuns are very welcome!

There are many ways you can contribute:

- Adding a new test function to the code base
- Adding a new univariate distribution to the code base
- Updating the documentation
- Requesting a new test function
- Reporting and fixing a bug

If you'd like to contribute but are still unsure how,
check out the [open issues](https://github.com/damar-wicaksono/uqtestfuns/issues),
pick one, and work on it!

We expect all contributors to follow our {ref}`development:code-of-conduct`.

## Requesting a new test function

If you're missing a particular test function in UQTestFuns,
don't hesitate to ask for it by opening an issue on the [GitHub page](https://github.com/damar-wicaksono/uqtestfuns/issues)
and label it as **enhancement**.

You can fully describe the function you'd like along with the formula,
probabilistic input specification, the context of the application
(metamodeling, sensitivity analysis, reliability analysis, etc.)
and the source in the literature.
When possible write down also the reference results.

Or you can simply tell us about the source of the test function in the literature.
The source is indeed the most important part of requesting a new test function.
All test functions that are included in UQTestFuns have clear references in the literature.

## Adding a new test function

And if you'd like, feel free to implement the test function yourself,
include the documentation, and make a pull request;
we'll sure appreciate it!
Before doing so, though,
be sure to check out the guides on:

- {ref}`setting up development environment <development:setting-up-dev-env>`
- {ref}`adding a new test function implementation <development:adding-test-function-implementation>`
- {ref}`adding a new test function documentation <development:adding-test-function-docs>`
- {ref}`making a pull request <development:making-a-pull-request>`
- In case the univariate distribution types are not yet available: {ref}`adding a new univariate distribution <development:adding-univ-dist>`

## Updating the documentation

Is something missing in the docs (perhaps reference results that you know of)?
Or was something wrongly written?
Is the API documentation unclear or incomplete?
Feel free open an issue on the [GitHub page](https://github.com/damar-wicaksono/uqtestfuns/issues)
and label it as **documentation**, then either **enhancement** (if something is missing)
or **bug** (if something is wrong).

Describe briefly which part is missing or wrong then try to propose how you would write them yourself.
If you don't want to wait longer before the change happens,
don't hesitate to {ref}`make a pull request <development:making-a-pull-request>`.

Before doing so, you might want to check out how to {ref}`build the documentation locally <development:setting-up-dev-env>`.

## Reporting and fixing a bug

If you find a bug in the codebase&mdash;perhaps a wrong computation in a test function,
or even a bunch of typos in the docs&mdash;please report it by opening an issue on the [GitHub page](https://github.com/damar-wicaksono/uqtestfuns/issues) and label it as a **bug**.

When it comes to bugs in the codebase,
reproducibility is important, so please when possible provide a reproducible example that breaks the code.
Write down what did you expect to happen and what happened instead.

If you want to fix the bug yourself by a pull request, you are very welcome!

Well, that's all! Thank you for contributing to UQTestFuns!
