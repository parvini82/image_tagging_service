<script lang="ts">
  import { navigate } from 'svelte-spa-router';
  import { authStore } from '../stores/auth';
  import { apiClient } from '../lib/api';
  import type { ApiKeyInfo } from '../types/api';

  let apiKey = '';
  let error = '';
  let loading = false;

  async function handleLogin() {
    if (!apiKey.trim()) {
      error = 'Please enter your API key.';
      return;
    }

    loading = true;
    error = '';

    try {
      const keyInfo: ApiKeyInfo = await apiClient.validateApiKey(apiKey);
      authStore.authenticate(apiKey, keyInfo);
      navigate('/dashboard');
    } catch (err) {
      error = err instanceof Error ? err.message : 'Authentication failed. Please try again.';
    } finally {
      loading = false;
    }
  }

  function handleKeyPress(e: KeyboardEvent) {
    if (e.key === 'Enter' && !loading) {
      handleLogin();
    }
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
  <div class="w-full max-w-md">
    <div class="bg-white rounded-lg shadow-2xl p-8">
      {/* Header */}
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">Image Tagging API</h1>
        <p class="text-slate-600">Dashboard</p>
      </div>

      {/* Form */}
      <form on:submit|preventDefault={handleLogin} class="space-y-6">
        {/* API Key Input */}
        <div>
          <label for="apiKey" class="block text-sm font-medium text-slate-700 mb-2">
            API Key
          </label>
          <input
            id="apiKey"
            type="password"
            bind:value={apiKey}
            on:keypress={handleKeyPress}
            placeholder="Enter your API key"
            class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            disabled={loading}
          />
        </div>

        {/* Error Message */}
        {#if error}
          <div class="bg-red-50 border border-red-200 rounded-lg p-4">
            <p class="text-red-800 text-sm font-medium">{error}</p>
          </div>
        {/if}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 text-white font-medium py-2 px-4 rounded-lg transition duration-200 flex items-center justify-center gap-2"
        >
          {#if loading}
            <div class="spinner"></div>
            <span>Authenticating...</span>
          {:else}
            <span>Enter Dashboard</span>
          {/if}
        </button>
      </form>

      {/* Footer */}
      <p class="text-center text-slate-500 text-xs mt-8">
        This dashboard is for API key owners only.
      </p>
    </div>
  </div>
</div>

<style>
  .spinner {
    border: 2px solid #e2e8f0;
    border-top: 2px solid white;
    border-radius: 50%;
    width: 16px;
    height: 16px;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>
