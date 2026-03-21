import React, { useEffect, useState } from "react";
import { getTransactions } from "../api/jobs";

function TransactionsTable({ jobId }) {
  const [rows, setRows] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [status, setStatus] = useState("");
  const pageSize = 10;

  useEffect(() => {
    if (!jobId) {
      setRows([]);
      return;
    }

    const fetchTransactions = async () => {
      const data = await getTransactions(jobId, {
        page,
        page_size: pageSize,
        ...(status ? { status } : {}),
      });
      setRows(data.items);
      setTotal(data.total);
    };

    fetchTransactions().catch(() => {
      setRows([]);
      setTotal(0);
    });
  }, [jobId, page, status]);

  return (
    <div className="panel">
      <div className="table-header">
        <h2>Transactions</h2>
        <select value={status} onChange={(event) => {
          setStatus(event.target.value);
          setPage(1);
        }}>
          <option value="">All</option>
          <option value="valid">Valid</option>
          <option value="invalid">Invalid</option>
          <option value="suspicious">Suspicious</option>
        </select>
      </div>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Transaction ID</th>
            <th>User ID</th>
            <th>Amount</th>
            <th>Timestamp</th>
            <th>Status</th>
            <th>Error</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              <td>{row.id}</td>
              <td>{row.transaction_id}</td>
              <td>{row.user_id}</td>
              <td>{row.amount ?? "-"}</td>
              <td>{row.timestamp ?? "-"}</td>
              <td>{row.status}</td>
              <td>{row.error_message ?? "-"}</td>
            </tr>
          ))}
          {!rows.length && (
            <tr>
              <td colSpan="7">No transactions to display.</td>
            </tr>
          )}
        </tbody>
      </table>

      <div className="pagination">
        <button type="button" onClick={() => setPage((current) => Math.max(1, current - 1))} disabled={page === 1}>
          Previous
        </button>
        <span>Page {page}</span>
        <button type="button" onClick={() => setPage((current) => current + 1)} disabled={page * pageSize >= total}>
          Next
        </button>
      </div>
    </div>
  );
}

export default TransactionsTable;
