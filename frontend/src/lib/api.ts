import type { ApiKeyInfo, TaggingRequest, TaggingResponse } from '../types/api';
import { authStore } from '../stores/auth';

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

    return headers;
  }

  private async handleResponse(response: Response) {
    const data = await response.json().catch(() => null);

    if (!response.ok) {
      // Try to extract meaningful error message from Django/DRF response
      let errorMessage = `HTTP ${response.status}`;

      if (data) {
        // Handle DRF validation errors (field-specific errors)
        if (typeof data === 'object') {
          // Check for non_field_errors first
          if (data.non_field_errors && Array.isArray(data.non_field_errors)) {
            errorMessage = data.non_field_errors[0];
          }
          // Check for detail field (common in DRF)
          else if (data.detail) {
            errorMessage = data.detail;
          }
          // Check for message field
          else if (data.message) {
            errorMessage = data.message;
          }
          // For field-specific errors, show the first one
          else {
            const firstFieldKey = Object.keys(data)[0];
            if (firstFieldKey && data[firstFieldKey]) {
              const fieldErrors = data[firstFieldKey];
              if (Array.isArray(fieldErrors) && fieldErrors.length > 0) {
                errorMessage = `${firstFieldKey}: ${fieldErrors[0]}`;
              } else if (typeof fieldErrors === 'string') {
                errorMessage = `${firstFieldKey}: ${fieldErrors}`;
              }
            }
          }
        } else if (typeof data === 'string') {
          errorMessage = data;
        }
      }

      throw new Error(errorMessage);
    }

    return data;
  }

  // ============= UI Auth Endpoints (Session-based) =============

  async register(email: string, password: string): Promise<{ id: number; email: string; created_at: string }> {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/register/`, {
      method: 'POST',
      headers: this.getHeaders(),
      credentials: 'include',
      body: JSON.stringify({ email, password, password2: password }),
    });
    return this.handleResponse(response);
  }

  async login(email: string, password: string): Promise<{ id: number; email: string; created_at: string }> {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/login/`, {
      method: 'POST',
      headers: this.getHeaders(),
      credentials: 'include',
      body: JSON.stringify({ email, password }),
    });
    return this.handleResponse(response);
  }

  async logout(): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/logout/`, {
      method: 'POST',
      headers: this.getHeaders(),
      credentials: 'include',
    });
    await this.handleResponse(response);
  }

  async getMe(): Promise<{ id: number; email: string; created_at: string }> {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/me/`, {
      method: 'GET',
      headers: this.getHeaders(),
      credentials: 'include',
    });
    return this.handleResponse(response);
  }

  // ============= API Key Management Endpoints =============

  async listAPIKeys(): Promise<Array<{ id: number; masked_key: string; created_at: string; last_used_at: string | null }>> {
    const response = await fetch(`${API_BASE_URL}/api/v1/keys/`, {
      method: 'GET',
      headers: this.getHeaders(),
      credentials: 'include',
    });
    return this.handleResponse(response);
  }

  async generateAPIKey(): Promise<{ id: number; key: string; masked_key: string; created_at: string }> {
    const response = await fetch(`${API_BASE_URL}/api/v1/keys/`, {
      method: 'POST',
      headers: this.getHeaders(),
      credentials: 'include',
      body: JSON.stringify({}),
    });
    return this.handleResponse(response);
  }

  async revokeAPIKey(keyId: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/v1/keys/${keyId}/`, {
      method: 'DELETE',
      headers: this.getHeaders(),
      credentials: 'include',
    });
    await this.handleResponse(response);
  }

  // ============= Image Tagging API (uses API key in header) =============

  async tagImage(request: TaggingRequest): Promise<TaggingResponse> {
    if (!this.apiKey) {
      throw new Error('No API key available. Generate one from the dashboard first.');
    }

    const headers = this.getHeaders({
      'Authorization': `Api-Key ${this.apiKey}`,
    });

    const response = await fetch(`${API_BASE_URL}/api/v1/tag/`, {
      method: 'POST',
      headers,
      body: JSON.stringify(request),
    });

    return this.handleResponse(response);
  }
}

export const apiClient = new ApiClient();
