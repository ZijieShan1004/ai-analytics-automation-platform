import { useEffect, useState } from "react";
import { AuthPage } from "./components/AuthPage";
import { DatasetList } from "./components/DatasetList";
import { ErrorBanner } from "./components/ErrorBanner";
import { Header } from "./components/Header";
import { JobStatusCard } from "./components/JobStatusCard";
import { LoadingBlock } from "./components/LoadingBlock";
import { ReportDashboard } from "./components/ReportDashboard";
import { UploadPanel } from "./components/UploadPanel";
import {
  getCurrentUser,
  getJob,
  getReportByDataset,
  getToken,
  listDatasets,
  loginUser,
  registerUser,
  removeToken,
  saveToken,
  uploadDataset
} from "./services/api";
import type { Dataset, NormalizedReport, ProcessingJob, User } from "./types";
import { normalizeReport } from "./utils/report";

// Render the main application.
export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<Dataset | null>(null);
  const [currentJob, setCurrentJob] = useState<ProcessingJob | null>(null);
  const [report, setReport] = useState<NormalizedReport | null>(null);
  const [initializing, setInitializing] = useState(true);
  const [loadingReport, setLoadingReport] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load authenticated application state.
  async function loadApplicationState() {
    const token = getToken();

    if (!token) {
      setInitializing(false);
      return;
    }

    try {
      const currentUser = await getCurrentUser();
      const datasetList = await listDatasets();

      setUser(currentUser);
      setDatasets(datasetList);
    } catch {
      removeToken();
      setUser(null);
    } finally {
      setInitializing(false);
    }
  }

  // Refresh the dataset list.
  async function refreshDatasets() {
    const datasetList = await listDatasets();
    setDatasets(datasetList);
  }

  // Handle user login.
  async function handleLogin(email: string, password: string) {
    setError(null);

    try {
      const auth = await loginUser(email, password);
      saveToken(auth.access_token);
      const currentUser = await getCurrentUser();
      const datasetList = await listDatasets();

      setUser(currentUser);
      setDatasets(datasetList);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Login failed.");
    }
  }

  // Handle user registration.
  async function handleRegister(email: string, password: string, fullName: string) {
    setError(null);

    try {
      const auth = await registerUser(email, password, fullName);
      saveToken(auth.access_token);
      const currentUser = await getCurrentUser();
      const datasetList = await listDatasets();

      setUser(currentUser);
      setDatasets(datasetList);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Registration failed.");
    }
  }

  // Handle user logout.
  function handleLogout() {
    removeToken();
    setUser(null);
    setDatasets([]);
    setSelectedDataset(null);
    setCurrentJob(null);
    setReport(null);
    setError(null);
  }

  // Handle dataset upload and job creation.
  async function handleUpload(file: File) {
    setError(null);

    try {
      const response = await uploadDataset(file);
      await refreshDatasets();

      if (response.dataset) {
        setSelectedDataset(response.dataset);
      } else if (response.dataset_id) {
        setSelectedDataset({ id: response.dataset_id });
      }

      if (response.job) {
        setCurrentJob(response.job);
      } else if (response.job_id) {
        const job = await getJob(response.job_id);
        setCurrentJob(job);
      }

      setReport(null);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Upload failed.");
    }
  }

  // Load a report for the selected dataset.
  async function loadReportForDataset(dataset: Dataset) {
    setError(null);
    setLoadingReport(true);
    setSelectedDataset(dataset);

    try {
      const response = await getReportByDataset(dataset.id);
      const normalized = normalizeReport(response);
      setReport(normalized);
    } catch (caughtError) {
      setReport(null);
      setError(caughtError instanceof Error ? caughtError.message : "Report is not available yet.");
    } finally {
      setLoadingReport(false);
    }
  }

  useEffect(() => {
    loadApplicationState();
  }, []);

  useEffect(() => {
    if (!currentJob) {
      return;
    }

    if (!["pending", "running", "queued", "processing"].includes(currentJob.status)) {
      return;
    }

    const intervalId = window.setInterval(async () => {
      try {
        const updatedJob = await getJob(currentJob.id);
        setCurrentJob(updatedJob);

        if (updatedJob.status === "completed" && selectedDataset) {
          await refreshDatasets();
          await loadReportForDataset(selectedDataset);
        }
      } catch (caughtError) {
        setError(caughtError instanceof Error ? caughtError.message : "Failed to refresh job status.");
      }
    }, 2500);

    return () => window.clearInterval(intervalId);
  }, [currentJob, selectedDataset]);

  if (initializing) {
    return (
      <div className="app-shell">
        <LoadingBlock message="Initializing application..." />
      </div>
    );
  }

  if (!user) {
    return (
      <div className="app-shell">
        <Header user={null} onLogout={handleLogout} />
        <ErrorBanner message={error} />
        <AuthPage onLogin={handleLogin} onRegister={handleRegister} />
      </div>
    );
  }

  return (
    <div className="app-shell">
      <Header user={user} onLogout={handleLogout} />
      <ErrorBanner message={error} />

      <main className="dashboard-layout">
        <aside className="sidebar">
          <UploadPanel onUpload={handleUpload} />
          <DatasetList
            datasets={datasets}
            selectedDatasetId={selectedDataset?.id || null}
            onSelect={loadReportForDataset}
          />
          <JobStatusCard job={currentJob} />
        </aside>

        <section className="main-content">
          {loadingReport ? (
            <LoadingBlock message="Loading analytics report..." />
          ) : (
            <ReportDashboard report={report} />
          )}
        </section>
      </main>
    </div>
  );
}