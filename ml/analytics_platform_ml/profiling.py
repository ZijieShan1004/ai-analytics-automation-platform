from __future__ import annotations

from typing import Any

import pandas as pd

from analytics_platform_ml.common import build_preview_rows
from analytics_platform_ml.common import infer_column_roles
from analytics_platform_ml.common import safe_float
from analytics_platform_ml.common import to_jsonable


# Build numeric statistics for one column.
def build_numeric_profile(series: pd.Series) -> dict[str, Any]:
  numeric = pd.to_numeric(series, errors="coerce").dropna()

  if len(numeric) == 0:
    return {}

  return {
    "min": safe_float(numeric.min()),
    "max": safe_float(numeric.max()),
    "mean": safe_float(numeric.mean()),
    "median": safe_float(numeric.median()),
    "std": safe_float(numeric.std()),
    "q1": safe_float(numeric.quantile(0.25)),
    "q3": safe_float(numeric.quantile(0.75)),
    "sum": safe_float(numeric.sum()),
  }


# Build categorical statistics for one column.
def build_categorical_profile(series: pd.Series, limit: int = 5) -> dict[str, Any]:
  values = series.dropna()

  if len(values) == 0:
    return {"top_values": []}

  counts = values.astype(str).value_counts().head(limit)

  return {
    "top_values": [
      {
        "value": to_jsonable(index),
        "count": int(count),
        "percentage": safe_float(count / max(len(values), 1)),
      }
      for index, count in counts.items()
    ]
  }


# Build datetime statistics for one column.
def build_datetime_profile(series: pd.Series) -> dict[str, Any]:
  parsed = pd.to_datetime(series, errors="coerce").dropna()

  if len(parsed) == 0:
    return {}

  return {
    "min": to_jsonable(parsed.min()),
    "max": to_jsonable(parsed.max()),
    "range_days": safe_float((parsed.max() - parsed.min()).days),
  }


# Build a profile for one dataframe column.
def build_column_profile(df: pd.DataFrame, column: str, roles: dict[str, list[str]]) -> dict[str, Any]:
  series = df[column]
  non_null_count = int(series.notna().sum())
  null_count = int(series.isna().sum())
  unique_count = int(series.dropna().nunique())

  role = "unknown"

  if column in roles["measure_columns"]:
    role = "measure"
  elif column in roles["datetime_columns"]:
    role = "datetime"
  elif column in roles["dimension_columns"]:
    role = "dimension"
  elif column in roles["id_columns"]:
    role = "identifier"
  elif column in roles["text_columns"]:
    role = "text"
  elif column in roles["boolean_columns"]:
    role = "boolean"

  profile: dict[str, Any] = {
    "name": column,
    "dtype": str(series.dtype),
    "role": role,
    "non_null_count": non_null_count,
    "null_count": null_count,
    "null_ratio": safe_float(null_count / max(len(df), 1)),
    "unique_count": unique_count,
    "unique_ratio": safe_float(unique_count / max(len(df), 1)),
  }

  if column in roles["measure_columns"]:
    profile["numeric"] = build_numeric_profile(series)

  if column in roles["dimension_columns"] or column in roles["boolean_columns"]:
    profile["categorical"] = build_categorical_profile(series)

  if column in roles["datetime_columns"]:
    profile["datetime"] = build_datetime_profile(series)

  return to_jsonable(profile)


# Build a complete dataframe profile.
def profile_dataframe(df: pd.DataFrame) -> dict[str, Any]:
  roles = infer_column_roles(df)
  row_count = int(len(df))
  column_count = int(len(df.columns))
  missing_cells = int(df.isna().sum().sum())
  total_cells = int(max(row_count * column_count, 1))

  column_profiles = [
    build_column_profile(df, column, roles)
    for column in df.columns
  ]

  profile = {
    "row_count": row_count,
    "column_count": column_count,
    "memory_usage_bytes": int(df.memory_usage(deep=True).sum()),
    "duplicate_row_count": int(df.duplicated().sum()),
    "missing_cell_count": missing_cells,
    "missing_cell_ratio": safe_float(missing_cells / total_cells),
    "roles": roles,
    "columns": column_profiles,
    "preview_rows": build_preview_rows(df),
  }

  return to_jsonable(profile)