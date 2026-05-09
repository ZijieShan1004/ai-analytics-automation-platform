import type { ChartRecommendation } from "../types";

type ChartRecommendationsProps = {
  recommendations: ChartRecommendation[];
};

// Render recommended chart configurations.
export function ChartRecommendations({ recommendations }: ChartRecommendationsProps) {
  if (recommendations.length === 0) {
    return (
      <section className="panel">
        <h2>Chart Recommendations</h2>
        <p className="muted">No chart recommendations are available.</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Visualization engine</p>
          <h2>Chart Recommendations</h2>
        </div>
        <span className="pill">{recommendations.length} charts</span>
      </div>

      <div className="chart-grid">
        {recommendations.map((chart, index) => (
          <article className="chart-card" key={`${chart.title}-${index}`}>
            <span className="chart-type">{chart.chart_type}</span>
            <h3>{chart.title}</h3>
            <p>{chart.description || chart.reason || "Recommended by the analytics engine."}</p>
            <div className="chart-meta">
              <span>X: {chart.x_axis || "N/A"}</span>
              <span>Y: {chart.y_axis || "N/A"}</span>
              <span>Agg: {chart.aggregation || "N/A"}</span>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}