<script lang="ts">
  import { authStore } from '../stores/auth';
  import { formatDate } from '../lib/utils';

  let showKey = false;

  function toggleKeyVisibility() {
    showKey = !showKey;
  }
</script>

<div class="bg-white rounded-lg shadow p-6">
  <h2 class="text-xl font-bold text-slate-900 mb-6">API Key Information</h2>

  {#if $authStore.keyInfo}
    <div class="space-y-4">
      <div>
        <label class="text-sm font-medium text-slate-600 block mb-2">API Key</label>
        <div class="flex gap-2 items-center">
          <code class="flex-1 bg-slate-100 px-3 py-2 rounded text-sm font-mono text-slate-900">
            {showKey ? $authStore.apiKey : $authStore.keyInfo.maskedKey}
          </code>
          <button
            on:click={toggleKeyVisibility}
            class="px-3 py-2 text-slate-600 hover:bg-slate-100 rounded transition"
          >
            {showKey ? 'Hide' : 'Show'}
          </button>
        </div>
      </div>

      <div>
        <label class="text-sm font-medium text-slate-600 block mb-2">Weekly Quota</label>
        <p class="text-lg font-semibold text-slate-900">{$authStore.keyInfo.weeklyQuota} requests</p>
      </div>

      <div>
        <label class="text-sm font-medium text-slate-600 block mb-2">Remaining Quota</label>
        <p class="text-lg font-semibold text-slate-900">{$authStore.keyInfo.remainingQuota} requests</p>
      </div>

      <div>
        <label class="text-sm font-medium text-slate-600 block mb-2">Last Used</label>
        <p class="text-slate-700">{formatDate($authStore.keyInfo.lastUsedAt)}</p>
      </div>

      <div>
        <label class="text-sm font-medium text-slate-600 block mb-2">Quota Reset At</label>
        <p class="text-slate-700">{formatDate($authStore.keyInfo.quotaResetAt)}</p>
      </div>
    </div>
  {/if}
</div>
