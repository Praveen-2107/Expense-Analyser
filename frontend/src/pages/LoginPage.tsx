import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { useAuth } from '../context/AuthContext';

export function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitting(true);
    setError('');

    try {
      await login({ email, password });
      navigate('/dashboard', { replace: true });
    } catch {
      setError('Invalid email or password');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div>
      <p className="text-uppercase text-primary fw-semibold small mb-2">Login</p>
      <h2 className="fw-bold mb-2">Welcome back</h2>
      <p className="text-secondary mb-4">Use your registered email and password to continue.</p>

      <form className="d-grid gap-3" onSubmit={handleSubmit}>
        <div>
          <label className="form-label">Email</label>
          <input className="form-control form-control-lg" type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
        </div>
        <div>
          <label className="form-label">Password</label>
          <input
            className="form-control form-control-lg"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>

        {error ? <div className="alert alert-danger mb-0">{error}</div> : null}

        <button className="btn btn-primary btn-lg" type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Signing in...' : 'Sign In'}
        </button>
      </form>

      <p className="mt-4 mb-0 text-secondary">
        New here? <Link to="/register">Create an account</Link>
      </p>
    </div>
  );
}
