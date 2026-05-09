import type { SummaryPayload } from "../types";

type SummaryPanelProps = {
  summary: SummaryPayload | null;
};

// Render the AI-generated summary panel.
export function SummaryPanel({ summary }: SummaryPanelProps) {
  if (!summary) {
    return (
      <section className="panel">
        <h2>AI Summary</h2>
        <p className="muted">No summary is available.</p>
      </section>
    );
  }

  return (
    <section className="panel summary-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Local LLM summary</p>
          <h2>AI Summary</h2>
        </div>
        <span className="pill">{summary.model || "local model"}</span>
      </div>

      <p className="summary-text">
        {summary.executive_summary || "No executive summary was generated."}
      </p>

      <div className="summary-columns">
        <div>
          <h3>Key findings</h3>
          <ul>
            {(summary.key_findings || []).map((finding, index) => (
              <li key={`${finding}-${index}`}>{finding}</li>
            ))}
          </ul>
        </div>

        <div>
          <h3>Recommended actions</h3>
          <ul>
            {(summary.recommended_actions || []).map((action, index) => (
              <li key={`${action}-${index}`}>{action}</li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}