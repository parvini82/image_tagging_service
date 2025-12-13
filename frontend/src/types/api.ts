export interface TaggingRequest {
  image_url: string;
  mode?: 'fast' | 'reasoning' | 'advanced_reasoning';
}

export interface TaggingResponse {
  image_url: string;
  tags: Record<string, unknown> | string[] | unknown;
}

export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface APIKey {
  id: number;
  masked_key: string;
  created_at: string;
  last_used_at: string | null;
}

export interface APIKeyCreated {
  id: number;
  key: string;
  masked_key: string;
  created_at: string;
}
