from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

from analytics_platform_ml.common import safe_float
from analytics_platform_ml.common import to_jsonable


# Select the best time and target columns for forecasting.
def select_forecast_columns(roles: dict[str, list[str]]) -> tuple[str | None, str | None]:
  time_column = roles["datetime_columns"][0] if roles["datetime_columns"] else None
  target_column = roles["measure_columns"][0] if roles["measure_columns"] else None
  return time_column, target_column


# Prepare a time-series dataframe for forecasting.
def prepare_time_series(df: pd.DataFrame, time_column: str, target_column: str) -> pd.DataFrame:
  prepared = df[[time_column, target_column]].copy()
  prepared[time_column] = pd.to_datetime(prepared[time_column], errors="coerce")
  prepared[target_column] = pd.to_numeric(prepared[target_column], errors="coerce")
  prepared = prepared.dropna()
  prepared = prepared.sort_values(time_column)

  if len(prepared) == 0:
    return pd.DataFrame(columns=["ds", "y"])

  prepared["ds"] = prepared[time_column].dt.floor("D")
  prepared["y"] = prepared[target_column]
  prepared = prepared.groupby("ds", as_index=False)["y"].mean()
  prepared = prepared.sort_values("ds")
  return prepared


# Infer a pandas frequency string from a time-series dataframe.
def infer_frequency(series: pd.Series) -> str:
  if len(series) < 3:
    return "D"

  inferred = pd.infer_freq(series)

  if inferred is not None:
    return inferred

  diffs = series.sort_values().diff().dropna()

  if len(diffs) == 0:
    return "D"

  median_days = diffs.median().days

  if median_days >= 28:
    return "MS"

  if median_days >= 7:
    return "W"

  return "D"


# Build future timestamps for sklearn forecasting.
def build_future_dates(last_date: pd.Timestamp, horizon: int, frequency: str) -> list[pd.Timestamp]:
  try:
    future = pd.date_range(start=last_date, periods=horizon + 1, freq=frequency)[1:]
    return list(future)
  except ValueError:
    future = pd.date_range(start=last_date, periods=horizon + 1, freq="D")[1:]
    return list(future)


# Fit an optional Prophet model when the dependency is available.
def forecast_with_prophet(time_series: pd.DataFrame, horizon: int, frequency: str) -> dict[str, Any] | None:
  try:
    from prophet import Prophet
  except ImportError:
    return None

  model = Prophet()
  model.fit(time_series)
  future = model.make_future_dataframe(periods=horizon, freq=frequency)
  forecast = model.predict(future)
  future_forecast = forecast.tail(horizon)

  return {
    "model_type": "prophet",
    "predictions": [
      {
        "date": to_jsonable(row["ds"]),
        "predicted_value": safe_float(row["yhat"]),
        "lower_bound": safe_float(row["yhat_lower"]),
        "upper_bound": safe_float(row["yhat_upper"]),
      }
      for _, row in future_forecast.iterrows()
    ],
  }


# Fit a sklearn trend model as a local fallback.
def forecast_with_linear_regression(time_series: pd.DataFrame, horizon: int, frequency: str) -> dict[str, Any]:
  series = time_series.copy()
  series["step"] = np.arange(len(series))
  x = series[["step"]].to_numpy()
  y = series["y"].to_numpy()

  model = LinearRegression()
  model.fit(x, y)

  future_steps = np.arange(len(series), len(series) + horizon).reshape(-1, 1)
  predictions = model.predict(future_steps)
  future_dates = build_future_dates(series["ds"].max(), horizon, frequency)

  return {
    "model_type": "linear_regression",
    "predictions": [
      {
        "date": to_jsonable(date),
        "predicted_value": safe_float(value),
        "lower_bound": None,
        "upper_bound": None,
      }
      for date, value in zip(future_dates, predictions)
    ],
  }


# Evaluate a simple forecasting baseline on recent history.
def evaluate_forecast(time_series: pd.DataFrame) -> dict[str, Any]:
  if len(time_series) < 8:
    return {
      "available": False,
      "reason": "Not enough historical points for holdout evaluation.",
    }

  holdout_size = max(2, min(5, len(time_series) // 4))
  train = time_series.iloc[:-holdout_size].copy()
  test = time_series.iloc[-holdout_size:].copy()

  train["step"] = np.arange(len(train))
  test["step"] = np.arange(len(train), len(train) + len(test))

  model = LinearRegression()
  model.fit(train[["step"]].to_numpy(), train["y"].to_numpy())
  predicted = model.predict(test[["step"]].to_numpy())

  mse = mean_squared_error(test["y"].to_numpy(), predicted)

  return {
    "available": True,
    "holdout_points": int(holdout_size),
    "mae": safe_float(mean_absolute_error(test["y"].to_numpy(), predicted)),
    "rmse": safe_float(np.sqrt(mse)),
  }


# Generate a forecast for the best available time-series target.
def generate_forecast(df: pd.DataFrame, roles: dict[str, list[str]], horizon: int = 7) -> dict[str, Any]:
  time_column, target_column = select_forecast_columns(roles)

  if time_column is None or target_column is None:
    return {
      "available": False,
      "reason": "Forecasting requires at least one datetime column and one numeric measure column.",
      "history": [],
      "predictions": [],
    }

  time_series = prepare_time_series(df, time_column, target_column)

  if len(time_series) < 5:
    return {
      "available": False,
      "reason": "Not enough valid time-series records for forecasting.",
      "time_column": time_column,
      "target_column": target_column,
      "history": to_jsonable(time_series.to_dict(orient="records")),
      "predictions": [],
    }

  frequency = infer_frequency(time_series["ds"])
  prophet_result = forecast_with_prophet(time_series, horizon, frequency)

  if prophet_result is None:
    model_result = forecast_with_linear_regression(time_series, horizon, frequency)
  else:
    model_result = prophet_result

  result = {
    "available": True,
    "time_column": time_column,
    "target_column": target_column,
    "frequency": frequency,
    "model_type": model_result["model_type"],
    "history": [
      {
        "date": to_jsonable(row["ds"]),
        "actual_value": safe_float(row["y"]),
      }
      for _, row in time_series.tail(30).iterrows()
    ],
    "predictions": model_result["predictions"],
    "evaluation": evaluate_forecast(time_series),
  }

  return to_jsonable(result)