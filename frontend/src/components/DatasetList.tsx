import type { Dataset } from "../types";

type DatasetListProps = {
  datasets: Dataset[];
  selectedDatasetId: string | number | null;
  onSelect: (dataset: Dataset) => void;
};

// Render the user's uploaded datasets.
export function DatasetList({ datasets, selectedDatasetId, onSelect }: DatasetListProps) {
  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Step 2</p>
          <h2>Datasets</h2>
        </div>
        <span className="pill">{datasets.length} total</span>
      </div>

      {datasets.length === 0 ? (
        <p className="muted">No datasets uploaded yet.</p>
      ) : (
        <div className="dataset-list">
          {datasets.map((dataset) => {
            const title = dataset.name || dataset.original_filename || dataset.filename || `Dataset ${dataset.id}`;

            return (
              <button
                key={dataset.id}
                className={dataset.id === selectedDatasetId ? "dataset-item active" : "dataset-item"}
                onClick={() => onSelect(dataset)}
              >
                <span>{title}</span>
                <small>{dataset.status || "unknown"}</small>
              </button>
            );
          })}
        </div>
      )}
    </section>
  );
}