<script lang="ts">
  import { authStore } from '../stores/auth';
  import Sidebar from '../components/Sidebar.svelte';
  import ApiKeyInfo from '../components/ApiKeyInfo.svelte';
  import UsageStats from '../components/UsageStats.svelte';
</script>

<div class="flex h-screen bg-slate-50">
  <Sidebar />

  <div class="flex-1 overflow-auto">
    <div class="max-w-6xl mx-auto px-6 py-8">
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-slate-900 mb-2">Dashboard</h1>
        <p class="text-slate-600">Manage your API key and monitor usage</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ApiKeyInfo />
        <UsageStats />
      </div>
    </div>
  </div>
</div>
