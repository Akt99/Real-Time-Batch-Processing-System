import React, { useState } from "react";
import { uploadJob } from "../api/jobs";

function UploadForm({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setMessage("Choose a CSV file first.");
      return;
    }

    setLoading(true);
    try {
      const data = await uploadJob(file);
      onUploaded(data.job_id);
      setMessage(`Job created: ${data.job_id}`);
    } catch (error) {
      setMessage(error.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Upload CSV</h2>
      <form onSubmit={handleSubmit} className="stack">
        <input type="file" accept=".csv" onChange={(event) => setFile(event.target.files?.[0] || null)} />
        <button type="submit" disabled={loading}>{loading ? "Uploading..." : "Create Job"}</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default UploadForm;
