import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import type { ForecastPayload } from "../types";

type ForecastPanelProps = {
  forecast: ForecastPayload | null;
};

type ForecastChartPoint = {
  date: string;
  actual?: number | null;
  predicted?: number | null;
};

// Build chart data from forecast history and predictions.
function buildForecastChartData(forecast: ForecastPayload): ForecastChartPoint[] {
  const history = (forecast.history || []).map((point) => ({
    date: point.date,
    actual: point.actual_value ?? null,
    predicted: null
  }));

  const predictions = (forecast.predictions || []).map((point) => ({
    date: point.date,
    actual: null,
    predicted: point.predicted_value ?? null
  }));

  return [...history, ...predictions];
}

// Render the forecast result panel.
export function ForecastPanel({ forecast }: ForecastPanelProps) {
  if (!forecast) {
    return (
      <section className="panel">
        <h2>Forecast</h2>
        <p className="muted">No forecast data is available.</p>
      </section>
    );
  }

  if (!forecast.available) {
    return (
      <section className="panel">
        <h2>Forecast</h2>
        <p className="muted">{forecast.reason || "Forecasting is not available for this dataset."}</p>
      </section>
    );
  }

  const chartData = buildForecastChartData(forecast);

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Forecasting</p>
          <h2>{forecast.target_column} Forecast</h2>
        </div>
        <span className="pill">{forecast.model_type}</span>
      </div>

      <div className="forecast-chart">
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" tick={{ fontSize: 11 }} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="actual" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="predicted" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}