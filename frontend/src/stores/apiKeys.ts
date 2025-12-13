import { writable } from 'svelte/store';
import type { APIKey } from '../types/api';

interface APIKeysState {
  keys: APIKey[];
  loading: boolean;
  error: string | null;
  selectedKeyId: number | null;
}

const initialState: APIKeysState = {
  keys: [],
  loading: false,
  error: null,
  selectedKeyId: null,
};

function createAPIKeysStore() {
  const { subscribe, set, update } = writable<APIKeysState>(initialState);

  return {
    subscribe,
    setKeys: (keys: APIKey[]) => {
      update((state) => ({ ...state, keys }));
    },
    addKey: (key: APIKey) => {
      update((state) => ({ ...state, keys: [key, ...state.keys] }));
    },
    removeKey: (keyId: number) => {
      update((state) => ({
        ...state,
        keys: state.keys.filter((k) => k.id !== keyId),
      }));
    },
    setLoading: (loading: boolean) => {
      update((state) => ({ ...state, loading }));
    },
    setError: (error: string | null) => {
      update((state) => ({ ...state, error }));
    },
    reset: () => {
      set(initialState);
    },
  };
}

export const apiKeysStore = createAPIKeysStore();
