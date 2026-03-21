import client from "./client";

export async function uploadJob(file) {
  const formData = new FormData();
  formData.append("file", file);
  const response = await client.post("/jobs", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export async function startJob(jobId) {
  const response = await client.post(`/jobs/${jobId}/start`);
  return response.data;
}

export async function getJob(jobId) {
  const response = await client.get(`/jobs/${jobId}`);
  return response.data;
}

export async function getTransactions(jobId, params) {
  const response = await client.get(`/jobs/${jobId}/transactions`, { params });
  return response.data;
}
