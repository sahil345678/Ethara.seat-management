import { useMutation } from '@tanstack/react-query';
import api from '../services/api';
import { AiQueryResponse } from '../types';

export const useAiQuery = () => {
  return useMutation({
    mutationFn: async (query: string) => {
      const { data } = await api.post<AiQueryResponse>('/ai/query', { query });
      return data;
    },
  });
};
