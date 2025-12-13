export interface ApiKeyInfo {
  maskedKey: string;
  weeklyQuota: number;
  remainingQuota: number;
  lastUsedAt: string | null;
  quotaResetAt: string | null;
}

export interface TaggingRequest {
  image_url: string;
  mode?: 'fast' | 'reasoning' | 'advanced_reasoning';
}

export interface TaggingResponse {
  image_url: string;
  tags: Record<string, unknown> | string[] | unknown;
}

export interface UsageEntry {
  timestamp: string;
  endpoint: string;
  status: number;
  success: boolean;
}

export interface ErrorResponse {
  detail?: string;
  [key: string]: unknown;
}
