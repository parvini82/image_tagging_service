<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore } from '../stores/auth';
  import { usageStore } from '../stores/usage';
  import { apiKeysStore } from '../stores/apiKeys';
  import { apiClient } from '../lib/api';
  import Sidebar from '../components/Sidebar.svelte';
  import APIKeyCard from '../components/APIKeyCard.svelte';

  let loadingKeys = false;
  let loadingUsage = false;
  let loadingTag = false;
  let errorMessage = '';
  let successMessage = '';
  
  let showNewKeyModal = false;
  let newKeyData: { key: string; masked_key: string } | null = null;
  let copiedToClipboard = false;

  let imageUrl = '';
  let tagResult: any = null;
  let tagError = '';

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

  onMount(async () => {
    await loadAPIKeys();
    await loadUsageInfo();
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

  async function loadUsageInfo() {
    loadingUsage = true;
    try {
      const info = await apiClient.getUsageInfo();
      usageStore.setInfo(info);
    } catch (err) {
      console.error('Failed to load usage info:', err);
    } finally {
      loadingUsage = false;
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
      successMessage = 'API key generated successfully!';
      setTimeout(() => { successMessage = ''; }, 3000);
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
      successMessage = 'API key revoked successfully!';
      setTimeout(() => { successMessage = ''; }, 3000);
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

  async function handleTag() {
    if (!imageUrl.trim()) {
      tagError = 'Please enter an image URL';
      return;
    }

    if ($usageStore.info && $usageStore.info.remaining <= 0) {
      tagError = 'Daily limit reached. Come back tomorrow!';
      return;
    }

    loadingTag = true;
    tagError = '';
    tagResult = null;

    try {
      const result = await apiClient.tagImageWithSession({
        image_url: imageUrl,
      });
      tagResult = result;
      usageStore.incrementUsage();
      successMessage = 'Tags generated successfully!';
      setTimeout(() => { successMessage = ''; }, 3000);
    } catch (err) {
      tagError = err instanceof Error ? err.message : 'Failed to generate tags';
    } finally {
      loadingTag = false;
    }
  }

  function handleKeyPress(e: KeyboardEvent) {
    if (e.key === 'Enter' && !loadingTag) {
      handleTag();
    }
  }

  function getProgressPercentage(): number {
    if (!$usageStore.info) return 0;
    return Math.round(($usageStore.info.used / $usageStore.info.limit) * 100);
  }

  function getProgressColor(): string {
    const percentage = getProgressPercentage();
    if (percentage < 50) return 'bg-green-500';
    if (percentage < 80) return 'bg-yellow-500';
    return 'bg-red-500';
  }
</script>

<div class="flex h-screen bg-slate-50">
  <Sidebar />

  <main class="flex-1 overflow-auto">
    <div class="p-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">Dashboard</h1>
        <p class="text-slate-600">Manage your API keys, test tagging, and monitor usage</p>
      </div>

      {#if errorMessage}
        <div class="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
          <p class="text-red-800 font-medium">{errorMessage}</p>
        </div>
      {/if}

      {#if successMessage}
        <div class="mb-6 bg-green-50 border border-green-200 rounded-lg p-4">
          <p class="text-green-800 font-medium">{successMessage}</p>
        </div>
      {/if}

      <div class="grid grid-cols-1 gap-6">
        <!-- 1. API Key Section -->
        <section class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h2 class="text-xl font-semibold text-slate-900">🔑 API Keys</h2>
              <p class="text-slate-600 text-sm mt-1">Generate and manage API keys for external API usage</p>
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
                  <p class="text-slate-500 text-sm">Generate your first API key to start using the external API</p>
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

        <!-- 2. Tagging Playground Section -->
        <section class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold text-slate-900 mb-6">🧪 Tagging Playground</h2>
          <div class="space-y-4">
            <div>
              <label for="imageUrl" class="block text-sm font-medium text-slate-700 mb-2">
                Image URL
              </label>
              <input
                id="imageUrl"
                type="url"
                bind:value={imageUrl}
                on:keypress={handleKeyPress}
                placeholder="https://example.com/image.jpg"
                class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                disabled={loadingTag}
              />
            </div>

            {#if tagError}
              <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                <p class="text-red-800 text-sm font-medium">{tagError}</p>
              </div>
            {/if}

            <button
              on:click={handleTag}
              disabled={loadingTag || ($usageStore.info && $usageStore.info.remaining <= 0)}
              class="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 text-white rounded-lg font-medium transition"
            >
              {#if loadingTag}
                <span>Generating tags...</span>
              {:else if $usageStore.info && $usageStore.info.remaining <= 0}
                <span>Daily limit reached</span>
              {:else}
                <span>Generate Tags</span>
              {/if}
            </button>

            {#if tagResult}
              <div class="mt-6">
                <h3 class="text-sm font-semibold text-slate-900 mb-3">Raw JSON Response:</h3>
                <div class="bg-slate-100 rounded-lg p-4 overflow-auto max-h-96 font-mono text-xs">
                  <pre>{JSON.stringify(tagResult, null, 2)}</pre>
                </div>
              </div>
            {/if}
          </div>
        </section>

        <!-- 3. Usage Section -->
        <section class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold text-slate-900 mb-6">📊 Daily Usage</h2>
          {#if loadingUsage}
            <div class="flex items-center justify-center py-12">
              <div class="text-slate-600">Loading usage info...</div>
            </div>
          {:else if $usageStore.info}
            <div class="space-y-4">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-slate-700">Daily Limit</span>
                  <span class="text-sm font-semibold text-slate-900">
                    {$usageStore.info.used} / {$usageStore.info.limit}
                  </span>
                </div>
                <div class="w-full bg-slate-200 rounded-full h-3">
                  <div
                    class="h-3 rounded-full transition-all {getProgressColor()}"
                    style="width: {getProgressPercentage()}%"
                  />
                </div>
              </div>
              <div class="grid grid-cols-3 gap-4 mt-6">
                <div class="bg-slate-50 rounded-lg p-4 text-center">
                  <p class="text-slate-600 text-xs mb-1">Used Today</p>
                  <p class="text-2xl font-bold text-slate-900">{$usageStore.info.used}</p>
                </div>
                <div class="bg-slate-50 rounded-lg p-4 text-center">
                  <p class="text-slate-600 text-xs mb-1">Remaining</p>
                  <p class="text-2xl font-bold text-blue-600">{$usageStore.info.remaining}</p>
                </div>
                <div class="bg-slate-50 rounded-lg p-4 text-center">
                  <p class="text-slate-600 text-xs mb-1">Daily Limit</p>
                  <p class="text-2xl font-bold text-slate-900">{$usageStore.info.limit}</p>
                </div>
              </div>
              <p class="text-xs text-slate-500 mt-4">⏰ Limit resets at midnight UTC</p>
            </div>
          {/if}
        </section>

        <!-- 4. API Documentation Section -->
        <section class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold text-slate-900 mb-6">📘 API Documentation</h2>
          <div class="space-y-6">
            <div>
              <h3 class="text-sm font-semibold text-slate-900 mb-2">Endpoint</h3>
              <div class="bg-slate-100 rounded-lg p-3 font-mono text-sm text-slate-800 overflow-auto">
                POST {API_BASE_URL}/api/v1/tag/
              </div>
            </div>

            <div>
              <h3 class="text-sm font-semibold text-slate-900 mb-2">Headers</h3>
              <div class="bg-slate-100 rounded-lg p-3 font-mono text-sm text-slate-800 overflow-auto space-y-1">
                <div>Authorization: Api-Key &lt;your-api-key&gt;</div>
                <div>Content-Type: application/json</div>
              </div>
            </div>

            <div>
              <h3 class="text-sm font-semibold text-slate-900 mb-2">Request Body</h3>
              <div class="bg-slate-100 rounded-lg p-3 font-mono text-sm text-slate-800 overflow-auto">
                <pre>{`{"image_url": "https://example.com/image.jpg"}`}</pre>
              </div>
            </div>

            <div>
              <h3 class="text-sm font-semibold text-slate-900 mb-2">Sample cURL Request</h3>
              <div class="bg-slate-100 rounded-lg p-3 font-mono text-xs text-slate-800 overflow-auto">
                <pre>{`curl -X POST ${API_BASE_URL}/api/v1/tag/ \\
  -H "Authorization: Api-Key your-api-key" \\
  -H "Content-Type: application/json" \\
  -d '{"image_url": "https://example.com/image.jpg"}'`}</pre>
              </div>
            </div>

            <div>
              <h3 class="text-sm font-semibold text-slate-900 mb-2">Response</h3>
              <div class="bg-slate-100 rounded-lg p-3 font-mono text-sm text-slate-800 overflow-auto">
                <pre>{`{"image_url": "...", "tags": {...}}`}</pre>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </main>
</div>
