import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';
import { Project, PaginatedResponse, ProjectStatus, Employee } from '../types';

interface GetProjectsParams {
  page?: number;
  page_size?: number;
  search?: string;
  status?: ProjectStatus;
  sort_by?: string;
  sort_desc?: boolean;
}

export const useProjects = (params: GetProjectsParams) => {
  return useQuery({
    queryKey: ['projects', params],
    queryFn: async () => {
      const { data } = await api.get<PaginatedResponse<Project>>('/projects', { params });
      return data;
    },
  });
};

export const useProjectEmployees = (projectId?: string, params?: { page?: number; page_size?: number }) => {
  return useQuery({
    queryKey: ['projects', projectId, 'employees', params],
    queryFn: async () => {
      const { data } = await api.get<PaginatedResponse<Employee>>(`/projects/${projectId}/employees`, { params });
      return data;
    },
    enabled: !!projectId,
  });
};

export const useCreateProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<Project>) => {
      const { data } = await api.post<Project>('/projects', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
};
