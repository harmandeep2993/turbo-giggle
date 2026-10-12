"""Entry point for the Calculation API: creates the FastAPI app and defines its routes."""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.calculation import router as calculation_router
from src.api.health import router as health_router
from src.api.power import router as power_router
from src.core.config import settings
from src.core.security import API_SCOPE, azure_scheme

# The title, description and version appear at the top of the /docs page.
# The title comes from settings so it can change per environment without code edits.
app = FastAPI(
    title=settings.app_name,
    description="API for performing calculations and power operations",
    version="1.0.0",
    # API docs reveal endpoints and login settings, so only show them in debug (local) mode.
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": settings.frontend_client_id,
        "scopes": API_SCOPE,
    },
)


app.include_router(health_router)
app.include_router(calculation_router, dependencies=[Depends(azure_scheme)])
app.include_router(power_router, dependencies=[Depends(azure_scheme)])

# Fixed: added CORS middleware using allowed_origins from settings.
# Browsers block requests from another origin (the frontend) unless the API allows it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
