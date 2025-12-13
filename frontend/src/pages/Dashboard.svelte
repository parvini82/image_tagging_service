<script lang="ts">
  import { authStore } from '../stores/auth';
  import Sidebar from '../components/Sidebar.svelte';
  import ApiKeyInfo from '../components/ApiKeyInfo.svelte';
  import UsageStats from '../components/UsageStats.svelte';
</script>

<div class="flex h-screen bg-slate-50">
  {/* Sidebar */}
  <Sidebar />

  {/* Main Content */}
  <div class="flex-1 overflow-auto">
    <div class="max-w-6xl mx-auto px-6 py-8">
      {/* Header */}
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-slate-900 mb-2">Dashboard</h1>
        <p class="text-slate-600">Manage your API key and monitor usage</p>
      </div>

      {/* Cards Grid */}
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* API Key Card */}
        <ApiKeyInfo />

        {/* Usage Stats Card */}
        <UsageStats />
      </div>
    </div>
  </div>
</div>
