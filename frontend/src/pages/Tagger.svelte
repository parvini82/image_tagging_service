<script lang="ts">
  import { authStore } from '../stores/auth';
  import Sidebar from '../components/Sidebar.svelte';
  import Tagger from '../components/Tagger.svelte';
</script>

<div class="flex h-screen bg-slate-50">
  <Sidebar />

  <div class="flex-1 overflow-auto">
    <div class="max-w-4xl mx-auto px-6 py-8">
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-slate-900 mb-2">Image Tagger</h1>
        <p class="text-slate-600">Test the image tagging API with your images</p>
      </div>

      <Tagger />
    </div>
  </div>
</div>
