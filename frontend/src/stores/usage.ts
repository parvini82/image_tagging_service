import { writable } from 'svelte/store';

interface UsageInfo {
  used: number;
  limit: number;
  remaining: number;
}

interface UsageState {
  info: UsageInfo | null;
  loading: boolean;
  error: string | null;
}

const initialState: UsageState = {
  info: null,
  loading: false,
  error: null,
};

function createUsageStore() {
  const { subscribe, set, update } = writable<UsageState>(initialState);

  return {
    subscribe,
    setInfo: (info: UsageInfo) => {
      update((state) => ({ ...state, info }));
    },
    setLoading: (loading: boolean) => {
      update((state) => ({ ...state, loading }));
    },
    setError: (error: string | null) => {
      update((state) => ({ ...state, error }));
    },
    incrementUsage: () => {
      update((state) => {
        if (!state.info) return state;
        return {
          ...state,
          info: {
            ...state.info,
            used: state.info.used + 1,
            remaining: state.info.remaining - 1,
          },
        };
      });
    },
    reset: () => {
      set(initialState);
    },
  };
}

export const usageStore = createUsageStore();
