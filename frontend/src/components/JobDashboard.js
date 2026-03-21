import React from "react";
import useJobPolling from "../hooks/useJobPolling";

function JobDashboard({ jobId, jobStarted, onStart }) {
  const { job, error } = useJobPolling(jobId, Boolean(jobId));

  return (
    <div className="panel">
      <h2>Job Progress</h2>
      <div className="stack">
        <p><strong>Job ID:</strong> {jobId || "No job selected yet"}</p>
        <button type="button" onClick={onStart} disabled={!jobId || jobStarted || job?.status === "running"}>
          {job?.status === "running" ? "Processing..." : "Start Job"}
        </button>

        {job && (
          <>
            <div className="progress-track">
              <div className="progress-fill" style={{ width: `${job.progress_percent || 0}%` }} />
            </div>
            <div className="stats-grid">
              <div className="stat-card"><span>Status</span><strong>{job.status}</strong></div>
              <div className="stat-card"><span>Processed</span><strong>{job.processed_records}</strong></div>
              <div className="stat-card"><span>Valid</span><strong>{job.valid_records}</strong></div>
              <div className="stat-card"><span>Invalid</span><strong>{job.invalid_records}</strong></div>
              <div className="stat-card"><span>Suspicious</span><strong>{job.suspicious_records}</strong></div>
            </div>
          </>
        )}

        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
}

export default JobDashboard;
