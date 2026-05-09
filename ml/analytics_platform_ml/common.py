from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


# Convert a value into a JSON-safe Python object.
def to_jsonable(value: Any) -> Any:
  if value is None:
    return None

  if isinstance(value, (np.integer,)):
    return int(value)

  if isinstance(value, (np.floating,)):
    if np.isnan(value) or np.isinf(value):
      return None
    return float(value)

  if isinstance(value, (np.bool_,)):
    return bool(value)

  if isinstance(value, (pd.Timestamp,)):
    if pd.isna(value):
      return None
    return value.isoformat()

  if isinstance(value, (pd.Timedelta,)):
    return str(value)

  if isinstance(value, float):
    if np.isnan(value) or np.isinf(value):
      return None
    return value

  if isinstance(value, dict):
    return {str(key): to_jsonable(item) for key, item in value.items()}

  if isinstance(value, list):
    return [to_jsonable(item) for item in value]

  if pd.isna(value):
    return None

  return value


# Convert a value into a safe float.
def safe_float(value: Any) -> float | None:
  try:
    number = float(value)
  except (TypeError, ValueError):
    return None

  if np.isnan(number) or np.isinf(number):
    return None

  return number


# Convert a value into a safe integer.
def safe_int(value: Any) -> int | None:
  try:
    return int(value)
  except (TypeError, ValueError):
    return None


# Clean a dataframe before analysis.
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
  cleaned = df.copy()
  cleaned = cleaned.dropna(axis=0, how="all")
  cleaned = cleaned.dropna(axis=1, how="all")
  cleaned.columns = [str(column).strip() for column in cleaned.columns]
  return cleaned


# Estimate whether an object column can be parsed as dates.
def try_parse_datetime(series: pd.Series) -> tuple[pd.Series, float]:
  non_null = series.dropna()

  if len(non_null) == 0:
    return pd.Series(pd.NaT, index=series.index), 0.0

  parsed = pd.to_datetime(series, errors="coerce", utc=False)
  success_rate = float(parsed.notna().sum() / max(series.notna().sum(), 1))
  return parsed, success_rate


# Infer semantic roles for dataframe columns.
def infer_column_roles(df: pd.DataFrame) -> dict[str, list[str]]:
  row_count = len(df)

  numeric_columns: list[str] = []
  datetime_columns: list[str] = []
  categorical_columns: list[str] = []
  boolean_columns: list[str] = []
  text_columns: list[str] = []
  id_columns: list[str] = []

  id_name_tokens = [
    "id",
    "_id",
    "uuid",
    "guid",
    "key",
    "code",
    "number",
    "no",
  ]

  measure_name_tokens = [
    "revenue",
    "sales",
    "cost",
    "price",
    "amount",
    "total",
    "profit",
    "margin",
    "orders",
    "quantity",
    "qty",
    "count",
    "rate",
    "score",
    "value",
    "income",
    "expense",
    "spend",
    "budget",
  ]

  for column in df.columns:
    series = df[column]
    column_name = str(column).strip().lower()
    non_null = series.dropna()
    unique_count = int(non_null.nunique()) if len(non_null) > 0 else 0
    unique_ratio = unique_count / max(row_count, 1)

    name_suggests_measure = any(token in column_name for token in measure_name_tokens)
    name_suggests_id = (
      column_name == "id"
      or column_name.endswith("_id")
      or column_name.endswith(" id")
      or any(token == column_name for token in id_name_tokens)
      or "uuid" in column_name
      or "guid" in column_name
    )

    if pd.api.types.is_bool_dtype(series):
      boolean_columns.append(column)
      categorical_columns.append(column)
      continue

    if pd.api.types.is_datetime64_any_dtype(series):
      datetime_columns.append(column)
      continue

    if pd.api.types.is_numeric_dtype(series):
      numeric_columns.append(column)

      if name_suggests_id and not name_suggests_measure:
        id_columns.append(column)
        continue

      if unique_count <= 20 and unique_ratio <= 0.2:
        categorical_columns.append(column)

      continue

    parsed, success_rate = try_parse_datetime(series)

    if success_rate >= 0.8:
      datetime_columns.append(column)
      continue

    average_length = float(non_null.astype(str).str.len().mean()) if len(non_null) > 0 else 0.0

    if average_length >= 40 and unique_ratio >= 0.5:
      text_columns.append(column)
    else:
      categorical_columns.append(column)

    if name_suggests_id and not name_suggests_measure:
      id_columns.append(column)

  measure_columns = [
    column for column in numeric_columns
    if column not in id_columns and column not in boolean_columns
  ]

  dimension_columns = [
    column for column in categorical_columns
    if column not in id_columns and column not in text_columns
  ]

  return {
    "numeric_columns": list(dict.fromkeys(numeric_columns)),
    "datetime_columns": list(dict.fromkeys(datetime_columns)),
    "categorical_columns": list(dict.fromkeys(categorical_columns)),
    "boolean_columns": list(dict.fromkeys(boolean_columns)),
    "text_columns": list(dict.fromkeys(text_columns)),
    "id_columns": list(dict.fromkeys(id_columns)),
    "measure_columns": list(dict.fromkeys(measure_columns)),
    "dimension_columns": list(dict.fromkeys(dimension_columns)),
  }


# Build a compact row preview for reports.
def build_preview_rows(df: pd.DataFrame, limit: int = 5) -> list[dict[str, Any]]:
  records = df.head(limit).to_dict(orient="records")
  return [to_jsonable(record) for record in records]