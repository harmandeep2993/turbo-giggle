"""Health check endpoint for the Calculation API."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])

# Azure Container Apps will call this later to check the app is alive,
# so it must stay simple and never require login.


# Root endpoint for the API, provides a welcome message.
@router.get("/")
def root():
    return {"message": "Welcome to the Calculation API"}


@router.get("/health")
def health_check():
    return {"status": "ok"}
