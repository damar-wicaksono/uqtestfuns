import ast
import math
import operator

from typing import Any

from .validation import SpecValidationError

NAMED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "inf": math.inf,
}

BINOP_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


def resolve_generic(value: Any) -> Any:
    """Resolve generic value to either numeric or string value.

    This function resolves values from YAML specifications by:
    - Returning numeric values (float, int) unchanged
    - Extracting and resolving expressions wrapped in '$()' syntax
    - Substituting named mathematical constants with their numeric values
    - Handling negative constants (e.g., '$(-pi)')
    - Other string returned unchanged

    Parameters
    ----------
    value : Any
        The value to resolve.

    Returns
    -------
    Any
        The resolved value. Expressions wrapped in '$()' are substituted
        with their numeric equivalents. Numeric values are returned unchanged.
        Non-expression strings are returned as-is.

    Raises
    ------
    SpecValidationError
        If the value is a string expression and cannot be evaluated.

    Notes
    -----
    - Expression syntax requires both '$(' prefix and ')' suffixes.
    - Currently, only named constants are supported for the expression.
    - Supported named constants are defined in the NAMED_CONSTANTS dictionary
    - Negative constants are handled by prefixing with '-'
      inside the expression.
    - Non-expression strings are returned unchanged (not validated).

    Examples
    --------
    >>> resolve_generic(3.14)
    3.14
    >>> resolve_generic("value")
    'value'
    >>> resolve_generic('$(pi)')
    3.141592653589793
    >>> resolve_generic('$(-pi)')
    -3.141592653589793
    >>> resolve_generic('$(e)')
    2.718281828459045
    """
    if isinstance(value, str) and _is_expression(value):
        # Evaluate the expression
        value = value[2:-1].strip()
        value = _resolve_expression(value)

    return value


def resolve_numeric(value: str | float | int) -> float | int:
    """Resolve a value to a numeric type.

    Parameters
    ----------
    value : float | int | str
        The value to resolve. Can be a numeric value or a string expression.

    Returns
    -------
    float | int
        The resolved numeric value.

    Raises
    ------
    SpecValidationError
        If the value is a string that is not a valid expression.
    """
    if isinstance(value, (float, int)):
        return value

    if not _is_expression(value):
        raise SpecValidationError(
            f"Unrecognized string value: {value!r}, "
            f"numeric value is expected."
        )

    value = value[2:-1].strip()

    return _resolve_expression(value)


def _is_expression(value: str) -> bool:
    """Check if a value is an expression wrapped in '$()' syntax.

    Parameters
    ----------
    value : str
        The value to check.

    Returns
    -------
    bool
        True if the value is a string starting with '$(' and ending with ')',
        False otherwise.
    """
    return value.startswith("$(") and value.endswith(")")


def _resolve_expression(expression: str) -> float | int:
    """Evaluate a `$()` expression body using a restricted AST walker.

    Supports numeric literals, named constants from ``NAMED_CONSTANTS``,
    and unary negation. All other syntax raises ``SpecValidationError``.

    Parameters
    ----------
    expression : str
        The expression string to evaluate (without the `$()` wrapper).

    Returns
    -------
    float | int
        The evaluated numeric result of the expression.

    Raises
    ------
    SpecValidationError
        If the expression has invalid syntax, contains unsupported operations,
        or references unknown names.
    """
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise SpecValidationError(
            f"Invalid expression {expression!r}: {exc.msg}"
        ) from exc

    return _eval_node(tree.body, expression)


def _eval_node(node: ast.AST, expression: str) -> float | int:
    """Recursively evaluate an AST node from a `$()` expression.

    Parameters
    ----------
    node : ast.AST
        The AST node to evaluate. Supported node types include:
        - ast.Constant: numeric literals (int, float)
        - ast.Name: references to named constants in NAMED_CONSTANTS
        - ast.UnaryOp with ast.USub: unary negation operator
    expression : str
        The original expression string (without `$()` wrapper) used for
        error reporting.

    Returns
    -------
    float | int
        The evaluated numeric result of the AST node.

    Raises
    ------
    SpecValidationError
        If the node contains unsupported constant types (e.g., bool),
        references an unknown name not in ``NAMED_CONSTANTS``, or uses
        unsupported syntax or operations.
    """

    # --- Literal numeric value
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(
            node.value, (int, float)
        ):
            raise SpecValidationError(
                f"Unsupported constant {node.value!r} "
                f"in expression {expression!r}"
            )
        return node.value

    # --- Named constant
    if isinstance(node, ast.Name):
        if node.id in NAMED_CONSTANTS:
            return NAMED_CONSTANTS[node.id]
        raise SpecValidationError(
            f"Unknown name {node.id!r} in expression {expression!r}"
        )

    # --- Binary operation
    if isinstance(node, ast.BinOp):
        op_func = BINOP_OPS.get(type(node.op))
        if op_func is None:
            raise SpecValidationError(
                f"Unsupported operator {type(node.op).__name__} "
                f"in expression {expression!r}"
            )
        # Recurse the binary operation
        left = _eval_node(node.left, expression)
        right = _eval_node(node.right, expression)
        try:
            return op_func(left, right)
        except ZeroDivisionError as exc:
            raise SpecValidationError(
                f"Division by zero in expression {expression!r}"
            ) from exc

    # --- Unary negation
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_node(node.operand, expression)

    # --- Unary positive
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
        return _eval_node(node.operand, expression)

    raise SpecValidationError(
        f"Unsupported syntax in expression {expression!r}: "
        f"{type(node).__name__}"
    )
