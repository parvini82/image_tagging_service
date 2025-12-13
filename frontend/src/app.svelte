<script lang="ts">
  import { onMount } from 'svelte';
  import Router from 'svelte-spa-router';
  import { wrap } from 'svelte-spa-router/wrap';
  import { authStore } from './stores/auth';
  import LoginPage from './pages/LoginPage.svelte';
  import Dashboard from './pages/Dashboard.svelte';
  import Tagger from './pages/Tagger.svelte';
  import Usage from './pages/Usage.svelte';
  import './styles/global.css';

  let routeLoading = false;
  let isInitialized = false;

  onMount(() => {
    authStore.restoreSession();
    isInitialized = true;
  });

  const routes = {
    '/login': wrap({
      component: LoginPage,
      conditions: [(detail) => !$authStore.isAuthenticated]
    }),
    '/dashboard': wrap({
      component: Dashboard,
      conditions: [(detail) => $authStore.isAuthenticated]
    }),
    '/dashboard/tagger': wrap({
      component: Tagger,
      conditions: [(detail) => $authStore.isAuthenticated]
    }),
    '/dashboard/usage': wrap({
      component: Usage,
      conditions: [(detail) => $authStore.isAuthenticated]
    }),
    '*': LoginPage,
  };

  function handleRouteEvent(event: CustomEvent) {
    routeLoading = event.detail.detail?.state === 'loading';
  }
</script>

{#if isInitialized}
  {#if $authStore.isAuthenticated}
    <div class="min-h-screen bg-slate-50">
      <Router {routes} on:routeEvent={handleRouteEvent} />
    </div>
  {:else}
    <Router {routes} on:routeEvent={handleRouteEvent} />
  {/if}
{:else}
  <div class="flex items-center justify-center min-h-screen bg-slate-50">
    <div class="text-slate-600">Loading...</div>
  </div>
{/if}
