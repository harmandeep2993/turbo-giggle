"""Tests for the perform_power service function."""

# Fixed: new file. test_power used to be in test_calculate.py and did the math
# itself (request.base ** request.exponent) without calling perform_power.

import pytest
from src.services.power import perform_power


def test_power():
    assert perform_power(2, 3) == 8


def test_power_zero_exponent():
    assert perform_power(5, 0) == 1


# Fixed: added the error cases. These are the inputs that used to cause a 500
# before error handling was added, so they are the most important to keep tested.
def test_zero_to_zero_raises():
    with pytest.raises(ValueError, match="0 to the power of 0"):
        perform_power(0, 0)


def test_zero_base_negative_exponent_raises():
    with pytest.raises(ValueError, match="Zero base with negative exponent"):
        perform_power(0, -1)


def test_negative_base_fractional_exponent_raises():
    with pytest.raises(ValueError, match="Negative base with non-integer exponent"):
        perform_power(-8, 0.5)


# Floats on purpose: Python ints never overflow (10 ** 1000 is a valid int), but
# floats do. Real requests always arrive as floats because the schema says float.
def test_overflow_raises():
    with pytest.raises(ValueError, match="too large"):
        perform_power(10.0, 1000.0)
