<script lang="ts">
  import type { APIKey } from '../types/api';

  export let key: APIKey;
  export let onRevoke: () => void;
  export let onCopy: () => void;

  function formatDate(dateString: string | null): string {
    if (!dateString) return 'Never';
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  }
</script>

<div class="border border-slate-200 rounded-lg p-4 hover:border-slate-300 transition">
  <div class="flex items-center justify-between mb-3">
    <div class="flex-1">
      <div class="flex items-center gap-2 mb-2">
        <code class="bg-slate-100 px-3 py-1 rounded font-mono text-sm text-slate-900">
          {key.masked_key}
        </code>
        <button
          on:click={onCopy}
          title="Copy masked key"
          class="text-slate-500 hover:text-slate-700 transition p-1"
        >
          📋
        </button>
      </div>
      <div class="flex gap-4 text-sm text-slate-500">
        <span>Created: {formatDate(key.created_at)}</span>
        <span>Last used: {formatDate(key.last_used_at)}</span>
      </div>
    </div>
    <button
      on:click={onRevoke}
      class="px-3 py-1 bg-red-50 hover:bg-red-100 text-red-700 rounded text-sm font-medium transition"
    >
      Revoke
    </button>
  </div>
</div>
