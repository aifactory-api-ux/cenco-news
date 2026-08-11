// src/stores/auth.store.ts
import create from 'zustand';

interface AuthState {
  token: string | null;
  userRole: string | null;
  setToken: (token: string, role: string) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  userRole: localStorage.getItem('role'),
  setToken: (token, role) => {
    localStorage.setItem('token', token);
    localStorage.setItem('role', role);
    set({ token, userRole: role });
  },
  clearAuth: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    set({ token: null, userRole: null });
  },
}));
