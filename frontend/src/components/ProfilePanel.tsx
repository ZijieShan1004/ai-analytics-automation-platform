import type { ProfilePayload } from "../types";
import { formatValue } from "../utils/report";

type ProfilePanelProps = {
  profile: ProfilePayload | null;
};

// Render dataset profile information.
export function ProfilePanel({ profile }: ProfilePanelProps) {
  if (!profile) {
    return (
      <section className="panel">
        <h2>Dataset Profile</h2>
        <p className="muted">No profile data is available.</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Data profiling</p>
          <h2>Dataset Profile</h2>
        </div>
      </div>

      <div className="metadata-grid">
        <div>
          <span>Rows</span>
          <strong>{formatValue(profile.row_count)}</strong>
        </div>
        <div>
          <span>Columns</span>
          <strong>{formatValue(profile.column_count)}</strong>
        </div>
        <div>
          <span>Missing ratio</span>
          <strong>{formatValue(profile.missing_cell_ratio)}</strong>
        </div>
        <div>
          <span>Duplicate rows</span>
          <strong>{formatValue(profile.duplicate_row_count)}</strong>
        </div>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Column</th>
              <th>Type</th>
              <th>Role</th>
              <th>Nulls</th>
              <th>Unique</th>
            </tr>
          </thead>
          <tbody>
            {(profile.columns || []).slice(0, 12).map((column) => (
              <tr key={column.name}>
                <td>{column.name}</td>
                <td>{column.dtype}</td>
                <td>{column.role}</td>
                <td>{formatValue(column.null_count)}</td>
                <td>{formatValue(column.unique_count)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}