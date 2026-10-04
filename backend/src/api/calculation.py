"""
API endpoints for performing calculations and power operations.
"""

from fastapi import APIRouter

from schemas.calculation import (
    CalculationRequest,
    CalculationResponse,
)
from services.calculation import perform_calculation
from fastapi import HTTPException

router = APIRouter(tags=["calculation"])


# POST because the input arrives as a JSON body described by CalculationRequest.
# FastAPI validates the body before this function runs: a missing field or an
# operation that is not in the Operation enum is rejected with a 422 automatically.
# Changed: added response_model so /docs shows the response shape {"result": number}
# and FastAPI checks that what we return matches CalculationResponse.
@router.post("/calculate", response_model=CalculationResponse)
def calculate(request: CalculationRequest):
    # The service raises ValueError for input that is valid in shape but not
    # allowed by the math (divide by zero). Turning it into HTTPException(400)
    # tells the client "your input is wrong" instead of a 500 "server crashed".
    try:
        result = perform_calculation(request.a, request.b, request.operation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return CalculationResponse(result=result)
