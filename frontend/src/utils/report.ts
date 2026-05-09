import type {
  ChartRecommendation,
  ForecastPayload,
  KpiItem,
  NormalizedReport,
  ProfilePayload,
  ReportResponse,
  ReportSection,
  SummaryPayload
} from "../types";

// Check whether a value is a plain object.
function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

// Parse JSON string values safely.
function parseMaybeJson(value: unknown): unknown {
  if (typeof value !== "string") {
    return value;
  }

  try {
    return JSON.parse(value);
  } catch {
    return value;
  }
}

// Normalize one backend chart object into frontend chart format.
function normalizeChart(chart: unknown): ChartRecommendation | null {
  const parsed = parseMaybeJson(chart);

  if (!isRecord(parsed)) {
    return null;
  }

  return {
    chart_type: String(parsed.chart_type || "bar"),
    title: String(parsed.title || "Untitled chart"),
    description: typeof parsed.description === "string" ? parsed.description : undefined,
    reason: typeof parsed.reason === "string" ? parsed.reason : undefined,
    x_axis: typeof parsed.x_axis === "string"
      ? parsed.x_axis
      : typeof parsed.x_column === "string"
        ? parsed.x_column
        : typeof parsed.group_by_column === "string"
          ? parsed.group_by_column
          : null,
    y_axis: typeof parsed.y_axis === "string"
      ? parsed.y_axis
      : typeof parsed.y_column === "string"
        ? parsed.y_column
        : null,
    aggregation: typeof parsed.aggregation === "string" ? parsed.aggregation : null,
    config: isRecord(parsed.config)
      ? parsed.config
      : isRecord(parsed.chart_payload)
        ? parsed.chart_payload
        : {}
  };
}

// Normalize backend report responses into a single frontend shape.
export function normalizeReport(response: ReportResponse | unknown): NormalizedReport {
  const root = parseMaybeJson(response);

  if (!isRecord(root)) {
    return {
      title: "Analytics Report",
      dataset_name: null,
      sections: []
    };
  }

  const reportPayload = parseMaybeJson(root.report_payload);
  const payload = isRecord(reportPayload) ? reportPayload : root;
  const sections: ReportSection[] = [];

  const title = typeof root.title === "string" ? root.title : "Analytics Report";
  const datasetName = typeof root.dataset_name === "string" ? root.dataset_name : null;

  if (Array.isArray(payload.sections)) {
    return {
      title,
      dataset_name: datasetName,
      sections: payload.sections as ReportSection[]
    };
  }

  if (isRecord(payload.report) && Array.isArray(payload.report.sections)) {
    return {
      title: typeof payload.report.title === "string" ? payload.report.title : title,
      dataset_name: typeof payload.report.dataset_name === "string" ? payload.report.dataset_name : datasetName,
      sections: payload.report.sections as ReportSection[]
    };
  }

  if (isRecord(payload.profile)) {
    sections.push({
      name: "Dataset Profile",
      type: "profile",
      content: payload.profile
    });
  }

  if (isRecord(payload.analytics)) {
    sections.push({
      name: "Automated Analytics",
      type: "analytics",
      content: payload.analytics
    });
  }

  if (isRecord(payload.forecast)) {
    sections.push({
      name: "Forecasting",
      type: "forecast",
      content: payload.forecast
    });
  }

  if (isRecord(payload.summary)) {
    sections.push({
      name: "AI Summary",
      type: "summary",
      content: payload.summary
    });
  }

  const rawCharts = Array.isArray(payload.chart_recommendations)
    ? payload.chart_recommendations
    : Array.isArray(payload.charts)
      ? payload.charts
      : [];

  const charts = rawCharts
    .map(normalizeChart)
    .filter((chart): chart is ChartRecommendation => chart !== null);

  if (charts.length > 0) {
    sections.push({
      name: "Chart Recommendations",
      type: "charts",
      content: charts
    });
  }

  return {
    title,
    dataset_name: datasetName,
    sections
  };
}

// Find one report section by type.
export function findSection(report: NormalizedReport, type: string): ReportSection | null {
  return report.sections.find((section) => section.type === type) || null;
}

// Extract the profile section payload.
export function getProfile(report: NormalizedReport): ProfilePayload | null {
  const section = findSection(report, "profile");
  return isRecord(section?.content) ? section.content as ProfilePayload : null;
}

// Extract the analytics section payload.
export function getKpis(report: NormalizedReport): KpiItem[] {
  const section = findSection(report, "analytics");

  if (!isRecord(section?.content)) {
    return [];
  }

  const kpis = section.content.kpis;
  return Array.isArray(kpis) ? kpis as KpiItem[] : [];
}

// Extract the chart recommendation section payload.
export function getChartRecommendations(report: NormalizedReport): ChartRecommendation[] {
  const section = findSection(report, "charts");

  if (!Array.isArray(section?.content)) {
    return [];
  }

  return section.content as ChartRecommendation[];
}

// Extract the forecasting section payload.
export function getForecast(report: NormalizedReport): ForecastPayload | null {
  const section = findSection(report, "forecast");
  return isRecord(section?.content) ? section.content as ForecastPayload : null;
}

// Extract the summary section payload.
export function getSummary(report: NormalizedReport): SummaryPayload | null {
  const section = findSection(report, "summary");
  return isRecord(section?.content) ? section.content as SummaryPayload : null;
}

// Format a value for dashboard display.
export function formatValue(value: unknown): string {
  if (value === null || value === undefined) {
    return "N/A";
  }

  if (typeof value === "number") {
    if (Math.abs(value) < 1 && value !== 0) {
      return value.toFixed(4);
    }

    return value.toLocaleString(undefined, {
      maximumFractionDigits: 2
    });
  }

  if (typeof value === "boolean") {
    return value ? "Yes" : "No";
  }

  return String(value);
}