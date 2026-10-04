from fastapi import APIRouter, HTTPException

from src.schemas.power import PowerRequest, PowerResponse
from src.services.power import perform_power

router = APIRouter(tags=["power"])


# Separate endpoint because power has different inputs (base and exponent)
# and no operation field: the URL already says what it does.
# Changed: added response_model, same reason as /calculate.
@router.post("/power", response_model=PowerResponse)
def power(request: PowerRequest):
    # Same pattern as /calculate: service errors become a 400 with the message.
    try:
        result = perform_power(request.base, request.exponent)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return PowerResponse(result=result)
