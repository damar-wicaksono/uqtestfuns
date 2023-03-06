(development:about-uqtestfuns)=
# About the UQTestFuns Project

UQTestFuns is an homage to the
[Virtual Library of Simulation Experiments: Test Functions and Datasets] (VLSE).

For many years this site has been very useful in providing
the uncertainty quantification (UQ) community 
with test functions and datasets from the literature.
It is very well organized, describing each of the test functions
briefly but clearly, and making proper citations to the sources
of the test functions.
It even includes implementations both in MATLAB and R.

But it has been a long time since the site was updated,
and it is not very clear how other people can contribute to the site,
say, to add a new test function or an implementation in languages 
other than MATLAB and R.

For instance, we are currently developing a software package written in Python
that is hopefully relevant to the UQ community.
For testing, we find ourselves reimplementing the test functions
and the corresponding input specification in Python.
Indeed, many UQ tools (in Python or other languages) include
a subset of the test functions
available in [VLSE] for testing, benchmarking, and illustration purposes.

Instead of doing the same thing, we opted to distribute the collection of
the test functions we have implemented as a Python package 
with a consistent interface.
The package can then be installed and imported as needed
by other packages (including our own) for testing and benchmarking purposes.

Test functions in applied UQ are unique due to the specifications of the input
as random variables.
In UQTestFuns, the input specification is an integral part of all the available
test functions.
With a common interface, realizations from probabilistic inputs can be
conveniently generated or transformed from and to the domain of the function.

The package documentation, available online, serves as
a library of UQ test functions similar to the [VLSE]
(but with implementations in Python).
While it may not always be possible, we also try to include
the relevant reference values for common UQ analyses
(e.g., metamodeling, sensitivity analysis, moments estimation error)
associated with the test functions available in the literature.

As an open-source project, UQTestFuns tries to provide clear guidance for all 
on how to contribute to it, fixing broken things, and adding new stuff&mdash;be
it a new test function, new reference values, or a better description.

We hope UQTestFuns can be useful for the UQ community,
just as the [VLSE] has been very useful to us.

[Virtual Library of Simulation Experiments: Test Functions and Datasets]: https://www.sfu.ca/~ssurjano/
[VLSE]: https://www.sfu.ca/~ssurjano/