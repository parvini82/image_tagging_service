<script lang="ts">
  import { authStore } from '../stores/auth';
  import { getQuotaPercentage } from '../lib/utils';

  $: quotaUsed = $authStore.keyInfo
    ? $authStore.keyInfo.weeklyQuota - $authStore.keyInfo.remainingQuota
    : 0;
  $: percentageUsed = $authStore.keyInfo
    ? getQuotaPercentage(quotaUsed, $authStore.keyInfo.weeklyQuota)
    : 0;
</script>

<div class="bg-white rounded-lg shadow p-6">
  <h2 class="text-xl font-bold text-slate-900 mb-6">Usage Statistics</h2>

  {#if $authStore.keyInfo}
    <div class="space-y-6">
      <div>
        <div class="flex justify-between items-center mb-3">
          <label class="text-sm font-medium text-slate-600">Requests Used</label>
          <span class="text-sm font-semibold text-slate-900">{quotaUsed} / {$authStore.keyInfo.weeklyQuota}</span>
        </div>
        <div class="w-full bg-slate-200 rounded-full h-3">
          <div
            class="bg-blue-600 h-3 rounded-full transition-all duration-300"
            style="width: {Math.min(percentageUsed, 100)}%"
          ></div>
        </div>
        <p class="text-xs text-slate-500 mt-2">{percentageUsed}% of quota used</p>
      </div>

      <div class="bg-slate-50 rounded-lg p-4">
        <p class="text-sm text-slate-600 mb-1">Status</p>
        {#if percentageUsed >= 100}
          <p class="font-semibold text-red-600">Quota Exceeded</p>
        {:else if percentageUsed >= 80}
          <p class="font-semibold text-orange-600">Quota Running Low</p>
        {:else}
          <p class="font-semibold text-green-600">Quota Available</p>
        {/if}
      </div>

      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p class="text-xs text-blue-900">
          Your API quota resets every 7 days. Contact support if you need higher limits.
        </p>
      </div>
    </div>
  {/if}
</div>
