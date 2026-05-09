from __future__ import annotations

from typing import Any

import pandas as pd

from analytics_platform_ml.common import to_jsonable


# Create a chart recommendation object.
def build_chart(
  chart_type: str,
  title: str,
  description: str,
  x_axis: str | None,
  y_axis: str | None,
  reason: str,
  aggregation: str | None = None,
) -> dict[str, Any]:
  return {
    "chart_type": chart_type,
    "title": title,
    "description": description,
    "x_axis": x_axis,
    "y_axis": y_axis,
    "aggregation": aggregation,
    "reason": reason,
    "config": {
      "x": x_axis,
      "y": y_axis,
      "type": chart_type,
      "aggregation": aggregation,
    },
  }


# Recommend time-series charts.
def recommend_time_series_charts(roles: dict[str, list[str]]) -> list[dict[str, Any]]:
  recommendations: list[dict[str, Any]] = []

  for time_column in roles["datetime_columns"][:2]:
    for measure in roles["measure_columns"][:3]:
      recommendations.append(build_chart(
        chart_type="line",
        title=f"{measure} over time",
        description=f"Tracks how {measure} changes across {time_column}.",
        x_axis=time_column,
        y_axis=measure,
        aggregation="mean",
        reason="A datetime column and a numeric measure were detected.",
      ))

  return recommendations


# Recommend categorical comparison charts.
def recommend_bar_charts(df: pd.DataFrame, roles: dict[str, list[str]]) -> list[dict[str, Any]]:
  recommendations: list[dict[str, Any]] = []

  for dimension in roles["dimension_columns"][:4]:
    unique_count = df[dimension].dropna().nunique()

    if unique_count == 0 or unique_count > 30:
      continue

    for measure in roles["measure_columns"][:3]:
      recommendations.append(build_chart(
        chart_type="bar",
        title=f"Average {measure} by {dimension}",
        description=f"Compares average {measure} across {dimension} groups.",
        x_axis=dimension,
        y_axis=measure,
        aggregation="mean",
        reason="A categorical dimension and numeric measure were detected.",
      ))

    recommendations.append(build_chart(
      chart_type="bar",
      title=f"Record count by {dimension}",
      description=f"Shows the distribution of records across {dimension}.",
      x_axis=dimension,
      y_axis=None,
      aggregation="count",
      reason="A categorical column with manageable cardinality was detected.",
    ))

  return recommendations


# Recommend distribution charts.
def recommend_distribution_charts(roles: dict[str, list[str]]) -> list[dict[str, Any]]:
  recommendations: list[dict[str, Any]] = []

  for measure in roles["measure_columns"][:5]:
    recommendations.append(build_chart(
      chart_type="histogram",
      title=f"Distribution of {measure}",
      description=f"Shows the spread and skew of {measure}.",
      x_axis=measure,
      y_axis=None,
      aggregation=None,
      reason="A numeric measure was detected.",
    ))

  return recommendations


# Recommend relationship charts.
def recommend_scatter_charts(roles: dict[str, list[str]]) -> list[dict[str, Any]]:
  recommendations: list[dict[str, Any]] = []
  measures = roles["measure_columns"]

  for index, x_column in enumerate(measures[:4]):
    for y_column in measures[index + 1:index + 3]:
      recommendations.append(build_chart(
        chart_type="scatter",
        title=f"{y_column} vs {x_column}",
        description=f"Shows the relationship between {x_column} and {y_column}.",
        x_axis=x_column,
        y_axis=y_column,
        aggregation=None,
        reason="Two numeric measures were detected.",
      ))

  return recommendations


# Generate chart recommendations for the dataframe.
def generate_chart_recommendations(df: pd.DataFrame, roles: dict[str, list[str]]) -> list[dict[str, Any]]:
  recommendations: list[dict[str, Any]] = []
  recommendations.extend(recommend_time_series_charts(roles))
  recommendations.extend(recommend_bar_charts(df, roles))
  recommendations.extend(recommend_distribution_charts(roles))
  recommendations.extend(recommend_scatter_charts(roles))

  unique: list[dict[str, Any]] = []
  seen: set[tuple[Any, Any, Any, Any]] = set()

  for recommendation in recommendations:
    key = (
      recommendation["chart_type"],
      recommendation["x_axis"],
      recommendation["y_axis"],
      recommendation["aggregation"],
    )

    if key in seen:
      continue

    seen.add(key)
    unique.append(recommendation)

  return to_jsonable(unique[:12])