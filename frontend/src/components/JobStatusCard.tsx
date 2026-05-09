import type { ProcessingJob } from "../types";

type JobStatusCardProps = {
  job: ProcessingJob | null;
};

// Render the current processing job status.
export function JobStatusCard({ job }: JobStatusCardProps) {
  if (!job) {
    return null;
  }

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Step 3</p>
          <h2>Processing job</h2>
        </div>
        <span className={`status-badge status-${job.status}`}>
          {job.status}
        </span>
      </div>

      {job.error_message && (
        <p className="error-text">{job.error_message}</p>
      )}

      <div className="metadata-grid">
        <div>
          <span>Job ID</span>
          <strong>{job.id}</strong>
        </div>
        <div>
          <span>Dataset ID</span>
          <strong>{job.dataset_id || "N/A"}</strong>
        </div>
        <div>
          <span>Completed</span>
          <strong>{job.completed_at || "Not yet"}</strong>
        </div>
      </div>
    </section>
  );
}