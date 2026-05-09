from __future__ import annotations

from typing import Any

import pandas as pd

from analytics_platform_ml.analytics import run_analytics
from analytics_platform_ml.anomalies import detect_anomalies
from analytics_platform_ml.charts import generate_chart_recommendations
from analytics_platform_ml.common import clean_dataframe
from analytics_platform_ml.common import to_jsonable
from analytics_platform_ml.forecasting import generate_forecast
from analytics_platform_ml.profiling import profile_dataframe
from analytics_platform_ml.summaries import build_summary


# Build a final report object from all pipeline outputs.
def build_report(
  dataset_name: str | None,
  profile: dict[str, Any],
  analytics: dict[str, Any],
  anomalies: dict[str, Any],
  charts: list[dict[str, Any]],
  forecast: dict[str, Any],
  summary: dict[str, Any],
) -> dict[str, Any]:
  report = {
    "title": f"Analytics Report for {dataset_name}" if dataset_name else "Analytics Report",
    "dataset_name": dataset_name,
    "sections": [
      {
        "name": "Dataset Profile",
        "type": "profile",
        "content": profile,
      },
      {
        "name": "Automated Analytics",
        "type": "analytics",
        "content": analytics,
      },
      {
        "name": "Anomaly Detection",
        "type": "anomalies",
        "content": anomalies,
      },
      {
        "name": "Chart Recommendations",
        "type": "charts",
        "content": charts,
      },
      {
        "name": "Forecasting",
        "type": "forecast",
        "content": forecast,
      },
      {
        "name": "AI Summary",
        "type": "summary",
        "content": summary,
      },
    ],
  }

  return to_jsonable(report)


# Run the complete ML analytics pipeline.
# Run the complete ML analytics pipeline.
def run_full_pipeline(
  df: pd.DataFrame | None = None,
  dataset_name: str | None = None,
  dataframe: pd.DataFrame | None = None,
) -> dict[str, Any]:
  input_df = dataframe if dataframe is not None else df

  if input_df is None:
    raise ValueError("run_full_pipeline requires a dataframe input.")

  cleaned_df = clean_dataframe(input_df)
  profile = profile_dataframe(cleaned_df)
  roles = profile["roles"]
  analytics = run_analytics(cleaned_df, roles)
  anomalies = detect_anomalies(cleaned_df, roles)
  charts = generate_chart_recommendations(cleaned_df, roles)
  forecast = generate_forecast(cleaned_df, roles)
  summary = build_summary(profile, analytics, anomalies, forecast, charts)
  report = build_report(dataset_name, profile, analytics, anomalies, charts, forecast, summary)

  result = {
    "profile": profile,
    "analytics": analytics,
    "anomalies": anomalies,
    "chart_recommendations": charts,
    "charts": charts,
    "forecast": forecast,
    "summary": summary,
    "report": report,
  }

  return to_jsonable(result)