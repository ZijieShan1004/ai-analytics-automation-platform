export type User = {
  id: number;
  email: string;
  full_name?: string | null;
  is_active?: boolean;
};

export type AuthResponse = {
  access_token: string;
  token_type: string;
};

export type Dataset = {
  id: string | number;
  user_id?: string | number;
  uploaded_file_id?: string | number;
  name?: string;
  original_filename?: string;
  filename?: string;
  status?: string;
  row_count?: number | null;
  column_count?: number | null;
  created_at?: string;
  updated_at?: string;
};

export type ProcessingJob = {
  id: string | number;
  dataset_id?: string | number;
  status: string;
  error_message?: string | null;
  created_at?: string;
  updated_at?: string;
  completed_at?: string | null;
};

export type DatasetUploadResponse = {
  dataset?: Dataset;
  job?: ProcessingJob;
  dataset_id?: string | number;
  job_id?: string | number;
  message?: string;
};

export type ReportResponse = {
  id?: string | number;
  dataset_id?: string | number;
  title?: string;
  content?: unknown;
  report_payload?: unknown;
  sections?: ReportSection[];
  created_at?: string;
  updated_at?: string;
};

export type ReportSection = {
  name: string;
  type: string;
  content: unknown;
};

export type NormalizedReport = {
  title: string;
  dataset_name?: string | null;
  sections: ReportSection[];
};

export type ApiErrorPayload = {
  detail?: string;
  message?: string;
};

export type KpiItem = {
  name: string;
  value: string | number | boolean | null;
  type?: string;
  column?: string;
  description?: string;
};

export type ChartRecommendation = {
  chart_type: string;
  title: string;
  description?: string;
  x_axis?: string | null;
  y_axis?: string | null;
  aggregation?: string | null;
  reason?: string;
  config?: Record<string, unknown>;
};

export type ForecastPoint = {
  date: string;
  actual_value?: number | null;
  predicted_value?: number | null;
  lower_bound?: number | null;
  upper_bound?: number | null;
};

export type ForecastPayload = {
  available: boolean;
  reason?: string;
  time_column?: string;
  target_column?: string;
  frequency?: string;
  model_type?: string;
  history?: ForecastPoint[];
  predictions?: ForecastPoint[];
  evaluation?: Record<string, unknown>;
};

export type ProfileColumn = {
  name: string;
  dtype: string;
  role: string;
  non_null_count: number;
  null_count: number;
  null_ratio: number | null;
  unique_count: number;
  unique_ratio: number | null;
};

export type ProfilePayload = {
  row_count?: number;
  column_count?: number;
  memory_usage_bytes?: number;
  duplicate_row_count?: number;
  missing_cell_count?: number;
  missing_cell_ratio?: number | null;
  roles?: Record<string, string[]>;
  columns?: ProfileColumn[];
  preview_rows?: Record<string, unknown>[];
};

export type SummaryPayload = {
  provider?: string;
  model?: string;
  executive_summary?: string;
  key_findings?: string[];
  recommended_actions?: string[];
  llm_prompt?: string;
};