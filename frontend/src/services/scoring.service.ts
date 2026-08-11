// src/services/scoring.service.ts
import api from '../lib/api';
import { ScoringDimension, ScoringDimensionCreate, ScoringWeights } from '../../shared/types';

export async function fetchScoringDimensions(): Promise<ScoringDimension[]> {
  const response = await api.get('/api/v1/scoring/dimensions');
  return response.data.items as ScoringDimension[];
}

export async function createScoringDimension(dimension: ScoringDimensionCreate): Promise<ScoringDimension> {
  const response = await api.post('/api/v1/scoring/dimensions', dimension);
  return response.data as ScoringDimension;
}

export async function calculateScore(newsId: string, weights: ScoringWeights): Promise<void> {
  await api.post(`/api/v1/scoring/calculate/${newsId}`, weights);
}
