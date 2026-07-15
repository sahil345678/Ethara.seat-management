import { useQuery } from '@tanstack/react-query';
import api from '../services/api';
import { DashboardSummary, ProjectUtilization, FloorUtilization } from '../types';

export const useDashboardSummary = () => {
  return useQuery({
    queryKey: ['dashboard', 'summary'],
    queryFn: async () => {
      const { data } = await api.get<DashboardSummary>('/dashboard/summary');
      return data;
    },
  });
};

export const useProjectUtilization = () => {
  return useQuery({
    queryKey: ['dashboard', 'project-utilization'],
    queryFn: async () => {
      const { data } = await api.get<ProjectUtilization[]>('/dashboard/project-utilization');
      return data;
    },
  });
};

export const useFloorUtilization = () => {
  return useQuery({
    queryKey: ['dashboard', 'floor-utilization'],
    queryFn: async () => {
      const { data } = await api.get<FloorUtilization[]>('/dashboard/floor-utilization');
      return data;
    },
  });
};
