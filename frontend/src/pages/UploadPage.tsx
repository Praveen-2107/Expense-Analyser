import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';

import { useAuth } from '../context/AuthContext';
import { fetchStatements, uploadCsvFile, uploadPdfFile } from '../services/uploadService';
import type { UploadResponse, UploadStatement } from '../types/upload';

type UploadMode = 'csv' | 'pdf';

export function UploadPage() {
  const { user } = useAuth();
  const [mode, setMode] = useState<UploadMode>('csv');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<UploadResponse | null>(null);
  const [statements, setStatements] = useState<UploadStatement[]>([]);

  useEffect(() => {
    fetchStatements()
      .then(setStatements)
      .catch(() => setStatements([]));
  }, []);

  const fileAccept = useMemo(() => (mode === 'csv' ? '.csv,text/csv' : '.pdf,application/pdf'), [mode]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null;
    setSelectedFile(file);
    setError('');
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError('');

    if (!selectedFile) {
      setError('Please choose a file before uploading.');
      return;
    }

    setIsSubmitting(true);
    try {
      const response = mode === 'csv' ? await uploadCsvFile(selectedFile) : await uploadPdfFile(selectedFile);
      setResult(response);
      const updatedStatements = await fetchStatements();
      setStatements(updatedStatements);
      setSelectedFile(null);
    } catch (uploadError) {
      setError(uploadError instanceof Error ? uploadError.message : 'Upload failed. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="upload-shell min-vh-100 py-4 py-lg-5 px-3 px-lg-4">
      <section className="container-fluid dashboard-container">
        <div className="upload-header card border-0 shadow-sm rounded-4 mb-4 overflow-hidden">
          <div className="card-body p-4 p-lg-5 upload-hero">
            <div className="d-flex flex-column flex-xl-row justify-content-between gap-4 align-items-xl-center">
              <div className="text-white">
                <p className="text-uppercase small fw-semibold mb-2 text-white-50">Statement Upload</p>
                <h1 className="display-6 fw-bold mb-3">Import CSV or PDF bank statements</h1>
                <p className="lead mb-0 text-white-75 dashboard-subtitle">
                  Upload bank files to create statement history and automatically import supported CSV transactions.
                </p>
              </div>
              <div className="d-flex flex-wrap gap-3">
                <Link className="btn btn-light btn-lg fw-semibold" to="/dashboard">
                  Back to dashboard
                </Link>
                <span className="badge rounded-pill text-bg-light text-secondary px-3 py-2 align-self-start">
                  Signed in as {user?.fullName}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="row g-4">
          <div className="col-12 col-xl-5">
            <section className="analytics-card rounded-4 p-4 p-lg-5 h-100">
              <div className="d-flex gap-2 mb-4">
                <button
                  type="button"
                  className={`btn btn-lg flex-fill ${mode === 'csv' ? 'btn-primary' : 'btn-outline-primary'}`}
                  onClick={() => setMode('csv')}
                >
                  CSV Upload
                </button>
                <button
                  type="button"
                  className={`btn btn-lg flex-fill ${mode === 'pdf' ? 'btn-primary' : 'btn-outline-primary'}`}
                  onClick={() => setMode('pdf')}
                >
                  PDF Upload
                </button>
              </div>

              <form className="d-grid gap-3" onSubmit={handleSubmit}>
                <div>
                  <label className="form-label fw-semibold">Choose file</label>
                  <input className="form-control form-control-lg" type="file" accept={fileAccept} onChange={handleFileChange} />
                </div>

                <div className="upload-note rounded-4 p-3">
                  <p className="mb-0 text-secondary">
                    CSV statements are parsed into income and expense records when the file has recognizable columns.
                    PDF statements are saved and text-extracted for review.
                  </p>
                </div>

                {error ? <div className="alert alert-danger mb-0">{error}</div> : null}

                <button className="btn btn-primary btn-lg" type="submit" disabled={isSubmitting}>
                  {isSubmitting ? 'Uploading...' : 'Upload Statement'}
                </button>
              </form>
            </section>
          </div>

          <div className="col-12 col-xl-7">
            <section className="analytics-card rounded-4 p-4 p-lg-5 mb-4">
              <p className="text-uppercase small text-secondary fw-semibold mb-1">Latest Result</p>
              <h2 className="h4 fw-bold mb-3">Upload summary</h2>

              {result ? (
                <>
                  <p className="text-secondary mb-4">{result.summary}</p>
                  <div className="row g-3 mb-4">
                    <div className="col-md-4">
                      <div className="info-tile rounded-4 p-3 h-100">
                        <p className="text-secondary small mb-1">Transactions</p>
                        <h4 className="h5 fw-bold mb-0">{result.total_transactions}</h4>
                      </div>
                    </div>
                    <div className="col-md-4">
                      <div className="info-tile rounded-4 p-3 h-100">
                        <p className="text-secondary small mb-1">Expenses created</p>
                        <h4 className="h5 fw-bold mb-0">{result.imported_expenses}</h4>
                      </div>
                    </div>
                    <div className="col-md-4">
                      <div className="info-tile rounded-4 p-3 h-100">
                        <p className="text-secondary small mb-1">Income created</p>
                        <h4 className="h5 fw-bold mb-0">{result.imported_incomes}</h4>
                      </div>
                    </div>
                  </div>

                  {result.transactions.length > 0 ? (
                    <div className="table-responsive">
                      <table className="table align-middle mb-0">
                        <thead>
                          <tr>
                            <th>Title</th>
                            <th>Type</th>
                            <th>Amount</th>
                            <th>Category</th>
                          </tr>
                        </thead>
                        <tbody>
                          {result.transactions.slice(0, 5).map((transaction) => (
                            <tr key={`${transaction.title}-${transaction.amount}-${transaction.transaction_date ?? 'na'}`}>
                              <td>{transaction.title}</td>
                              <td>{transaction.entry_type}</td>
                              <td>{transaction.amount}</td>
                              <td>{transaction.category_name ?? 'Uncategorized'}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <div className="insight-card rounded-4 p-3">
                      <p className="mb-0 text-secondary">PDF uploads do not create transaction rows, but they are stored and summarized.</p>
                    </div>
                  )}
                </>
              ) : (
                <div className="insight-card rounded-4 p-3">
                  <p className="mb-0 text-secondary">Upload a bank statement to see parsed results here.</p>
                </div>
              )}
            </section>

            <section className="analytics-card rounded-4 p-4 p-lg-5">
              <p className="text-uppercase small text-secondary fw-semibold mb-1">Statement History</p>
              <h2 className="h4 fw-bold mb-4">Recent uploads</h2>

              <div className="list-group list-group-flush">
                {statements.length > 0 ? (
                  statements.map((statement) => (
                    <div className="list-group-item px-0 py-3 border-0 transaction-row" key={statement.id}>
                      <div className="d-flex justify-content-between align-items-center gap-3">
                        <div>
                          <h3 className="h6 fw-bold mb-1">{statement.file_name}</h3>
                          <p className="mb-0 text-secondary">{statement.file_type.toUpperCase()} · {statement.upload_status}</p>
                        </div>
                        <span className="badge rounded-pill text-bg-light border text-secondary px-3 py-2">{statement.created_at}</span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="insight-card rounded-4 p-3">
                    <p className="mb-0 text-secondary">No uploads yet. Your history will appear here after the first import.</p>
                  </div>
                )}
              </div>
            </section>
          </div>
        </div>
      </section>
    </main>
  );
}
