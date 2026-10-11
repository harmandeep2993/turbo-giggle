/* === MSAL settings: which app logs in, against which tenant, for which API === */

// Values come from .env.local so they can differ per environment without code edits.
const tenantId = import.meta.env.VITE_TENANT_ID;

export const msalConfig = {
  auth: {
    clientId: import.meta.env.VITE_CLIENT_ID,
    authority: `https://login.microsoftonline.com/${tenantId}`,
    redirectUri: window.location.origin,
  },
  cache: {
    // sessionStorage clears tokens when the tab closes, which is safer than localStorage.
    cacheLocation: "sessionStorage",
  },
};

// The scope that calc-api exposes; the token is only valid for calls to our API.
export const apiRequest = {
  scopes: [import.meta.env.VITE_API_SCOPE],
};
