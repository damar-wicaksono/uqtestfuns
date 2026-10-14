# Glossary

```{glossary}

CDF
    Cumulative distribution function, denoted by $F_X(x; \circ)$ where $\circ$
    is a placeholder for the distribution parameter(s).
    
    See {ref}`the relevant section in Concepts and Notations <prob-input:concepts-and-notations:cdf>` for more details.

DS
    Directional sampling

FORM
    First-order reliability method

FOSM
    First-order Second-moment method

FOSPA
    First-order Saddlepoint Approximation reliability method {cite}`Du2004`

ICDF
    Inverse cumulative distribution function, denoted by $F^{-1}_X(x; \circ)$
    where $\circ$ is a placeholder for the distribution parameter(s).
    The domain of ICDF is $(0, 1)$. Depending on the distribution
    and its parameter values, the value at the boundaries may or may not be
    finite.
    ICDF is also known as the _quantile function_
    or _percent point function_.

    See {ref}`the relevant section in Concepts and Notations <prob-input:concepts-and-notations:icdf>` for more details.

IS
    Importance sampling

MCS
    Monte-Carlo simulation

Output dimension
    The total number of scalar values in a single output point of a test
    function, equal to the product of all elements of the
    {term}`output shape <Output shape>`.
    A scalar function has output dimension $1$; a function returning a vector
    of length $n$ has output dimension $n$; a function returning a
    $(d_1 \times d_2 \times \cdots \times d_k)$ array has output dimension
    $d_1 \cdot d_2 \cdots d_k$.

Output shape
    The shape of a single output point of a test function, following the
    NumPy convention for array shapes.
    An empty tuple $()$ denotes scalar output; $(n,)$ denotes a 1-D vector
    of length $n$; $(d_1, d_2, \ldots, d_k)$ denotes a multi-dimensional
    array output.
    The {term}`output dimension <Output dimension>` is the product of all
    shape elements (1 for scalar output).

    Note that when a test function is evaluated on a sample of $N$ points,
    the returned array has shape $(N,) + \mathrm{output shape}$; the sample
    size occupies the first axis and is **not** part of the output shape.

PDF
    Probability density function, denoted by $f_X(x; \circ)$ where $\circ$
    is a placeholder for the distribution parameter(s).

    See {ref}`the relevant section in Concepts and Notations <prob-input:concepts-and-notations:pdf>` for more details.

SORM
    Second-order reliability method

SS
    Subset simulation

SSRM
    Sequential surrogate reliability method {cite}`Li2018`

Support
    The support of the probability density function, that is, the subset of 
    the function domain whose elements are not mapped to zero;
    denoted by $\mathcal{D}_X$.

SVM
    Support Vector Machines
```

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```