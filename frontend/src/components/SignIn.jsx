import { useMsal } from "@azure/msal-react";

import { apiRequest } from "../authConfig";

function SignIn() {
  const { instance } = useMsal();

  return (
    <section className="card card--center">
      <h1>Welcome</h1>
      <p className="muted">Sign in with your company account to use the calculator.</p>
      {/* Asking for the API scope at login means the first API call needs no extra prompt. */}
      <button className="button button--primary button--wide" onClick={() => instance.loginRedirect(apiRequest)}>
        Sign in with Microsoft
      </button>
    </section>
  );
}

export default SignIn;
