<script lang="ts">
  import { onMount } from 'svelte';
  import { push } from 'svelte-spa-router';
  import Router from 'svelte-spa-router';
  import { wrap } from 'svelte-spa-router/wrap';
  import { authStore } from './stores/auth';
  import { apiClient } from './lib/api';
  import LoginPage from './pages/LoginPage.svelte';
  import RegisterPage from './pages/RegisterPage.svelte';
  import Dashboard from './pages/Dashboard.svelte';
  import Tagger from './pages/Tagger.svelte';
  import Usage from './pages/Usage.svelte';
  import ApiDocs from './pages/ApiDocs.svelte';
  import './styles/global.css';

  let isInitialized = false;

  onMount(async () => {
    try {
      const user = await apiClient.getMe();
      authStore.restoreSession(user);
    } catch (err) {
      // User not authenticated, this is normal
      authStore.logout();
    } finally {
      isInitialized = true;
    }
  });

  const routes = {
    '/login': wrap({
      component: LoginPage,
      conditions: [(detail) => !$authStore.isAuthenticated],
    }),
    '/register': wrap({
      component: RegisterPage,
      conditions: [(detail) => !$authStore.isAuthenticated],
    }),
    '/dashboard': wrap({
      component: Dashboard,
      conditions: [(detail) => $authStore.isAuthenticated],
    }),
    '/dashboard/tagger': wrap({
      component: Tagger,
      conditions: [(detail) => $authStore.isAuthenticated],
    }),
    '/dashboard/usage': wrap({
      component: Usage,
      conditions: [(detail) => $authStore.isAuthenticated],
    }),
    '/dashboard/docs': wrap({
      component: ApiDocs,
      conditions: [(detail) => $authStore.isAuthenticated],
    }),
  };

  function onRouterReady() {
    // Router is ready, navigation can begin
  }
</script>

{#if isInitialized}
  <Router {routes} on:routeFailed={() => push('/login')} on:conditionsFailed={() => push('/login')} />
{:else}
  <div class="flex items-center justify-center min-h-screen bg-slate-50">
    <div class="text-slate-600">Initializing...</div>
  </div>
{/if}
