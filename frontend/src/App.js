import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import JobDashboard from "./components/JobDashboard";
import TransactionsTable from "./components/TransactionsTable";
import { startJob } from "./api/jobs";

function App() {
  const [jobId, setJobId] = useState("");
  const [jobStarted, setJobStarted] = useState(false);

  const handleStart = async () => {
    if (!jobId) {
      return;
    }

    await startJob(jobId);
    setJobStarted(true);
  };

  return (
    <main className="app-shell">
      <section className="hero">
        <p className="eyebrow">A Real-Time Batch Processing System</p>
        <h1>Welcome to the dashboard</h1>
        <p className="subtitle">
          Upload transaction CSVs, process them in durable batches, and monitor validation results in near real time.
        </p>
      </section>

      <section className="panel-grid">
        <UploadForm onUploaded={(uploadedJobId) => {
          setJobId(uploadedJobId);
          setJobStarted(false);
        }} />

        <JobDashboard jobId={jobId} jobStarted={jobStarted} onStart={handleStart} />
      </section>

      <section className="panel-full">
        <TransactionsTable jobId={jobId} />
      </section>
    </main>
  );
}

export default App;
