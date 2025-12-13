<script lang="ts">
  import { onMount } from 'svelte';
  import { push } from 'svelte-spa-router';
  import { authStore } from '../stores/auth';
  import { apiKeysStore } from '../stores/apiKeys';
  import { apiClient } from '../lib/api';
  import Sidebar from '../components/Sidebar.svelte';
  import APIKeyCard from '../components/APIKeyCard.svelte';

  let loadingKeys = false;
  let errorMessage = '';
  let showNewKeyModal = false;
  let newKeyData: { key: string; masked_key: string } | null = null;
  let copiedToClipboard = false;

  onMount(async () => {
    await loadAPIKeys();
  });

  async function loadAPIKeys() {
    loadingKeys = true;
    errorMessage = '';
    try {
      const keys = await apiClient.listAPIKeys();
      apiKeysStore.setKeys(keys);
    } catch (err) {
      errorMessage = err instanceof Error ? err.message : 'Failed to load API keys';
    } finally {
      loadingKeys = false;
    }
  }

  async function generateNewKey() {
    try {
      const response = await apiClient.generateAPIKey();
      newKeyData = {
        key: response.key,
        masked_key: response.masked_key,
      };
      showNewKeyModal = true;
      await loadAPIKeys();
    } catch (err) {
      errorMessage = err instanceof Error ? err.message : 'Failed to generate API key';
    }
  }

  async function revokeKey(keyId: number) {
    if (!confirm('Are you sure you want to revoke this API key? This action cannot be undone.')) {
      return;
    }
    try {
      await apiClient.revokeAPIKey(keyId);
      apiKeysStore.removeKey(keyId);
    } catch (err) {
      errorMessage = err instanceof Error ? err.message : 'Failed to revoke API key';
    }
  }

  function copyToClipboard(text: string) {
    navigator.clipboard.writeText(text);
    copiedToClipboard = true;
    setTimeout(() => {
      copiedToClipboard = false;
    }, 2000);
  }

  function closeModal() {
    showNewKeyModal = false;
    newKeyData = null;
  }
</script>

<div class="flex h-screen bg-slate-50">
  <Sidebar />

  <main class="flex-1 overflow-auto">
    <div class="p-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">Dashboard</h1>
        <p class="text-slate-600">Manage your API keys and usage</p>
      </div>

      {#if errorMessage}
        <div class="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
          <p class="text-red-800 font-medium">{errorMessage}</p>
        </div>
      {/if}

      <div class="grid grid-cols-1 gap-6">
        <section class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h2 class="text-xl font-semibold text-slate-900">API Keys</h2>
              <p class="text-slate-600 text-sm mt-1">Manage your API keys for the image tagging service</p>
            </div>
            <button
              on:click={generateNewKey}
              disabled={loadingKeys}
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 text-white rounded-lg font-medium transition"
            >
              {#if loadingKeys}
                <span>Loading...</span>
              {:else}
                <span>Generate API Key</span>
              {/if}
            </button>
          </div>

          {#if newKeyData && showNewKeyModal}
            <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
              <div class="bg-white rounded-lg shadow-2xl max-w-md w-full p-6">
                <h3 class="text-lg font-semibold text-slate-900 mb-4">API Key Created</h3>
                <div class="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-4">
                  <p class="text-amber-800 text-sm font-medium mb-2">⚠️ Save your API key now</p>
                  <p class="text-amber-700 text-sm">You won't be able to see it again. Copy it and keep it safe.</p>
                </div>

                <div class="bg-slate-100 rounded-lg p-3 mb-4 font-mono text-sm break-all">
                  {newKeyData.key}
                </div>

                <button
                  on:click={() => copyToClipboard(newKeyData.key)}
                  class="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition mb-2"
                >
                  {copiedToClipboard ? '✓ Copied!' : 'Copy API Key'}
                </button>

                <button
                  on:click={closeModal}
                  class="w-full px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-900 rounded-lg font-medium transition"
                >
                  Done
                </button>
              </div>
            </div>
          {/if}

          {#if loadingKeys}
            <div class="flex items-center justify-center py-12">
              <div class="text-slate-600">Loading API keys...</div>
            </div>
          {:else}
            <div class="space-y-3">
              {#if $apiKeysStore.keys.length === 0}
                <div class="text-center py-12">
                  <p class="text-slate-600 mb-4">No API keys yet</p>
                  <p class="text-slate-500 text-sm">Generate your first API key to start using the image tagging service</p>
                </div>
              {:else}
                {#each $apiKeysStore.keys as key (key.id)}
                  <APIKeyCard
                    {key}
                    onRevoke={() => revokeKey(key.id)}
                    onCopy={() => copyToClipboard(key.masked_key)}
                  />
                {/each}
              {/if}
            </div>
          {/if}
        </section>

        <section class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold text-slate-900 mb-6">Usage Information</h2>
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-slate-50 rounded-lg p-4">
              <p class="text-slate-600 text-sm mb-1">Weekly Quota</p>
              <p class="text-2xl font-bold text-slate-900">Unlimited</p>
              <p class="text-slate-500 text-xs mt-2">Rate limited</p>
            </div>
            <div class="bg-slate-50 rounded-lg p-4">
              <p class="text-slate-600 text-sm mb-1">Account Status</p>
              <p class="text-2xl font-bold text-green-600">Active</p>
              <p class="text-slate-500 text-xs mt-2">Ready to use</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  </main>
</div>
