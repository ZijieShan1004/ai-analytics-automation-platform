from __future__ import annotations

from typing import Any

import pandas as pd

from analytics_platform_ml.common import safe_float
from analytics_platform_ml.common import to_jsonable


# Generate high-level KPI values from the dataframe.
def generate_kpis(df: pd.DataFrame, roles: dict[str, list[str]]) -> list[dict[str, Any]]:
  kpis: list[dict[str, Any]] = []
  row_count = len(df)
  column_count = len(df.columns)
  missing_ratio = float(df.isna().sum().sum() / max(row_count * column_count, 1))

  kpis.append({
    "name": "Total Rows",
    "value": int(row_count),
    "type": "volume",
    "description": "Total number of records in the uploaded dataset.",
  })

  kpis.append({
    "name": "Total Columns",
    "value": int(column_count),
    "type": "structure",
    "description": "Total number of fields in the uploaded dataset.",
  })

  kpis.append({
    "name": "Missing Cell Ratio",
    "value": safe_float(missing_ratio),
    "type": "quality",
    "description": "Percentage of missing values across the entire dataset.",
  })

  kpis.append({
    "name": "Duplicate Rows",
    "value": int(df.duplicated().sum()),
    "type": "quality",
    "description": "Number of duplicated records detected in the dataset.",
  })

  for column in roles["measure_columns"][:6]:
    numeric = pd.to_numeric(df[column], errors="coerce").dropna()

    if len(numeric) == 0:
      continue

    kpis.extend([
      {
        "name": f"Average {column}",
        "value": safe_float(numeric.mean()),
        "type": "measure_average",
        "column": column,
        "description": f"Average value for {column}.",
      },
      {
        "name": f"Total {column}",
        "value": safe_float(numeric.sum()),
        "type": "measure_total",
        "column": column,
        "description": f"Total value for {column}.",
      },
    ])

  return to_jsonable(kpis)


# Calculate correlations between numeric measure columns.
def calculate_correlations(df: pd.DataFrame, roles: dict[str, list[str]]) -> list[dict[str, Any]]:
  columns = roles["measure_columns"]

  if len(columns) < 2:
    return []

  numeric_df = df[columns].apply(pd.to_numeric, errors="coerce")
  correlation_matrix = numeric_df.corr()
  correlations: list[dict[str, Any]] = []

  for left_index, left_column in enumerate(columns):
    for right_column in columns[left_index + 1:]:
      value = correlation_matrix.loc[left_column, right_column]

      if pd.isna(value):
        continue

      correlations.append({
        "column_a": left_column,
        "column_b": right_column,
        "correlation": safe_float(value),
        "strength": classify_correlation_strength(value),
      })

  correlations.sort(key=lambda item: abs(item["correlation"] or 0), reverse=True)
  return to_jsonable(correlations[:10])


# Classify a correlation coefficient.
def classify_correlation_strength(value: float) -> str:
  absolute = abs(value)

  if absolute >= 0.8:
    return "very_strong"

  if absolute >= 0.6:
    return "strong"

  if absolute >= 0.4:
    return "moderate"

  if absolute >= 0.2:
    return "weak"

  return "very_weak"


# Generate grouped insights using dimensions and measures.
def generate_grouped_insights(df: pd.DataFrame, roles: dict[str, list[str]]) -> list[dict[str, Any]]:
  insights: list[dict[str, Any]] = []
  dimensions = roles["dimension_columns"][:4]
  measures = roles["measure_columns"][:4]

  for dimension in dimensions:
    unique_count = df[dimension].dropna().nunique()

    if unique_count == 0 or unique_count > 30:
      continue

    counts = df[dimension].dropna().astype(str).value_counts().head(5)

    if len(counts) > 0:
      top_value = counts.index[0]
      top_count = int(counts.iloc[0])
      insights.append({
        "type": "top_category",
        "dimension": dimension,
        "title": f"Most common {dimension}",
        "description": f"{top_value} is the most frequent value in {dimension}.",
        "value": to_jsonable(top_value),
        "count": top_count,
      })

    for measure in measures:
      grouped = df[[dimension, measure]].copy()
      grouped[measure] = pd.to_numeric(grouped[measure], errors="coerce")
      grouped = grouped.dropna()

      if len(grouped) == 0:
        continue

      summary = (
        grouped
        .groupby(dimension)[measure]
        .mean()
        .sort_values(ascending=False)
        .head(5)
      )

      if len(summary) == 0:
        continue

      insights.append({
        "type": "grouped_average",
        "dimension": dimension,
        "measure": measure,
        "title": f"Average {measure} by {dimension}",
        "description": f"Shows which {dimension} groups have the highest average {measure}.",
        "values": [
          {
            "group": to_jsonable(index),
            "average": safe_float(value),
          }
          for index, value in summary.items()
        ],
      })

  return to_jsonable(insights[:20])


# Run deterministic analytics over the dataframe.
def run_analytics(df: pd.DataFrame, roles: dict[str, list[str]]) -> dict[str, Any]:
  analytics = {
    "kpis": generate_kpis(df, roles),
    "correlations": calculate_correlations(df, roles),
    "insights": generate_grouped_insights(df, roles),
  }

  return to_jsonable(analytics)