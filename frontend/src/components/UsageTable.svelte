<script lang="ts">
  import { usageStore } from '../stores/usage';
  import { formatDate } from '../lib/utils';

  let itemsPerPage = 10;
  let currentPage = 1;

  $: filteredEntries = $usageStore.entries;
  $: totalPages = Math.ceil(filteredEntries.length / itemsPerPage);
  $: paginatedEntries = filteredEntries.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );
</script>

<div class="bg-white rounded-lg shadow overflow-hidden">
  {#if $usageStore.loading}
    <div class="p-8 text-center">
      <div class="inline-block spinner"></div>
      <p class="text-slate-600 mt-4">Loading usage history...</p>
    </div>
  {:else if $usageStore.error}
    <div class="p-8">
      <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p class="text-yellow-800 text-sm font-medium">
          Note: This is a mock implementation. The actual usage history endpoint is not yet implemented in the backend.
        </p>
      </div>
    </div>
  {:else if paginatedEntries.length === 0}
    <div class="p-8 text-center">
      <p class="text-slate-500">No usage history available.</p>
    </div>
  {:else}
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="bg-slate-50 border-b border-slate-200">
          <tr>
            <th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Timestamp</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Endpoint</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200">
          {#each paginatedEntries as entry (entry.timestamp)}
            <tr class="hover:bg-slate-50 transition">
              <td class="px-6 py-4 text-sm text-slate-700">{formatDate(entry.timestamp)}</td>
              <td class="px-6 py-4 text-sm text-slate-700 font-mono">{entry.endpoint}</td>
              <td class="px-6 py-4 text-sm">
                {#if entry.success}
                  <span class="inline-block bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-medium">
                    {entry.status}
                  </span>
                {:else}
                  <span class="inline-block bg-red-100 text-red-800 px-2 py-1 rounded text-xs font-medium">
                    {entry.status}
                  </span>
                {/if}
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    {#if totalPages > 1}
      <div class="px-6 py-4 border-t border-slate-200 flex items-center justify-between">
        <button
          on:click={() => (currentPage = Math.max(1, currentPage - 1))}
          disabled={currentPage === 1}
          class="px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 rounded disabled:opacity-50 transition"
        >
          Previous
        </button>
        <span class="text-sm text-slate-600">
          Page {currentPage} of {totalPages}
        </span>
        <button
          on:click={() => (currentPage = Math.min(totalPages, currentPage + 1))}
          disabled={currentPage === totalPages}
          class="px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 rounded disabled:opacity-50 transition"
        >
          Next
        </button>
      </div>
    {/if}
  {/if}
</div>

<style>
  .spinner {
    border: 2px solid #e2e8f0;
    border-top: 2px solid #334155;
    border-radius: 50%;
    width: 20px;
    height: 20px;
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
