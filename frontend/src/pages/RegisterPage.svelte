<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { authStore } from '../stores/auth';
  import { apiClient } from '../lib/api';

  let email = '';
  let password = '';
  let password2 = '';
  let error = '';
  let loading = false;

  async function handleRegister() {
    if (!email.trim()) {
      error = 'Please enter your email.';
      return;
    }
    if (!password.trim()) {
      error = 'Please enter a password (at least 8 characters).';
      return;
    }
    if (password.length < 8) {
      error = 'Password must be at least 8 characters.';
      return;
    }
    if (password !== password2) {
      error = 'Passwords do not match.';
      return;
    }

    loading = true;
    error = '';

    try {
      await apiClient.register(email, password);
      const user = await apiClient.login(email, password);
      authStore.authenticate(user);
      push('/dashboard');
    } catch (err) {
      error = err instanceof Error ? err.message : 'Registration failed. Please try again.';
    } finally {
      loading = false;
    }
  }

  function handleKeyPress(e: KeyboardEvent) {
    if (e.key === 'Enter' && !loading) {
      handleRegister();
    }
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
  <div class="w-full max-w-md">
    <div class="bg-white rounded-lg shadow-2xl p-8">
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">Create Account</h1>
        <p class="text-slate-600">Image Tagging API</p>
      </div>

      <form on:submit|preventDefault={handleRegister} class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-slate-700 mb-2">
            Email
          </label>
          <input
            id="email"
            type="email"
            bind:value={email}
            placeholder="your@email.com"
            class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            disabled={loading}
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-slate-700 mb-2">
            Password (min 8 characters)
          </label>
          <input
            id="password"
            type="password"
            bind:value={password}
            placeholder="••••••••"
            class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            disabled={loading}
          />
        </div>

        <div>
          <label for="password2" class="block text-sm font-medium text-slate-700 mb-2">
            Confirm Password
          </label>
          <input
            id="password2"
            type="password"
            bind:value={password2}
            on:keypress={handleKeyPress}
            placeholder="••••••••"
            class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            disabled={loading}
          />
        </div>

        {#if error}
          <div class="bg-red-50 border border-red-200 rounded-lg p-4">
            <p class="text-red-800 text-sm font-medium">{error}</p>
          </div>
        {/if}

        <button
          type="submit"
          disabled={loading}
          class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 text-white font-medium py-2 px-4 rounded-lg transition duration-200 flex items-center justify-center gap-2"
        >
          {#if loading}
            <div class="spinner"></div>
            <span>Creating Account...</span>
          {:else}
            <span>Create Account</span>
          {/if}
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-slate-600 text-sm">Already have an account? <a href="#/login" class="text-blue-600 hover:text-blue-700 font-medium">Sign In</a></p>
      </div>
    </div>
  </div>
</div>

<style>
  .spinner {
    border: 2px solid #e2e8f0;
    border-top: 2px solid white;
    border-radius: 50%;
    width: 16px;
    height: 16px;
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
