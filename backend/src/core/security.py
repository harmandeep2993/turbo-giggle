"""

Security-related utilities and functions for the Calculation API.
"""

from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer

from src.core.config import settings

API_SCOPE = f"api://{settings.api_client_id}/access-as-user"

azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=settings.api_client_id,
    tenant_id=settings.tenant_id,
    scopes={API_SCOPE: "access-as-user"},
)
