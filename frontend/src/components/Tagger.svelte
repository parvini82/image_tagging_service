<script lang="ts">
  import { apiClient } from '../lib/api';
  import { isValidUrl, formatJson } from '../lib/utils';
  import type { TaggingResponse } from '../types/api';

  let imageUrl = '';
  let mode: 'fast' | 'reasoning' | 'advanced_reasoning' = 'fast';
  let loading = false;
  let error = '';
  let response: TaggingResponse | null = null;
  let showRawJson = true;

  async function handleSubmit() {
    error = '';
    response = null;

    if (!imageUrl.trim()) {
      error = 'Please enter an image URL.';
      return;
    }

    if (!isValidUrl(imageUrl)) {
      error = 'Please enter a valid URL.';
      return;
    }

    loading = true;

    try {
      const result = await apiClient.tagImage({
        image_url: imageUrl,
        mode,
      });
      response = result;
    } catch (err) {
      error = err instanceof Error ? err.message : 'Failed to tag image. Please try again.';
    } finally {
      loading = false;
    }
  }

  function handleKeyPress(e: KeyboardEvent) {
    if (e.key === 'Enter' && e.ctrlKey && !loading) {
      handleSubmit();
    }
  }
</script>

<div class="space-y-6">
  {/* Input Form */}
  <div class="bg-white rounded-lg shadow p-6">
    <form on:submit|preventDefault={handleSubmit} class="space-y-4">
      {/* Image URL */}
      <div>
        <label for="imageUrl" class="block text-sm font-medium text-slate-700 mb-2">
          Image URL
        </label>
        <input
          id="imageUrl"
          type="text"
          bind:value={imageUrl}
          on:keypress={handleKeyPress}
          placeholder="https://example.com/image.jpg"
          class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
          disabled={loading}
        />
      </div>

      {/* Mode Selection */}
      <div>
        <label for="mode" class="block text-sm font-medium text-slate-700 mb-2">
          Tagging Mode
        </label>
        <select
          id="mode"
          bind:value={mode}
          class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
          disabled={loading}
        >
          <option value="fast">Fast (Quick results)</option>
          <option value="reasoning">Reasoning (More accurate)</option>
          <option value="advanced_reasoning">Advanced Reasoning (Most accurate)</option>
        </select>
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
          <span>Processing...</span>
        {:else}
          <span>Run Tagger</span>
        {/if}
      </button>
    </form>
  </div>

  {/* Response */}
  {#if response}
    <div class="bg-white rounded-lg shadow p-6 fade-in">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-bold text-slate-900">Response</h2>
        <button
          on:click={() => (showRawJson = !showRawJson)}
          class="text-sm text-blue-600 hover:text-blue-700 font-medium"
        >
          {showRawJson ? 'View Formatted' : 'View Raw JSON'}
        </button>
      </div>

      {#if showRawJson}
        <div class="json-viewer">{formatJson(response)}</div>
      {:else}
        <div class="space-y-4">
          <div>
            <label class="text-sm font-medium text-slate-600 block mb-2">Image URL</label>
            <a
              href={response.image_url}
              target="_blank"
              rel="noopener noreferrer"
              class="text-blue-600 hover:text-blue-700 break-all"
            >
              {response.image_url}
            </a>
          </div>

          <div>
            <label class="text-sm font-medium text-slate-600 block mb-2">Tags</label>
            <div class="bg-slate-50 rounded-lg p-4">
              <pre class="text-sm text-slate-700 overflow-x-auto">{formatJson(response.tags)}</pre>
            </div>
          </div>
        </div>
      {/if}
    </div>
  {/if}
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

  .fade-in {
    animation: fadeIn 0.3s ease-in;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .json-viewer {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 12px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    line-height: 1.5;
    overflow-x: auto;
    white-space: pre-wrap;
    word-wrap: break-word;
  }
</style>
