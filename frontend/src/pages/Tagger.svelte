<script lang="ts">
  import { authStore } from '../stores/auth';
  import { apiClient } from '../lib/api';
  import Sidebar from '../components/Sidebar.svelte';
  import type { TaggingResponse } from '../types/api';

  let imageUrl = '';
  let mode: 'fast' | 'reasoning' | 'advanced_reasoning' = 'fast';
  let loading = false;
  let error = '';
  let result: TaggingResponse | null = null;

  async function handleTag() {
    if (!imageUrl.trim()) {
      error = 'Please enter an image URL';
      return;
    }

    loading = true;
    error = '';
    result = null;

    try {
      result = await apiClient.tagImage({
        image_url: imageUrl,
        mode,
      });
    } catch (err) {
      error = err instanceof Error ? err.message : 'Failed to tag image';
    } finally {
      loading = false;
    }
  }

  function handleKeyPress(e: KeyboardEvent) {
    if (e.key === 'Enter' && !loading) {
      handleTag();
    }
  }
</script>

<div class="flex h-screen bg-slate-50">
  <Sidebar />

  <main class="flex-1 overflow-auto">
    <div class="p-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">Image Tagger</h1>
        <p class="text-slate-600">Test the image tagging service</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold text-slate-900 mb-4">Tag Image</h2>

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
                disabled={loading}
              />
            </div>

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
                <option value="fast">Fast</option>
                <option value="reasoning">Reasoning</option>
                <option value="advanced_reasoning">Advanced Reasoning</option>
              </select>
            </div>

            {#if error}
              <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                <p class="text-red-800 text-sm font-medium">{error}</p>
              </div>
            {/if}

            <button
              on:click={handleTag}
              disabled={loading}
              class="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 text-white rounded-lg font-medium transition"
            >
              {#if loading}
                <span>Tagging...</span>
              {:else}
                <span>Tag Image</span>
              {/if}
            </button>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold text-slate-900 mb-4">Preview</h2>

          {#if imageUrl}
            <div class="mb-4 rounded-lg overflow-hidden bg-slate-100 aspect-square flex items-center justify-center">
              <img
                src={imageUrl}
                alt="Preview"
                class="w-full h-full object-cover"
                on:error={() => (error = 'Failed to load image')}
              />
            </div>
          {:else}
            <div class="mb-4 rounded-lg bg-slate-100 aspect-square flex items-center justify-center">
              <p class="text-slate-500 text-center">
                <span class="text-4xl mb-2 block">🖼</span>
                Enter an image URL to preview
              </p>
            </div>
          {/if}
        </div>
      </div>

      {#if result}
        <div class="mt-6 bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold text-slate-900 mb-4">Results</h2>
          <pre class="bg-slate-100 rounded-lg p-4 overflow-auto">{JSON.stringify(result, null, 2)}</pre>
        </div>
      {/if}
    </div>
  </main>
</div>
