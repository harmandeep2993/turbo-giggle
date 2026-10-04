"""
This module contains a function for performing addition, subtraction, multiplication, and division operations.
"""

# Changed: was importing CalculationRequest and CalculationResponse, which were
# never used here. The service only needs the Operation enum.
from src.schemas.calculation import Operation


# This is a "service": pure logic with no FastAPI code, so it can be tested on
# its own and reused from any route.
# Changed: operation type is Operation instead of str, and "-> float" was added
# so readers and the editor know exactly what goes in and comes out.
def perform_calculation(a: float, b: float, operation: Operation) -> float:
    """
    Returns the result of the specified arithmetic operation on two numbers.

    Parameters:
    a (float): The first number.
    b (float): The second number.
    operation (Operation): The arithmetic operation to perform.

    Returns:
    float: The result of the specified arithmetic operation.

    Raises:
    ValueError: If the operation is division and b is zero.
    """
    # Changed: compares with Operation.ADD etc. instead of "add". A typo in an
    # enum name fails immediately, while a typo in a string fails silently.
    # Changed: the final "else: raise ValueError('Unsupported operation')" was
    # removed. The schema rejects unknown operations with a 422 before this
    # function is ever called, so that branch could never run.
    if operation == Operation.ADD:
        return a + b
    elif operation == Operation.SUBTRACT:
        return a - b
    elif operation == Operation.MULTIPLY:
        return a * b
    elif operation == Operation.DIVIDE:
        # The schema cannot catch this: b=0 is a valid number, it is only
        # invalid together with "divide". So the service checks it and the
        # route turns the ValueError into a 400.
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b
