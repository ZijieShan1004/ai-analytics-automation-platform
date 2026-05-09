import type { User } from "../types";

type HeaderProps = {
  user: User | null;
  onLogout: () => void;
};

// Render the application header.
export function Header({ user, onLogout }: HeaderProps) {
  return (
    <header className="app-header">
      <div>
        <p className="eyebrow">Backend + AI Analytics Platform</p>
        <h1>AI Analytics Automation Platform</h1>
      </div>

      {user && (
        <div className="header-user">
          <span>{user.email}</span>
          <button className="secondary-button" onClick={onLogout}>
            Log out
          </button>
        </div>
      )}
    </header>
  );
}