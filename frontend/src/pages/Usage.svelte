<script lang="ts">
  import { onMount } from 'svelte';
  import { usageStore } from '../stores/usage';
  import { apiClient } from '../lib/api';
  import Sidebar from '../components/Sidebar.svelte';
  import UsageTable from '../components/UsageTable.svelte';

  onMount(async () => {
    usageStore.setLoading(true);
    try {
      const entries = await apiClient.getUsageHistory();
      usageStore.setEntries(entries);
    } catch (err) {
      usageStore.setError(err instanceof Error ? err.message : 'Failed to load usage history');
    } finally {
      usageStore.setLoading(false);
    }
  });
</script>

<div class="flex h-screen bg-slate-50">
  {/* Sidebar */}
  <Sidebar />

  {/* Main Content */}
  <div class="flex-1 overflow-auto">
    <div class="max-w-6xl mx-auto px-6 py-8">
      {/* Header */}
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-slate-900 mb-2">Usage History</h1>
        <p class="text-slate-600">View your recent API requests</p>
      </div>

      {/* Table */}
      <UsageTable />
    </div>
  </div>
</div>
