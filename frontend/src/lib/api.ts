import type { ApiKeyInfo, TaggingRequest, TaggingResponse, UsageEntry } from '../types/api';
import { authStore } from '../stores/auth';
import { get } from 'svelte/store';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class ApiClient {
  private apiKey: string | null = null;

  constructor() {
    authStore.subscribe((state) => {
      this.apiKey = state.apiKey;
    });
  }

  private getHeaders(additionalHeaders: Record<string, string> = {}): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...additionalHeaders,
    };

    if (this.apiKey) {
      headers['Authorization'] = `Api-Key ${this.apiKey}`;
    }

    return headers;
  }

  private async handleResponse(response: Response) {
    const data = await response.json().catch(() => null);

    if (!response.ok) {
      const error = data?.detail || data?.message || `HTTP ${response.status}`;
      throw new Error(error);
    }

    return data;
  }

  async validateApiKey(key: string): Promise<ApiKeyInfo> {
    const response = await fetch(`${API_BASE_URL}/api/v1/health/`, {
      method: 'GET',
      headers: {
        'Authorization': `Api-Key ${key}`,
        'Content-Type': 'application/json',
      },
    });

    if (response.status === 401) {
      throw new Error('Invalid API key.');
    }

    if (response.status === 429) {
      throw new Error('API quota exceeded.');
    }

    if (!response.ok) {
      const data = await response.json().catch(() => null);
      throw new Error(data?.detail || `HTTP ${response.status}`);
    }

    // Mock response from backend with the API key info
    // In production, the backend would return actual data
    const info: ApiKeyInfo = {
      maskedKey: this.maskApiKey(key),
      weeklyQuota: 20,
      remainingQuota: 20,
      lastUsedAt: null,
      quotaResetAt: null,
    };

    return info;
  }

  async tagImage(request: TaggingRequest): Promise<TaggingResponse> {
    const response = await fetch(`${API_BASE_URL}/api/v1/tag/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(request),
    });

    return this.handleResponse(response);
  }

  async getUsageHistory(): Promise<UsageEntry[]> {
    // This endpoint does not exist yet, so we return mock data
    // In production, the backend would provide this endpoint
    return [
      {
        timestamp: new Date().toISOString(),
        endpoint: '/api/v1/tag/',
        status: 200,
        success: true,
      },
    ];
  }

  private maskApiKey(key: string): string {
    if (key.length <= 8) return key;
    return `${key.substring(0, 8)}****${key.substring(key.length - 4)}`;
  }
}

export const apiClient = new ApiClient();
