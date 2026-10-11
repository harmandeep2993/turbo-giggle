/* === Calls to the backend, each with an Entra ID access token === */

import { InteractionRequiredAuthError } from "@azure/msal-browser";

import { apiRequest } from "./authConfig";

const API_URL = import.meta.env.VITE_API_URL;

async function getToken(instance, account) {
  try {
    // Uses the cached token, or refreshes it in the background without user action.
    const result = await instance.acquireTokenSilent({ ...apiRequest, account });
    return result.accessToken;
  } catch (error) {
    // The session expired or consent is missing: the user has to log in again.
    if (error instanceof InteractionRequiredAuthError) {
      await instance.acquireTokenRedirect({ ...apiRequest, account });
    }
    throw error;
  }
}

// FastAPI returns "detail" as a string (400), a list (422) or an object (401).
function errorMessage(detail) {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return detail.map((item) => item.msg).join(", ");
  if (detail && detail.message) return detail.message;
  return "Request failed";
}

async function post(instance, account, path, body) {
  const token = await getToken(instance, account);
  const response = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(body),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(errorMessage(data.detail));
  }
  return data.result;
}

export function calculate(instance, account, a, b, operation) {
  return post(instance, account, "/calculate", { a, b, operation });
}

export function power(instance, account, base, exponent) {
  return post(instance, account, "/power", { base, exponent });
}
