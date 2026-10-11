import {
  AuthenticatedTemplate,
  UnauthenticatedTemplate,
  useMsal,
} from "@azure/msal-react";

import { apiRequest } from "./authConfig";
import Calculator from "./components/Calculator";

function App() {
  const { instance, accounts } = useMsal();
  const account = accounts[0];

  return (
    <main className="app">
      <h1>Calculator</h1>

      <UnauthenticatedTemplate>
        <p>Sign in with your company account to use the calculator.</p>
        {/* Asking for the API scope at login means the first API call needs no extra prompt. */}
        <button onClick={() => instance.loginRedirect(apiRequest)}>Sign in</button>
      </UnauthenticatedTemplate>

      <AuthenticatedTemplate>
        <div className="user">
          <span>Signed in as {account?.name}</span>
          <button className="secondary" onClick={() => instance.logoutRedirect()}>
            Sign out
          </button>
        </div>
        <Calculator />
      </AuthenticatedTemplate>
    </main>
  );
}

export default App;
