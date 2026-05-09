from __future__ import annotations

from typing import Any

from analytics_platform_ml.common import to_jsonable


# Extract the most useful KPI facts for summary generation.
def extract_kpi_findings(analytics: dict[str, Any]) -> list[str]:
  findings: list[str] = []

  for kpi in analytics.get("kpis", [])[:8]:
    name = kpi.get("name")
    value = kpi.get("value")

    if name is None:
      continue

    findings.append(f"{name}: {value}")

  return findings


# Extract notable correlation facts for summary generation.
def extract_correlation_findings(analytics: dict[str, Any]) -> list[str]:
  findings: list[str] = []

  for item in analytics.get("correlations", [])[:3]:
    column_a = item.get("column_a")
    column_b = item.get("column_b")
    correlation = item.get("correlation")
    strength = item.get("strength")

    findings.append(
      f"{column_a} and {column_b} have a {strength} correlation of {correlation}."
    )

  return findings


# Extract anomaly facts for summary generation.
def extract_anomaly_findings(anomalies: dict[str, Any]) -> list[str]:
  findings: list[str] = []

  for item in anomalies.get("univariate", [])[:5]:
    column = item.get("column")
    count = item.get("anomaly_count")
    ratio = item.get("anomaly_ratio")

    if count and count > 0:
      findings.append(f"{column} has {count} IQR outliers with anomaly ratio {ratio}.")

  multivariate = anomalies.get("multivariate", {})

  if multivariate.get("available") and multivariate.get("anomaly_count", 0) > 0:
    findings.append(
      f"Multivariate anomaly detection found {multivariate.get('anomaly_count')} unusual records."
    )

  return findings


# Extract forecasting facts for summary generation.
def extract_forecast_findings(forecast: dict[str, Any]) -> list[str]:
  if not forecast.get("available"):
    return ["Forecasting was not available for this dataset."]

  predictions = forecast.get("predictions", [])
  target = forecast.get("target_column")

  if len(predictions) == 0:
    return [f"Forecasting ran for {target}, but no future predictions were generated."]

  first = predictions[0].get("predicted_value")
  last = predictions[-1].get("predicted_value")

  return [
    f"The forecast target is {target}.",
    f"The first predicted value is {first}, and the last predicted value is {last}.",
  ]


# Build a deterministic fallback summary.
def generate_rule_based_summary(
  profile: dict[str, Any],
  analytics: dict[str, Any],
  anomalies: dict[str, Any],
  forecast: dict[str, Any],
  charts: list[dict[str, Any]],
) -> dict[str, Any]:
  row_count = profile.get("row_count")
  column_count = profile.get("column_count")
  missing_ratio = profile.get("missing_cell_ratio")
  findings = []
  findings.extend(extract_kpi_findings(analytics))
  findings.extend(extract_correlation_findings(analytics))
  findings.extend(extract_anomaly_findings(anomalies))
  findings.extend(extract_forecast_findings(forecast))

  executive_summary = (
    f"The dataset contains {row_count} rows and {column_count} columns. "
    f"The overall missing-cell ratio is {missing_ratio}. "
    f"The system generated {len(charts)} chart recommendations and completed automated profiling, analytics, anomaly detection, and forecasting when possible."
  )

  return {
    "executive_summary": executive_summary,
    "key_findings": findings[:10],
    "recommended_actions": [
      "Review missing values before using the dataset for high-stakes decisions.",
      "Inspect detected anomalies to determine whether they are valid edge cases or data quality issues.",
      "Use the recommended charts to validate trends, distributions, and category-level differences.",
    ],
  }


# Build an LLM prompt for local business-report generation.
def build_llm_prompt(
  profile: dict[str, Any],
  analytics: dict[str, Any],
  anomalies: dict[str, Any],
  forecast: dict[str, Any],
  charts: list[dict[str, Any]],
) -> str:
  fallback = generate_rule_based_summary(profile, analytics, anomalies, forecast, charts)

  prompt = f"""
You are an internal business analytics assistant.

Write a concise business report for a structured dataset.

Dataset profile:
- Rows: {profile.get("row_count")}
- Columns: {profile.get("column_count")}
- Missing cell ratio: {profile.get("missing_cell_ratio")}
- Duplicate rows: {profile.get("duplicate_row_count")}

Key findings:
{fallback.get("key_findings")}

Forecast:
{forecast}

Chart recommendations:
{charts[:5]}

Return:
1. Executive summary
2. KPI interpretation
3. Trend or anomaly interpretation
4. Recommended next actions
""".strip()

  return prompt


# Build the summary payload for backend persistence.
def build_summary(
  profile: dict[str, Any],
  analytics: dict[str, Any],
  anomalies: dict[str, Any],
  forecast: dict[str, Any],
  charts: list[dict[str, Any]],
) -> dict[str, Any]:
  fallback = generate_rule_based_summary(profile, analytics, anomalies, forecast, charts)
  prompt = build_llm_prompt(profile, analytics, anomalies, forecast, charts)

  summary = {
    "provider": "rule_based_with_ollama_prompt",
    "model": "qwen2.5:1.5b",
    "executive_summary": fallback["executive_summary"],
    "key_findings": fallback["key_findings"],
    "recommended_actions": fallback["recommended_actions"],
    "llm_prompt": prompt,
  }

  return to_jsonable(summary)