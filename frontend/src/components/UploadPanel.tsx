import { ChangeEvent, useState } from "react";

type UploadPanelProps = {
  onUpload: (file: File) => Promise<void>;
};

// Render the dataset upload panel.
export function UploadPanel({ onUpload }: UploadPanelProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  // Store the selected file from the input.
  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);
  }

  // Upload the selected file to the backend.
  async function handleUpload() {
    if (!selectedFile) {
      return;
    }

    setLoading(true);

    try {
      await onUpload(selectedFile);
      setSelectedFile(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel upload-panel">
      <div>
        <p className="eyebrow">Step 1</p>
        <h2>Upload dataset</h2>
        <p className="muted">
          Upload a CSV or Excel file. The backend will enqueue a Celery job and run the ML analytics pipeline.
        </p>
      </div>

      <div className="upload-controls">
        <input type="file" accept=".csv,.xlsx,.xls" onChange={handleFileChange} />
        <button className="primary-button" onClick={handleUpload} disabled={!selectedFile || loading}>
          {loading ? "Uploading..." : "Upload and analyze"}
        </button>
      </div>

      {selectedFile && (
        <p className="muted small-text">
          Selected: {selectedFile.name}
        </p>
      )}
    </section>
  );
}