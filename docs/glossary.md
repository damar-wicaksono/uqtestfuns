# Glossary

```{glossary}

CDF
    Cumulative distribution function, denoted by $F_X(x; \circ)$ where $\circ$
    is a placeholder for the distribution parameter(s).

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

IS
    Importance sampling

MCS
    Monte-Carlo simulation

PDF
    Probability density function, denoted by $f_X(x; \circ)$ where $\circ$
    is a placeholder for the distribution parameter(s).

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