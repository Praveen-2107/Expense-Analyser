import api from './api';
import type { AuthUser, LoginPayload, RegisterPayload, TokenResponse } from '../types/auth';

type UserResponse = {
  id: number;
  full_name: string;
  email: string;
  is_active: boolean;
};

function mapUser(response: UserResponse): AuthUser {
  return {
    id: response.id,
    fullName: response.full_name,
    email: response.email,
    isActive: response.is_active
  };
}

export async function registerUser(payload: RegisterPayload): Promise<AuthUser> {
  const response = await api.post<UserResponse>('/auth/register', {
    full_name: payload.fullName,
    email: payload.email,
    password: payload.password
  });
  return mapUser(response.data);
}

export async function loginUser(payload: LoginPayload): Promise<TokenResponse> {
  const formData = new URLSearchParams();
  formData.append('username', payload.email);
  formData.append('password', payload.password);
  const response = await api.post<TokenResponse>('/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });
  return response.data;
}

export async function fetchCurrentUser(): Promise<AuthUser> {
  const response = await api.get<UserResponse>('/auth/me');
  return mapUser(response.data);
}
