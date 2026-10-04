"""Entry point for the Calculation API: creates the FastAPI app and defines its routes."""

from fastapi import FastAPI, HTTPException
from full_stack_practice.calculate.calculate import perform_calculation
from full_stack_practice.calculate.power import perform_power
from full_stack_practice.schemas.calculation import (
    CalculationRequest,
    CalculationResponse,
)
from full_stack_practice.schemas.power import PowerRequest, PowerResponse

# The title, description and version appear at the top of the /docs page.
app = FastAPI(
    title="Calculation API",
    description="API for performing calculations and power operations",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to the API"}


# Azure Container Apps will call this later to check the app is alive,
# so it must stay simple and never require login.
@app.get("/health")
def health_check():
    return {"status": "ok"}


# POST because the input arrives as a JSON body described by CalculationRequest.
# FastAPI validates the body before this function runs: a missing field or an
# operation that is not in the Operation enum is rejected with a 422 automatically.
# Changed: added response_model so /docs shows the response shape {"result": number}
# and FastAPI checks that what we return matches CalculationResponse.
@app.post("/calculate", response_model=CalculationResponse)
def calculate(request: CalculationRequest):
    # The service raises ValueError for input that is valid in shape but not
    # allowed by the math (divide by zero). Turning it into HTTPException(400)
    # tells the client "your input is wrong" instead of a 500 "server crashed".
    try:
        result = perform_calculation(request.a, request.b, request.operation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return CalculationResponse(result=result)


# Separate endpoint because power has different inputs (base and exponent)
# and no operation field: the URL already says what it does.
# Changed: added response_model, same reason as /calculate.
@app.post("/power", response_model=PowerResponse)
def power(request: PowerRequest):
    # Same pattern as /calculate: service errors become a 400 with the message.
    try:
        result = perform_power(request.base, request.exponent)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return PowerResponse(result=result)
