from pathlib import Path
from typing import Any
from uuid import UUID

from app.db.session import SessionLocal
from app.repositories.dataset_repository import DatasetRepository
from app.repositories.job_repository import JobRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.result_repository import ResultRepository
from app.tasks.celery_app import celery_app
from app.utils.dataframe_loader import load_dataframe
from app.utils.json_encoder import to_json_safe


# Normalize ML chart recommendations for database persistence.
def normalize_chart_payloads(raw_charts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized_charts: list[dict[str, Any]] = []

    for chart in raw_charts:
        if not isinstance(chart, dict):
            continue

        x_column = chart.get("x_column") or chart.get("x_axis")
        y_column = chart.get("y_column") or chart.get("y_axis")
        chart_payload = chart.get("chart_payload") or chart.get("config") or chart

        normalized_charts.append(
            {
                "chart_type": chart.get("chart_type", "bar"),
                "title": chart.get("title", "Untitled chart"),
                "x_column": x_column,
                "y_column": y_column,
                "group_by_column": chart.get("group_by_column") or x_column,
                "aggregation": chart.get("aggregation"),
                "confidence_score": chart.get("confidence_score", 0.8),
                "reason": chart.get("reason") or chart.get("description") or "Recommended by the analytics engine.",
                "chart_payload": chart_payload,
            }
        )

    return normalized_charts


# Serialize chart database records for the report payload.
def serialize_chart_results(chart_results: list[Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": str(chart.id),
            "chart_type": chart.chart_type,
            "title": chart.title,
            "x_axis": chart.x_column,
            "y_axis": chart.y_column,
            "x_column": chart.x_column,
            "y_column": chart.y_column,
            "group_by_column": chart.group_by_column,
            "aggregation": chart.aggregation,
            "confidence_score": chart.confidence_score,
            "reason": chart.reason,
            "chart_payload": chart.chart_payload,
            "config": chart.chart_payload,
        }
        for chart in chart_results
    ]


# Build the complete report payload for frontend rendering.
def build_full_report_payload(
    pipeline_result: dict[str, Any],
    chart_results: list[Any],
) -> dict[str, Any]:
    chart_recommendations = pipeline_result.get("chart_recommendations", [])
    serialized_charts = serialize_chart_results(chart_results)

    return to_json_safe(
        {
            "profile": pipeline_result.get("profile", {}),
            "analytics": pipeline_result.get("analytics", {}),
            "anomalies": pipeline_result.get("anomalies", {}),
            "chart_recommendations": chart_recommendations,
            "charts": serialized_charts if serialized_charts else chart_recommendations,
            "forecast": pipeline_result.get("forecast", {}),
            "summary": pipeline_result.get("summary", {}),
            "report": pipeline_result.get("report", {}),
        }
    )


# Process a dataset through the full analytics pipeline.
@celery_app.task(name="process_dataset_job")
def process_dataset_job(job_id: str) -> dict:
    db = SessionLocal()

    try:
        parsed_job_id = UUID(job_id)
        job_repository = JobRepository(db)
        dataset_repository = DatasetRepository(db)
        result_repository = ResultRepository(db)
        report_repository = ReportRepository(db)

        job = job_repository.mark_running(parsed_job_id, progress=5)

        if job is None:
            return {"status": "failed", "error": "Job not found"}

        dataset_repository.update_status(job.dataset_id, "processing")
        job_repository.update_progress(parsed_job_id, 10)

        dataset = dataset_repository.get_owned(job.dataset_id, job.user_id)

        if dataset is None:
            raise ValueError("Dataset not found")

        file_path = Path(dataset.uploaded_file.file_path)
        dataframe = load_dataframe(file_path)
        job_repository.update_progress(parsed_job_id, 20)

        from analytics_platform_ml.pipeline import run_full_pipeline

        pipeline_result = run_full_pipeline(
            dataframe=dataframe,
            dataset_name=dataset.name,
        )

        analytics_payload = to_json_safe(pipeline_result.get("analytics", {}))
        raw_chart_payloads = to_json_safe(pipeline_result.get("chart_recommendations", []))
        chart_payloads = normalize_chart_payloads(raw_chart_payloads)
        forecast_payload = to_json_safe(pipeline_result.get("forecast", {}))
        summary_payload = to_json_safe(pipeline_result.get("summary", {}))

        job_repository.update_progress(parsed_job_id, 55)
        analytics_result = result_repository.create_analytics_result(
            dataset.id,
            job.id,
            analytics_payload,
        )

        job_repository.update_progress(parsed_job_id, 65)
        chart_results = result_repository.create_chart_recommendations(
            dataset.id,
            analytics_result.id,
            chart_payloads,
        )

        job_repository.update_progress(parsed_job_id, 75)
        forecast_result = result_repository.create_forecast_result(
            dataset.id,
            job.id,
            forecast_payload,
        )

        job_repository.update_progress(parsed_job_id, 85)
        ai_summary = result_repository.create_ai_summary(
            dataset.id,
            job.id,
            summary_payload,
        )

        report_payload = build_full_report_payload(
            pipeline_result=pipeline_result,
            chart_results=chart_results,
        )

        report = report_repository.create(
            user_id=job.user_id,
            dataset_id=dataset.id,
            analytics_result_id=analytics_result.id,
            forecast_result_id=forecast_result.id,
            ai_summary_id=ai_summary.id,
            title=f"Analytics Report for {dataset.name}",
            report_payload=report_payload,
        )

        dataset_repository.update_status(dataset.id, "completed")
        job_repository.mark_completed(parsed_job_id)

        return {"status": "completed", "report_id": str(report.id)}
    except Exception as exc:
        if "parsed_job_id" in locals():
            JobRepository(db).mark_failed(parsed_job_id, str(exc))

        if "job" in locals() and job is not None:
            DatasetRepository(db).update_status(job.dataset_id, "failed")

        return {"status": "failed", "error": str(exc)}
    finally:
        db.close()