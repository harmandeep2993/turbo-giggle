import { InteractionStatus } from "@azure/msal-browser";
import { useIsAuthenticated, useMsal } from "@azure/msal-react";

import Calculator from "./components/Calculator";
import Header from "./components/Header";
import SignIn from "./components/SignIn";

function App() {
  const { inProgress } = useMsal();
  const isAuthenticated = useIsAuthenticated();

  // While MSAL processes the redirect back from Microsoft, show a loader instead
  // of briefly flashing the sign-in page.
  const isLoading = !isAuthenticated && inProgress !== InteractionStatus.None;

  return (
    <div className="layout">
      <Header />
      <main className="content">
        {isLoading && <p className="muted">Signing you in...</p>}
        {!isLoading && !isAuthenticated && <SignIn />}
        {isAuthenticated && <Calculator />}
      </main>
    </div>
  );
}

export default App;
