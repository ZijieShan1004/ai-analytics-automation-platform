import type {
  AuthResponse,
  Dataset,
  DatasetUploadResponse,
  ProcessingJob,
  ReportResponse,
  User
} from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const TOKEN_KEY = "ai_analytics_access_token";

export class ApiError extends Error {
  status: number;

  // Create an API error with status metadata.
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

// Save the current access token.
export function saveToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

// Read the current access token.
export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

// Remove the current access token.
export function removeToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

// Build authorization headers for authenticated requests.
function buildAuthHeaders(): HeadersInit {
  const token = getToken();

  if (!token) {
    return {};
  }

  return {
    Authorization: `Bearer ${token}`
  };
}

// Parse an API response into JSON when possible.
async function parseResponse(response: Response): Promise<unknown> {
  const contentType = response.headers.get("content-type");

  if (!contentType || !contentType.includes("application/json")) {
    return null;
  }

  return response.json();
}

// Send a request to the backend API.
async function apiRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      ...buildAuthHeaders(),
      ...(options.headers || {})
    }
  });

  const payload = await parseResponse(response);

  if (!response.ok) {
    const errorPayload = payload as { detail?: string; message?: string } | null;
    const message = errorPayload?.detail || errorPayload?.message || `API request failed with status ${response.status}`;
    throw new ApiError(message, response.status);
  }

  return payload as T;
}

// Register a new user account.
export async function registerUser(email: string, password: string, fullName: string): Promise<AuthResponse> {
  return apiRequest<AuthResponse>("/api/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email,
      password,
      full_name: fullName
    })
  });
}

// Log in an existing user account.
export async function loginUser(email: string, password: string): Promise<AuthResponse> {
  return apiRequest<AuthResponse>("/api/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email,
      password
    })
  });
}

// Fetch the current authenticated user.
export async function getCurrentUser(): Promise<User> {
  return apiRequest<User>("/api/users/me");
}

// Upload a dataset file for asynchronous processing.
export async function uploadDataset(file: File): Promise<DatasetUploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  return apiRequest<DatasetUploadResponse>("/api/datasets/upload", {
    method: "POST",
    body: formData
  });
}

// Fetch datasets owned by the current user.
export async function listDatasets(): Promise<Dataset[]> {
  return apiRequest<Dataset[]>("/api/datasets");
}

// Fetch one dataset by identifier.
export async function getDataset(datasetId: string | number): Promise<Dataset> {
  return apiRequest<Dataset>(`/api/datasets/${datasetId}`);
}

// Fetch one processing job by identifier.
export async function getJob(jobId: string | number): Promise<ProcessingJob> {
  return apiRequest<ProcessingJob>(`/api/jobs/${jobId}`);
}

// Fetch the generated report for a dataset.
export async function getReportByDataset(datasetId: string | number): Promise<ReportResponse> {
  return apiRequest<ReportResponse>(`/api/reports/by-dataset/${datasetId}`);
}

// Fetch a generated report by report identifier.
export async function getReport(reportId: string | number): Promise<ReportResponse> {
  return apiRequest<ReportResponse>(`/api/reports/${reportId}`);
}