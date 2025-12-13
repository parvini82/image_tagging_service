<script lang="ts">
  import { apiKeysStore } from '../stores/apiKeys';
  let selectedLang = 'curl';
  let copied = false;

  let currentApiKey = '';
  apiKeysStore.subscribe((keys) => {
    if (keys.length > 0) {
      currentApiKey = keys[0].masked_key || 'YOUR_API_KEY';
    }
  });

  function copyToClipboard(text: string) {
    navigator.clipboard.writeText(text);
    copied = true;
    setTimeout(() => {
      copied = false;
    }, 2000);
  }

  const curlExample = `curl -X POST https://yourdomain.com/api/v1/tag/ \\
  -H "Authorization: Api-Key YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "image_url": "https://example.com/image.jpg",
    "mode": "fast"
  }'`;

  const pythonExample = `import requests

headers = {
    "Authorization": "Api-Key YOUR_API_KEY",
    "Content-Type": "application/json"
}

data = {
    "image_url": "https://example.com/image.jpg",
    "mode": "fast"
}

response = requests.post(
    "https://yourdomain.com/api/v1/tag/",
    headers=headers,
    json=data
)

print(response.json())`;

  const jsExample = `const apiKey = 'YOUR_API_KEY';
const imageUrl = 'https://example.com/image.jpg';

const response = await fetch('https://yourdomain.com/api/v1/tag/', {
  method: 'POST',
  headers: {
    'Authorization': \`Api-Key \${apiKey}\`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    image_url: imageUrl,
    mode: 'fast'
  })
});

const result = await response.json();
console.log(result);`;
</script>

<div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
  <div class="max-w-4xl mx-auto">
    <!-- Header -->
    <div class="mb-12">
      <h1 class="text-4xl font-bold text-white mb-2">API Documentation</h1>
      <p class="text-slate-300">Learn how to integrate the Image Tagging API into your application</p>
    </div>

    <!-- Getting Started -->
    <div class="bg-slate-800 rounded-lg p-8 mb-8 border border-slate-700">
      <h2 class="text-2xl font-bold text-white mb-4">Getting Started</h2>
      <div class="space-y-4 text-slate-300">
        <p>1. <strong>Sign up</strong> for an account (if you haven't already)</p>
        <p>2. <strong>Generate an API Key</strong> from your dashboard</p>
        <p>3. <strong>Copy the key</strong> - it's shown only once!</p>
        <p>4. <strong>Make requests</strong> using the examples below</p>
      </div>
    </div>

    <!-- API Key Info -->
    <div class="bg-blue-900/20 border border-blue-700/50 rounded-lg p-6 mb-8">
      <h3 class="text-lg font-semibold text-blue-300 mb-3">📋 Your API Key</h3>
      <p class="text-slate-300 mb-3">Use this key in all API requests:</p>
      <div class="bg-slate-900 rounded p-4 border border-slate-700 font-mono text-sm">
        <span class="text-amber-400">{currentApiKey}</span>
      </div>
      <p class="text-sm text-slate-400 mt-3">⚠️ Keep your API key secret. Never share it or commit it to version control.</p>
    </div>

    <!-- Base URL -->
    <div class="bg-slate-800 rounded-lg p-8 mb-8 border border-slate-700">
      <h2 class="text-2xl font-bold text-white mb-4">Base URL</h2>
      <div class="bg-slate-900 rounded p-4 border border-slate-700 font-mono text-sm text-slate-300">
        https://yourdomain.com
      </div>
      <p class="text-slate-400 mt-3 text-sm">Replace with your actual domain after deployment</p>
    </div>

    <!-- Authentication -->
    <div class="bg-slate-800 rounded-lg p-8 mb-8 border border-slate-700">
      <h2 class="text-2xl font-bold text-white mb-4">Authentication</h2>
      <p class="text-slate-300 mb-4">All requests require the API key in the Authorization header:</p>
      <div class="bg-slate-900 rounded p-4 border border-slate-700 font-mono text-sm text-slate-300">
        Authorization: Api-Key YOUR_API_KEY
      </div>
    </div>

    <!-- Endpoints -->
    <div class="bg-slate-800 rounded-lg p-8 mb-8 border border-slate-700">
      <h2 class="text-2xl font-bold text-white mb-6">Endpoint</h2>

      <!-- Tag Image Endpoint -->
      <div class="mb-8">
        <h3 class="text-xl font-semibold text-white mb-4 flex items-center gap-2">
          <span class="bg-green-600 px-3 py-1 rounded text-sm font-mono">POST</span>
          <span>/api/v1/tag/</span>
        </h3>

        <!-- Request -->
        <div class="mb-6">
          <h4 class="text-lg font-semibold text-slate-200 mb-3">Request</h4>
          <div class="space-y-2 text-slate-300 text-sm mb-4">
            <p><strong>Content-Type:</strong> application/json</p>
            <p><strong>Authentication:</strong> Required (API Key)</p>
          </div>

          <h5 class="font-semibold text-slate-300 mb-2">Request Body:</h5>
          <div class="bg-slate-900 rounded p-4 border border-slate-700 font-mono text-sm text-slate-300">
            <pre>{`{
  "image_url": "https://example.com/image.jpg",
  "mode": "fast"  // or "detailed"
}`}</pre>
          </div>

          <div class="mt-4 space-y-2 text-sm text-slate-400">
            <p><strong>Parameters:</strong></p>
            <ul class="list-disc list-inside space-y-1">
              <li><code class="bg-slate-700 px-2 py-1 rounded">image_url</code> (string, required): URL of the image to tag</li>
              <li><code class="bg-slate-700 px-2 py-1 rounded">mode</code> (string, optional): "fast" (default) or "detailed"</li>
            </ul>
          </div>
        </div>

        <!-- Response -->
        <div class="mb-6">
          <h4 class="text-lg font-semibold text-slate-200 mb-3">Response</h4>
          <p class="text-slate-300 text-sm mb-3">Success (200 OK):</p>
          <div class="bg-slate-900 rounded p-4 border border-slate-700 font-mono text-sm text-slate-300">
            <pre>{`{
  "tags": [
    {
      "name": "dress",
      "confidence": 0.95,
      "category": "clothing"
    },
    {
      "name": "blue",
      "confidence": 0.87,
      "category": "color"
    }
  ],
  "processing_time_ms": 245,
  "model": "vision-model-v2"
}`}</pre>
          </div>
        </div>
      </div>
    </div>

    <!-- Code Examples -->
    <div class="bg-slate-800 rounded-lg p-8 mb-8 border border-slate-700">
      <h2 class="text-2xl font-bold text-white mb-6">Code Examples</h2>

      <!-- Language Selector -->
      <div class="flex gap-3 mb-6">
        {#each ['curl', 'python', 'javascript'] as lang}
          <button
            on:click={() => (selectedLang = lang)}
            class={`px-4 py-2 rounded font-medium transition ${
              selectedLang === lang
                ? 'bg-blue-600 text-white'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            {lang.charAt(0).toUpperCase() + lang.slice(1)}
          </button>
        {/each}
      </div>

      <!-- Code Display -->
      <div class="relative">
        <div class="bg-slate-900 rounded p-4 border border-slate-700 font-mono text-sm text-slate-300 overflow-x-auto">
          <pre>{selectedLang === 'curl'
            ? curlExample
            : selectedLang === 'python'
            ? pythonExample
            : jsExample}</pre>
        </div>

        <!-- Copy Button -->
        <button
          on:click={() =>
            copyToClipboard(
              selectedLang === 'curl'
                ? curlExample
                : selectedLang === 'python'
                ? pythonExample
                : jsExample
            )}
          class="absolute top-3 right-3 bg-slate-700 hover:bg-slate-600 text-slate-300 px-3 py-1 rounded text-sm font-medium transition"
        >
          {copied ? '✓ Copied!' : 'Copy'}
        </button>
      </div>
    </div>

    <!-- Error Handling -->
    <div class="bg-slate-800 rounded-lg p-8 mb-8 border border-slate-700">
      <h2 class="text-2xl font-bold text-white mb-4">Error Handling</h2>
      <div class="space-y-4">
        <div>
          <p class="text-slate-300 mb-2"><strong>401 Unauthorized:</strong></p>
          <p class="text-slate-400 text-sm">Invalid or missing API key. Check that your key is correct and in the Authorization header.</p>
        </div>
        <div>
          <p class="text-slate-300 mb-2"><strong>400 Bad Request:</strong></p>
          <p class="text-slate-400 text-sm">Invalid request parameters. Check that image_url is a valid URL.</p>
        </div>
        <div>
          <p class="text-slate-300 mb-2"><strong>429 Too Many Requests:</strong></p>
          <p class="text-slate-400 text-sm">API rate limit exceeded. You have 20 requests per week.</p>
        </div>
        <div>
          <p class="text-slate-300 mb-2"><strong>500 Internal Server Error:</strong></p>
          <p class="text-slate-400 text-sm">Server error. Try again later or contact support.</p>
        </div>
      </div>
    </div>

    <!-- Rate Limiting -->
    <div class="bg-amber-900/20 border border-amber-700/50 rounded-lg p-6 mb-8">
      <h3 class="text-lg font-semibold text-amber-300 mb-3">⏱️ Rate Limits</h3>
      <p class="text-slate-300"><strong>20 requests per week</strong> per API key</p>
      <p class="text-slate-400 text-sm mt-2">Rate limits reset every 7 days. Contact us if you need higher limits.</p>
    </div>

    <!-- Support -->
    <div class="bg-slate-800 rounded-lg p-8 border border-slate-700">
      <h2 class="text-2xl font-bold text-white mb-4">Need Help?</h2>
      <p class="text-slate-300 mb-4">
        For questions or issues with the API, please contact our support team:
      </p>
      <div class="space-y-2 text-slate-400">
        <p>📧 Email: support@example.com</p>
        <p>💬 Discord: <a href="#" class="text-blue-400 hover:text-blue-300">Join our community</a></p>
        <p>📖 Docs: <a href="#" class="text-blue-400 hover:text-blue-300">Full documentation</a></p>
      </div>
    </div>
  </div>
</div>

<style>
  :global(body) {
    background: #0f172a;
  }
</style>
