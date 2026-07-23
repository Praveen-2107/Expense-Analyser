import api from './api';
import type { UploadResponse, UploadStatement } from '../types/upload';

export async function uploadCsvFile(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post<UploadResponse>('/uploads/csv', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
}

export async function uploadPdfFile(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post<UploadResponse>('/uploads/pdf', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
}

export async function fetchStatements(): Promise<UploadStatement[]> {
  const response = await api.get<UploadStatement[]>('/uploads/statements');
  return response.data;
}
