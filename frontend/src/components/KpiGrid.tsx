import type { KpiItem } from "../types";
import { formatValue } from "../utils/report";

type KpiGridProps = {
  kpis: KpiItem[];
};

// Render KPI cards from analytics results.
export function KpiGrid({ kpis }: KpiGridProps) {
  if (kpis.length === 0) {
    return (
      <section className="panel">
        <h2>KPI Summary</h2>
        <p className="muted">No KPI values are available.</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Analytics</p>
          <h2>KPI Summary</h2>
        </div>
        <span className="pill">{kpis.length} KPIs</span>
      </div>

      <div className="kpi-grid">
        {kpis.slice(0, 8).map((kpi) => (
          <article className="kpi-card" key={`${kpi.name}-${kpi.column || "global"}`}>
            <span>{kpi.type || "metric"}</span>
            <strong>{formatValue(kpi.value)}</strong>
            <p>{kpi.name}</p>
          </article>
        ))}
      </div>
    </section>
  );
}