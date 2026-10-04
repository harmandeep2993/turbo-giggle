"""Entry point for the Calculation API: creates the FastAPI app and defines its routes."""

from fastapi import FastAPI

from api.calculation import router as calculation_router
from api.health import router as health_router
from api.power import router as power_router

# The title, description and version appear at the top of the /docs page.
app = FastAPI(
    title="Calculation API",
    description="API for performing calculations and power operations",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(calculation_router)
app.include_router(power_router)
