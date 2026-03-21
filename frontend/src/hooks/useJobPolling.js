import { useEffect, useState } from "react";
import { getJob } from "../api/jobs";

function useJobPolling(jobId, enabled) {
  const [job, setJob] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!jobId || !enabled) {
      return undefined;
    }

    let cancelled = false;

    const poll = async () => {
      try {
        const data = await getJob(jobId);
        if (!cancelled) {
          setJob(data);
          setError("");
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.response?.data?.detail || "Unable to fetch job status");
        }
      }
    };

    poll();
    const interval = setInterval(poll, 2500);

    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, [jobId, enabled]);

  return { job, error };
}

export default useJobPolling;
