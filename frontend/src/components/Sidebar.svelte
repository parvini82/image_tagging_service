<script lang="ts">
  import { location, push } from 'svelte-spa-router';
  import { authStore } from '../stores/auth';
  import { apiKeysStore } from '../stores/apiKeys';
  import { apiClient } from '../lib/api';

  let loggingOut = false;

  async function handleLogout() {
    loggingOut = true;
    try {
      await apiClient.logout();
      authStore.logout();
      apiKeysStore.reset();
      push('/login');
    } catch (err) {
      console.error('Logout failed:', err);
    } finally {
      loggingOut = false;
    }
  }

  function isActive(path: string): boolean {
    return $location === path || $location.startsWith(path + '/');
  }
</script>

<div class="w-64 bg-slate-800 text-white flex flex-col">
  <div class="px-6 py-8 border-b border-slate-700">
    <h2 class="text-xl font-bold">🔖 Tagging API</h2>
    <p class="text-slate-400 text-sm mt-1">{$authStore.user?.email || 'User'}</p>
  </div>

  <nav class="flex-1 px-4 py-6 space-y-2">
    <a
      href="#/dashboard"
      class="block px-4 py-3 rounded-lg transition {isActive('/dashboard')
        ? 'bg-slate-700 text-white'
        : 'text-slate-300 hover:bg-slate-700/50'}"
    >
      <span class="font-medium">📊 Dashboard</span>
    </a>
    <a
      href="#/dashboard/tagger"
      class="block px-4 py-3 rounded-lg transition {isActive('/dashboard/tagger')
        ? 'bg-slate-700 text-white'
        : 'text-slate-300 hover:bg-slate-700/50'}"
    >
      <span class="font-medium">🏷️ Tagger Playground</span>
    </a>
    <a
      href="#/dashboard/usage"
      class="block px-4 py-3 rounded-lg transition {isActive('/dashboard/usage')
        ? 'bg-slate-700 text-white'
        : 'text-slate-300 hover:bg-slate-700/50'}"
    >
      <span class="font-medium">📈 Usage History</span>
    </a>
    <a
      href="#/dashboard/docs"
      class="block px-4 py-3 rounded-lg transition {isActive('/dashboard/docs')
        ? 'bg-slate-700 text-white'
        : 'text-slate-300 hover:bg-slate-700/50'}"
    >
      <span class="font-medium">📚 API Documentation</span>
    </a>
  </nav>

  <div class="px-4 py-4 border-t border-slate-700 space-y-2">
    <button
      on:click={handleLogout}
      disabled={loggingOut}
      class="w-full px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-slate-600 text-white rounded-lg text-sm font-medium transition"
    >
      {loggingOut ? 'Logging out...' : '🚪 Logout'}
    </button>
  </div>
</div>
