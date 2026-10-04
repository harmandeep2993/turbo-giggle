"""Tests for the perform_calculation service function."""

# Fixed: the docstring said "calculation endpoints", but these tests call the
# service function directly. Endpoint tests live in test_api.py.

import pytest
from src.schemas.calculation import Operation

# Fixed: was "from src.full_stack_practice...", which fails with
# "No module named 'src'". src/ is only the folder; the package name is
# full_stack_practice.
# Fixed: CalculationRequest and CalculationResponse are no longer imported.
# Service tests call the function directly and do not need schema objects.
from src.services.calculation import perform_calculation


# Fixed: every test used to do the math itself (request.a + request.b) and
# never called perform_calculation, so it would pass even if the function were
# broken. Now each test calls your function and checks what it returns.
def test_addition():
    assert perform_calculation(2, 3, Operation.ADD) == 5


def test_subtraction():
    assert perform_calculation(5, 3, Operation.SUBTRACT) == 2


def test_multiplication():
    assert perform_calculation(2, 3, Operation.MULTIPLY) == 6


def test_division():
    assert perform_calculation(6, 3, Operation.DIVIDE) == 2


# Fixed: the old test divided by zero itself and caught Python's
# ZeroDivisionError, but your function raises ValueError. It also built
# CalculationResponse(result=None), which fails because result must be a float.
# pytest.raises passes only if the code inside the "with" block raises that error.
def test_division_by_zero():
    with pytest.raises(ValueError, match="Division by zero"):
        perform_calculation(6, 0, Operation.DIVIDE)


# Fixed: test_power was moved to test_power.py so each test file matches one
# code file.
