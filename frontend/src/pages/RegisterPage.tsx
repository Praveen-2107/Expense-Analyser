import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { useAuth } from '../context/AuthContext';

export function RegisterPage() {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitting(true);
    setError('');

    try {
      await register({ fullName, email, password });
      navigate('/dashboard', { replace: true });
    } catch {
      setError('Registration failed. Email may already be in use.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div>
      <p className="text-uppercase text-primary fw-semibold small mb-2">Register</p>
      <h2 className="fw-bold mb-2">Create your account</h2>
      <p className="text-secondary mb-4">Add your profile details to start tracking finances.</p>

      <form className="d-grid gap-3" onSubmit={handleSubmit}>
        <div>
          <label className="form-label">Full Name</label>
          <input className="form-control form-control-lg" type="text" value={fullName} onChange={(event) => setFullName(event.target.value)} />
        </div>
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
          {isSubmitting ? 'Creating account...' : 'Create Account'}
        </button>
      </form>

      <p className="mt-4 mb-0 text-secondary">
        Already have an account? <Link to="/login">Sign in</Link>
      </p>
    </div>
  );
}
