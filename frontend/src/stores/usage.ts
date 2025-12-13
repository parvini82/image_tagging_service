import { writable } from 'svelte/store';
import type { UsageEntry } from '../types/api';

interface UsageState {
  entries: UsageEntry[];
  loading: boolean;
  error: string | null;
}

const initialState: UsageState = {
  entries: [],
  loading: false,
  error: null,
};

function createUsageStore() {
  const { subscribe, set, update } = writable<UsageState>(initialState);

  return {
    subscribe,
    setEntries: (entries: UsageEntry[]) => {
      update((state) => ({ ...state, entries }));
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

export const usageStore = createUsageStore();
