"""Schemas for power requests and responses."""

# Changed: added the module docstring above.
from pydantic import BaseModel


# No "operation" field: the /power endpoint only does one thing.
# base and exponent are clearer than a and b, because /docs readers can see
# which number is raised to which.
class PowerRequest(BaseModel):
    base: float
    exponent: float


class PowerResponse(BaseModel):
    result: float
