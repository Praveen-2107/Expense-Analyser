import { useAuth } from '../context/AuthContext';

export function DashboardRedirect() {
  const { user, logout } = useAuth();

  return (
    <main className="min-vh-100 d-flex align-items-center justify-content-center bg-light p-4">
      <section className="bg-white rounded-4 shadow p-4 p-md-5 w-100" style={{ maxWidth: '720px' }}>
        <p className="text-uppercase text-primary fw-semibold small mb-2">Dashboard placeholder</p>
        <h1 className="fw-bold mb-3">Hello, {user?.fullName}</h1>
        <p className="text-secondary mb-4">Authentication is working. The finance dashboard comes in the next module.</p>
        <button className="btn btn-outline-primary" type="button" onClick={logout}>
          Logout
        </button>
      </section>
    </main>
  );
}
