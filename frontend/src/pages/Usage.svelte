<script lang="ts">
  import Sidebar from '../components/Sidebar.svelte';
  import type { APIKey } from '../types/api';

  let usageData: Array<{
    date: string;
    requests: number;
    timestamp: string;
  }> = [
    { date: '2025-12-13', requests: 45, timestamp: '2025-12-13' },
    { date: '2025-12-12', requests: 32, timestamp: '2025-12-12' },
    { date: '2025-12-11', requests: 67, timestamp: '2025-12-11' },
    { date: '2025-12-10', requests: 28, timestamp: '2025-12-10' },
    { date: '2025-12-09', requests: 54, timestamp: '2025-12-09' },
  ];

  let totalRequests = usageData.reduce((sum, item) => sum + item.requests, 0);
  let averageRequests = Math.round(totalRequests / usageData.length);
</script>

<div class="flex h-screen bg-slate-50">
  <Sidebar />

  <main class="flex-1 overflow-auto">
    <div class="p-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">Usage History</h1>
        <p class="text-slate-600">Track your API usage and quota</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div class="bg-white rounded-lg shadow p-6">
          <p class="text-slate-600 text-sm mb-2">Total Requests (7 days)</p>
          <p class="text-3xl font-bold text-slate-900">{totalRequests}</p>
          <p class="text-slate-500 text-xs mt-2">Requests across all API keys</p>
        </div>
        <div class="bg-white rounded-lg shadow p-6">
          <p class="text-slate-600 text-sm mb-2">Daily Average</p>
          <p class="text-3xl font-bold text-slate-900">{averageRequests}</p>
          <p class="text-slate-500 text-xs mt-2">Requests per day</p>
        </div>
        <div class="bg-white rounded-lg shadow p-6">
          <p class="text-slate-600 text-sm mb-2">Status</p>
          <p class="text-3xl font-bold text-green-600">Active</p>
          <p class="text-slate-500 text-xs mt-2">Within quota limits</p>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold text-slate-900 mb-6">Daily Usage</h2>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-slate-200">
                <th class="text-left px-4 py-3 text-sm font-semibold text-slate-900">Date</th>
                <th class="text-right px-4 py-3 text-sm font-semibold text-slate-900">Requests</th>
                <th class="text-center px-4 py-3 text-sm font-semibold text-slate-900">Status</th>
              </tr>
            </thead>
            <tbody>
              {#each usageData as item (item.timestamp)}
                <tr class="border-b border-slate-200 hover:bg-slate-50">
                  <td class="px-4 py-3 text-sm text-slate-900">
                    {new Date(item.date).toLocaleDateString(undefined, {
                      weekday: 'short',
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                    })}
                  </td>
                  <td class="px-4 py-3 text-right text-sm font-medium text-slate-900">{item.requests}</td>
                  <td class="px-4 py-3 text-center text-sm">
                    <span class="inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium"
                      >OK</span
                    >
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>

      <div class="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 class="font-semibold text-blue-900 mb-2">About Usage Tracking</h3>
        <p class="text-blue-800 text-sm">Usage is tracked for each API key. Each request to the image tagging endpoint counts as one request. Quota resets weekly.</p>
      </div>
    </div>
  </main>
</div>
