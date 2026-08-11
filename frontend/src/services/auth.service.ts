// src/services/auth.service.ts
import api from '../lib/api';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  const response = await api.post('/api/v1/auth/login', { email, password });
  return response.data as LoginResponse;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface RefreshTokenResponse {
  access_token: string;
  expires_in: number;
}

export async function refreshToken(refreshToken: string): Promise<RefreshTokenResponse> {
  const response = await api.post('/api/v1/auth/refresh', { refresh_token: refreshToken });
  return response.data as RefreshTokenResponse;
}
