from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.ensemble import IsolationForest

from analytics_platform_ml.common import safe_float
from analytics_platform_ml.common import to_jsonable


# Detect univariate numeric anomalies using the IQR rule.
def detect_iqr_anomalies(df: pd.DataFrame, roles: dict[str, list[str]]) -> list[dict[str, Any]]:
  results: list[dict[str, Any]] = []

  for column in roles["measure_columns"]:
    numeric = pd.to_numeric(df[column], errors="coerce")
    non_null = numeric.dropna()

    if len(non_null) < 8:
      continue

    q1 = non_null.quantile(0.25)
    q3 = non_null.quantile(0.75)
    iqr = q3 - q1

    if iqr == 0:
      continue

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    mask = (numeric < lower_bound) | (numeric > upper_bound)
    anomaly_indices = df.index[mask.fillna(False)].tolist()

    results.append({
      "type": "iqr",
      "column": column,
      "lower_bound": safe_float(lower_bound),
      "upper_bound": safe_float(upper_bound),
      "anomaly_count": int(len(anomaly_indices)),
      "anomaly_ratio": safe_float(len(anomaly_indices) / max(len(df), 1)),
      "sample_indices": [int(index) for index in anomaly_indices[:10]],
    })

  return to_jsonable(results)


# Detect multivariate numeric anomalies using Isolation Forest.
def detect_isolation_forest_anomalies(df: pd.DataFrame, roles: dict[str, list[str]]) -> dict[str, Any]:
  columns = roles["measure_columns"]

  if len(columns) < 2 or len(df) < 20:
    return {
      "available": False,
      "reason": "Not enough numeric columns or rows for multivariate anomaly detection.",
      "anomalies": [],
    }

  numeric_df = df[columns].apply(pd.to_numeric, errors="coerce")
  numeric_df = numeric_df.dropna(axis=1, how="all")
  numeric_df = numeric_df.fillna(numeric_df.median(numeric_only=True))

  if numeric_df.shape[1] < 2 or numeric_df.shape[0] < 20:
    return {
      "available": False,
      "reason": "Not enough complete numeric data for multivariate anomaly detection.",
      "anomalies": [],
    }

  contamination = min(0.1, max(0.01, 5 / max(len(numeric_df), 1)))
  model = IsolationForest(contamination=contamination, random_state=42)
  labels = model.fit_predict(numeric_df)
  scores = model.decision_function(numeric_df)
  anomaly_positions = [index for index, label in enumerate(labels) if label == -1]

  anomalies = [
    {
      "row_index": int(numeric_df.index[position]),
      "score": safe_float(scores[position]),
    }
    for position in anomaly_positions[:20]
  ]

  return to_jsonable({
    "available": True,
    "method": "isolation_forest",
    "columns": list(numeric_df.columns),
    "anomaly_count": int(len(anomaly_positions)),
    "anomaly_ratio": safe_float(len(anomaly_positions) / max(len(numeric_df), 1)),
    "anomalies": anomalies,
  })


# Run anomaly detection over the dataframe.
def detect_anomalies(df: pd.DataFrame, roles: dict[str, list[str]]) -> dict[str, Any]:
  result = {
    "univariate": detect_iqr_anomalies(df, roles),
    "multivariate": detect_isolation_forest_anomalies(df, roles),
  }

  return to_jsonable(result)