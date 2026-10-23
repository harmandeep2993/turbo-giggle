import { useMsal } from "@azure/msal-react";

// "Harmandeep Singh" -> "HS", used for the round avatar.
function initials(name) {
  return (name || "?")
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join("");
}

function Header() {
  const { instance, accounts } = useMsal();
  const account = accounts[0];

  return (
    <header className="header">
      <div className="brand">
        <span className="brand-mark">=</span>
        <span>Calculator</span>
      </div>
      {account && (
        <div className="user">
          <span className="avatar" aria-hidden="true">
            {initials(account.name)}
          </span>
          <span className="user-name">{account.name}</span>
          <button className="button button--ghost" onClick={() => instance.logoutRedirect()}>
            Sign out
          </button>
        </div>
      )}
    </header>
  );
}

export default Header;
