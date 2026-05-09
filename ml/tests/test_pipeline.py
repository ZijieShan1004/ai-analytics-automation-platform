import pandas as pd

from analytics_platform_ml.pipeline import run_full_pipeline


# Test that the full pipeline returns all major report sections.
def test_run_full_pipeline_returns_expected_sections():
  df = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=12, freq="D"),
    "region": ["East", "West", "East", "West", "East", "West", "East", "West", "East", "West", "East", "West"],
    "revenue": [100, 120, 130, 140, 150, 170, 160, 180, 190, 210, 220, 240],
    "cost": [50, 60, 63, 70, 71, 85, 80, 90, 95, 105, 110, 120],
  })

  result = run_full_pipeline(df, dataset_name="sample_sales")

  assert "profile" in result
  assert "analytics" in result
  assert "anomalies" in result
  assert "chart_recommendations" in result
  assert "forecast" in result
  assert "summary" in result
  assert "report" in result


# Test that profiling detects rows and columns correctly.
def test_pipeline_profile_counts_rows_and_columns():
  df = pd.DataFrame({
    "category": ["A", "B", "A"],
    "value": [1, 2, 3],
  })

  result = run_full_pipeline(df)

  assert result["profile"]["row_count"] == 3
  assert result["profile"]["column_count"] == 2


# Test that chart recommendations are generated for usable data.
def test_pipeline_generates_chart_recommendations():
  df = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=10, freq="D"),
    "category": ["A", "B"] * 5,
    "sales": [10, 12, 14, 15, 16, 19, 21, 22, 24, 25],
  })

  result = run_full_pipeline(df)

  assert len(result["chart_recommendations"]) > 0