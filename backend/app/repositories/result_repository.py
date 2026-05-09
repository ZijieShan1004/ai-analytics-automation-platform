from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ai_generated_summary import AIGeneratedSummary
from app.models.analytics_result import AnalyticsResult
from app.models.chart_recommendation import ChartRecommendation
from app.models.forecast_result import ForecastResult


class ResultRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create an analytics result record.
    def create_analytics_result(self, dataset_id: UUID, job_id: UUID, payload: dict) -> AnalyticsResult:
        result = AnalyticsResult(
            dataset_id=dataset_id,
            job_id=job_id,
            numeric_columns=payload.get("numeric_columns", []),
            categorical_columns=payload.get("categorical_columns", []),
            datetime_columns=payload.get("datetime_columns", []),
            missing_value_summary=payload.get("missing_value_summary", {}),
            outlier_summary=payload.get("outlier_summary", {}),
            correlation_matrix=payload.get("correlation_matrix", {}),
            kpi_summary=payload.get("kpi_summary", {}),
            trend_summary=payload.get("trend_summary", {}),
            anomaly_summary=payload.get("anomaly_summary", {}),
        )
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result

    # Create chart recommendation records.
    def create_chart_recommendations(
        self,
        dataset_id: UUID,
        analytics_result_id: UUID,
        payloads: list[dict],
    ) -> list[ChartRecommendation]:
        charts = []

        for payload in payloads:
            chart = ChartRecommendation(
                dataset_id=dataset_id,
                analytics_result_id=analytics_result_id,
                chart_type=payload.get("chart_type", "unknown"),
                title=payload.get("title", "Untitled Chart"),
                x_column=payload.get("x_column"),
                y_column=payload.get("y_column"),
                group_by_column=payload.get("group_by_column"),
                aggregation=payload.get("aggregation"),
                confidence_score=payload.get("confidence_score", 0.0),
                reason=payload.get("reason", ""),
                chart_payload=payload.get("chart_payload", {}),
            )
            self.db.add(chart)
            charts.append(chart)

        self.db.commit()

        for chart in charts:
            self.db.refresh(chart)

        return charts

    # Create a forecast result record.
    def create_forecast_result(self, dataset_id: UUID, job_id: UUID, payload: dict) -> ForecastResult:
        result = ForecastResult(
            dataset_id=dataset_id,
            job_id=job_id,
            datetime_column=payload.get("datetime_column"),
            target_column=payload.get("target_column"),
            model_type=payload.get("model_type", "none"),
            forecast_horizon=payload.get("forecast_horizon", 0),
            metrics=payload.get("metrics", {}),
            forecast_values=payload.get("forecast_values", []),
            confidence_intervals=payload.get("confidence_intervals", []),
        )
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result

    # Create an AI-generated summary record.
    def create_ai_summary(self, dataset_id: UUID, job_id: UUID, payload: dict) -> AIGeneratedSummary:
        summary = AIGeneratedSummary(
            dataset_id=dataset_id,
            job_id=job_id,
            summary_type=payload.get("summary_type", "executive"),
            prompt_version=payload.get("prompt_version", "v1"),
            input_facts=payload.get("input_facts", {}),
            generated_text=payload.get("generated_text", ""),
        )
        self.db.add(summary)
        self.db.commit()
        self.db.refresh(summary)
        return summary

    # Get the latest analytics result for a dataset.
    def get_latest_analytics_result(self, dataset_id: UUID) -> AnalyticsResult | None:
        statement = (
            select(AnalyticsResult)
            .where(AnalyticsResult.dataset_id == dataset_id)
            .order_by(AnalyticsResult.created_at.desc())
        )
        return self.db.scalar(statement)

    # Get chart recommendations for a dataset.
    def list_chart_recommendations(self, dataset_id: UUID) -> list[ChartRecommendation]:
        statement = (
            select(ChartRecommendation)
            .where(ChartRecommendation.dataset_id == dataset_id)
            .order_by(ChartRecommendation.created_at.desc())
        )
        return list(self.db.scalars(statement).all())

    # Get the latest forecast result for a dataset.
    def get_latest_forecast_result(self, dataset_id: UUID) -> ForecastResult | None:
        statement = (
            select(ForecastResult)
            .where(ForecastResult.dataset_id == dataset_id)
            .order_by(ForecastResult.created_at.desc())
        )
        return self.db.scalar(statement)