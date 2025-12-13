import { writable } from 'svelte/store';
import type { ApiKeyInfo } from '../types/api';

interface AuthState {
  isAuthenticated: boolean;
  apiKey: string | null;
  keyInfo: ApiKeyInfo | null;
  error: string | null;
  loading: boolean;
}

const initialState: AuthState = {
  isAuthenticated: false,
  apiKey: null,
  keyInfo: null,
  error: null,
  loading: false,
};

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>(initialState);

  return {
    subscribe,
    setApiKey: (key: string) => {
      update((state) => ({ ...state, apiKey: key }));
    },
    setKeyInfo: (info: ApiKeyInfo) => {
      update((state) => ({ ...state, keyInfo: info }));
    },
    setError: (error: string | null) => {
      update((state) => ({ ...state, error }));
    },
    setLoading: (loading: boolean) => {
      update((state) => ({ ...state, loading }));
    },
    authenticate: (key: string, info: ApiKeyInfo) => {
      localStorage.setItem('apiKey', key);
      set({
        isAuthenticated: true,
        apiKey: key,
        keyInfo: info,
        error: null,
        loading: false,
      });
    },
    logout: () => {
      localStorage.removeItem('apiKey');
      set(initialState);
    },
    restoreSession: () => {
      const storedKey = localStorage.getItem('apiKey');
      if (storedKey) {
        update((state) => ({
          ...state,
          apiKey: storedKey,
          isAuthenticated: true,
        }));
      }
    },
  };
}

export const authStore = createAuthStore();
