import api from './api';
import type { ExpenseForecastResponse, ForecastRequest } from '../types/prediction';

export async function fetchExpenseForecast(payload: ForecastRequest = {}): Promise<ExpenseForecastResponse> {
  const response = await api.post<ExpenseForecastResponse>('/predictions/expense-forecast', payload);
  return response.data;
}
