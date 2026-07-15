import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';
import { Employee, PaginatedResponse, EmployeeStatus } from '../types';

interface GetEmployeesParams {
  page?: number;
  page_size?: number;
  search?: string;
  status?: EmployeeStatus;
  project_id?: string;
  sort_by?: string;
  sort_desc?: boolean;
}

export const useEmployees = (params: GetEmployeesParams) => {
  return useQuery({
    queryKey: ['employees', params],
    queryFn: async () => {
      const { data } = await api.get<PaginatedResponse<Employee>>('/employees', { params });
      return data;
    },
  });
};

export const useEmployee = (id?: string) => {
  return useQuery({
    queryKey: ['employees', id],
    queryFn: async () => {
      const { data } = await api.get<Employee>(`/employees/${id}`);
      return data;
    },
    enabled: !!id,
  });
};

export const useCreateEmployee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<Employee>) => {
      const { data } = await api.post<Employee>('/employees', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employees'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
};

export const useUpdateEmployee = (id: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<Employee>) => {
      const { data } = await api.put<Employee>(`/employees/${id}`, payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employees'] });
      queryClient.invalidateQueries({ queryKey: ['employees', id] });
    },
  });
};

export const useDeleteEmployee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/employees/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employees'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
};
