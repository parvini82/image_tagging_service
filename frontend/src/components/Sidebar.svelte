<script lang="ts">
  import { location } from 'svelte-spa-router';
  import { authStore } from '../stores/auth';
  import { navigate } from 'svelte-spa-router';

  function handleLogout() {
    authStore.logout();
    navigate('/login');
  }

  function isActive(path: string): boolean {
    return $location === path || $location.startsWith(path + '/');
  }
</script>

<div class="w-64 bg-slate-800 text-white flex flex-col">
  {/* Logo */}
  <div class="px-6 py-8">
    <h2 class="text-xl font-bold">Tagging API</h2>
    <p class="text-slate-400 text-sm">Dashboard</p>
  </div>

  {/* Navigation */}
  <nav class="flex-1 px-4 space-y-2">
    <a
      href="#/dashboard"
      class="block px-4 py-3 rounded-lg transition {isActive('/dashboard')
        ? 'bg-slate-700 text-white'
        : 'text-slate-400 hover:bg-slate-700/50'}"
    >
      <span class="font-medium">Dashboard</span>
    </a>
    <a
      href="#/dashboard/tagger"
      class="block px-4 py-3 rounded-lg transition {isActive('/dashboard/tagger')
        ? 'bg-slate-700 text-white'
        : 'text-slate-400 hover:bg-slate-700/50'}"
    >
      <span class="font-medium">Tagger Playground</span>
    </a>
    <a
      href="#/dashboard/usage"
      class="block px-4 py-3 rounded-lg transition {isActive('/dashboard/usage')
        ? 'bg-slate-700 text-white'
        : 'text-slate-400 hover:bg-slate-700/50'}"
    >
      <span class="font-medium">Usage History</span>
    </a>
  </nav>

  {/* Logout */}
  <div class="px-4 py-4 border-t border-slate-700">
    <button
      on:click={handleLogout}
      class="w-full px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-sm font-medium transition"
    >
      Logout
    </button>
  </div>
</div>
