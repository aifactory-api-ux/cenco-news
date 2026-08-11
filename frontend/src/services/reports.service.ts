// src/services/reports.service.ts
import api from '../lib/api';
import { Report, ReportCreate, ReportStatus, ReportTemplate } from '../../shared/types';

export async function fetchReports(page = 1, pageSize = 20): Promise<{ items: Report[]; total: number; page: number; page_size: number; pages: number }> {
  const response = await api.get('/api/v1/reports', { params: { page, page_size: pageSize } });
  return response.data;
}

export async function fetchReportTemplates(): Promise<ReportTemplate[]> {
  const response = await api.get('/api/v1/reports/templates');
  return response.data.items as ReportTemplate[];
}

export async function createReport(report: ReportCreate): Promise<Report> {
  const response = await api.post('/api/v1/reports', report);
  return response.data as Report;
}

export async function approveReport(reportId: string): Promise<void> {
  await api.post(`/api/v1/reports/${reportId}/approve`);
}

export async function sendReport(reportId: string): Promise<void> {
  await api.post(`/api/v1/reports/${reportId}/send`);
}
