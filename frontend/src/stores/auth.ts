import { writable } from 'svelte/store';
import type { User } from '../types/api';

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  error: string | null;
  loading: boolean;
}

const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  error: null,
  loading: false,
};

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>(initialState);

  return {
    subscribe,
    setUser: (user: User) => {
      update((state) => ({ ...state, user, isAuthenticated: true }));
    },
    setError: (error: string | null) => {
      update((state) => ({ ...state, error }));
    },
    setLoading: (loading: boolean) => {
      update((state) => ({ ...state, loading }));
    },
    authenticate: (user: User) => {
      set({
        isAuthenticated: true,
        user,
        error: null,
        loading: false,
      });
    },
    logout: () => {
      set(initialState);
    },
    restoreSession: (user: User) => {
      set({
        isAuthenticated: true,
        user,
        error: null,
        loading: false,
      });
    },
  };
}

export const authStore = createAuthStore();
