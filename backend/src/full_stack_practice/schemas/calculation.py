"""Schemas for calculation requests and responses."""

# Changed: a blank line now separates standard library imports (enum) from
# third-party imports (pydantic), which is the usual Python import order.
from enum import Enum

from pydantic import BaseModel


# Inheriting from both str and Enum means: the only allowed values are these
# four, and each value is still a plain string in JSON. FastAPI shows them as a
# dropdown in /docs and returns 422 for anything else (for example "power").
class Operation(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


# What the client sends. Pydantic checks that a and b are numbers and that
# operation is one of the Operation values before the route code runs.
class CalculationRequest(BaseModel):
    a: float
    b: float
    operation: Operation


# What the API sends back. Kept separate from the request model so input and
# output can change independently.
class CalculationResponse(BaseModel):
    result: float
