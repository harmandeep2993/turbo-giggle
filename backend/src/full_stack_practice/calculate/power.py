"""
This module contains a function for performing the power operation.
"""


# Changed: added "-> float". Earlier this function also took an "operation"
# argument that could only be "power"; that was removed because the /power
# endpoint already says what it does.
def perform_power(base: float, exponent: float) -> float:
    """
    Returns the result of the power operation on two numbers.

    Parameters:
    base (float): The base number.
    exponent (float): The exponent number.

    Returns:
    float: The result of the power operation.

    Raises:
    ValueError: If the result is undefined or not a real number.
    """
    # Changed: the checks were reordered. Before, "base == 0 -> return 0" ran
    # first, so 0 ** -1 returned 0 instead of an error. Zero-base cases are
    # now checked first: 0 ** negative would divide by zero.
    # Changed: removed "base == 0 -> return 0" and "exponent == 0 -> return 1"
    # because base**exponent already gives those results.
    if base == 0 and exponent == 0:
        raise ValueError("0 to the power of 0 is undefined.")
    elif base == 0 and exponent < 0:
        raise ValueError("Zero base with negative exponent is not allowed.")
    elif base < 0 and exponent % 1 != 0:
        # Python would return a complex number here, which is not a valid float result.
        raise ValueError("Negative base with non-integer exponent is not allowed.")
    # Very large results (10 ** 1000) do not fit in a float and raise
    # OverflowError. Converting it to ValueError means the route only has to
    # handle one error type to return a 400.
    try:
        return base**exponent
    except OverflowError:
        raise ValueError("Result is too large to be represented as a float.")
