import api from './api';
import type { AIInsightRequest, AIInsightResponse } from '../types/ai';

export async function fetchAIInsights(payload: AIInsightRequest = {}): Promise<AIInsightResponse> {
  const response = await api.post<AIInsightResponse>('/ai/insights', payload);
  return response.data;
}
