import type { NormalizedReport } from "../types";
import {
  getChartRecommendations,
  getForecast,
  getKpis,
  getProfile,
  getSummary
} from "../utils/report";
import { ChartRecommendations } from "./ChartRecommendations";
import { ForecastPanel } from "./ForecastPanel";
import { KpiGrid } from "./KpiGrid";
import { ProfilePanel } from "./ProfilePanel";
import { SummaryPanel } from "./SummaryPanel";

type ReportDashboardProps = {
  report: NormalizedReport | null;
};

// Render the full analytics report dashboard.
export function ReportDashboard({ report }: ReportDashboardProps) {
  if (!report) {
    return (
      <section className="panel empty-report">
        <h2>Analytics Report</h2>
        <p className="muted">
          Select a completed dataset or upload a new file to generate a report.
        </p>
      </section>
    );
  }

  const profile = getProfile(report);
  const kpis = getKpis(report);
  const charts = getChartRecommendations(report);
  const forecast = getForecast(report);
  const summary = getSummary(report);

  return (
    <div className="report-stack">
      <section className="report-title-card">
        <p className="eyebrow">Generated report</p>
        <h2>{report.title}</h2>
      </section>

      <SummaryPanel summary={summary} />
      <KpiGrid kpis={kpis} />
      <ForecastPanel forecast={forecast} />
      <ChartRecommendations recommendations={charts} />
      <ProfilePanel profile={profile} />
    </div>
  );
}