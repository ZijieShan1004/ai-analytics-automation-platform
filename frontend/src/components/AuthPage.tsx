import { FormEvent, useState } from "react";

type AuthPageProps = {
  onLogin: (email: string, password: string) => Promise<void>;
  onRegister: (email: string, password: string, fullName: string) => Promise<void>;
};

// Render login and registration forms.
export function AuthPage({ onLogin, onRegister }: AuthPageProps) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("demo@example.com");
  const [password, setPassword] = useState("password123");
  const [fullName, setFullName] = useState("Demo User");
  const [loading, setLoading] = useState(false);

  // Submit the active authentication form.
  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);

    try {
      if (mode === "login") {
        await onLogin(email, password);
      } else {
        await onRegister(email, password, fullName);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <div>
          <p className="eyebrow">Local demo environment</p>
          <h2>{mode === "login" ? "Log in" : "Create account"}</h2>
          <p className="muted">
            Upload structured data and let the backend generate profiling, chart recommendations,
            forecasting, anomaly detection, and AI summaries.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="form-stack">
          {mode === "register" && (
            <label>
              Full name
              <input value={fullName} onChange={(event) => setFullName(event.target.value)} />
            </label>
          )}

          <label>
            Email
            <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
          </label>

          <label>
            Password
            <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
          </label>

          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? "Please wait..." : mode === "login" ? "Log in" : "Register"}
          </button>
        </form>

        <button
          className="link-button"
          onClick={() => setMode(mode === "login" ? "register" : "login")}
        >
          {mode === "login" ? "Need an account? Register" : "Already have an account? Log in"}
        </button>
      </section>
    </main>
  );
}