import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';

import { fetchCurrentUser, loginUser, registerUser } from '../services/authService';
import type { AuthUser, LoginPayload, RegisterPayload } from '../types/auth';

type AuthContextValue = {
  user: AuthUser | null;
  isLoading: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = window.localStorage.getItem('accessToken');
    if (!token) {
      setIsLoading(false);
      return;
    }

    fetchCurrentUser()
      .then(setUser)
      .catch(() => {
        window.localStorage.removeItem('accessToken');
        setUser(null);
      })
      .finally(() => setIsLoading(false));
  }, []);

  const login = async (payload: LoginPayload) => {
    const tokenResponse = await loginUser(payload);
    window.localStorage.setItem('accessToken', tokenResponse.access_token);
    const currentUser = await fetchCurrentUser();
    setUser(currentUser);
  };

  const register = async (payload: RegisterPayload) => {
    await registerUser(payload);
    await login({ email: payload.email, password: payload.password });
  };

  const logout = () => {
    window.localStorage.removeItem('accessToken');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout }}>{children}</AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
