import { NavLink, Outlet } from 'react-router-dom';

export function AuthLayout() {
  return (
    <main className="auth-shell min-vh-100 d-flex align-items-center justify-content-center px-3 py-5">
      <div className="auth-card shadow-lg rounded-4 overflow-hidden bg-white w-100">
        <div className="row g-0">
          <div className="col-lg-5 auth-hero p-4 p-md-5 text-white d-flex flex-column justify-content-between">
            <div>
              <p className="text-uppercase small fw-semibold mb-2 opacity-75">AI Expense Analyzer</p>
              <h1 className="display-6 fw-bold mb-3">Take control of every rupee.</h1>
              <p className="mb-0 opacity-75">
                Sign in to track spending, automate categorization, and unlock AI insights for your budget.
              </p>
            </div>
            <div className="d-flex gap-3 mt-4 flex-wrap">
              <NavLink className="btn btn-light fw-semibold" to="/login">
                Login
              </NavLink>
              <NavLink className="btn btn-outline-light fw-semibold" to="/register">
                Register
              </NavLink>
            </div>
          </div>
          <div className="col-lg-7 p-4 p-md-5">
            <Outlet />
          </div>
        </div>
      </div>
    </main>
  );
}
