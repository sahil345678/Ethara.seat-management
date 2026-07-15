import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';
import { Seat, PaginatedResponse, SeatStatus, SeatAllocation } from '../types';

interface GetSeatsParams {
  page?: number;
  page_size?: number;
  floor?: number;
  zone?: string;
  status?: SeatStatus;
  search?: string;
  sort_by?: string;
  sort_desc?: boolean;
}

export const useSeats = (params: GetSeatsParams) => {
  return useQuery({
    queryKey: ['seats', params],
    queryFn: async () => {
      const { data } = await api.get<PaginatedResponse<Seat>>('/seats', { params });
      return data;
    },
  });
};

export const useAvailableSeats = (params: { page?: number; page_size?: number; floor?: number; zone?: string }) => {
  return useQuery({
    queryKey: ['seats', 'available', params],
    queryFn: async () => {
      const { data } = await api.get<PaginatedResponse<Seat>>('/seats/available', { params });
      return data;
    },
  });
};

export const useCreateSeat = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<Seat>) => {
      const { data } = await api.post<Seat>('/seats', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['seats'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
};

export const useAllocateSeat = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: { employee_id: string; seat_id?: string }) => {
      const { data } = await api.post<SeatAllocation>('/seats/allocate', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['seats'] });
      queryClient.invalidateQueries({ queryKey: ['employees'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
};

export const useReleaseSeat = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: { employee_id?: string; seat_id?: string }) => {
      const { data } = await api.post<SeatAllocation>('/seats/release', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['seats'] });
      queryClient.invalidateQueries({ queryKey: ['employees'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
};
