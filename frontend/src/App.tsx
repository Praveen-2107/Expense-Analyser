import { Navigate, Route, Routes } from 'react-router-dom';

import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AuthLayout } from './layouts/AuthLayout';
import { DashboardRedirect } from './pages/DashboardRedirect';
import { LoginPage } from './pages/LoginPage';
import { UploadPage } from './pages/UploadPage';
import { RegisterPage } from './pages/RegisterPage';

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Route>
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardRedirect />
            </ProtectedRoute>
          }
        />
        <Route
          path="/uploads"
          element={
            <ProtectedRoute>
              <UploadPage />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;

