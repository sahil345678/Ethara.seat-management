import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useEmployees } from '../useEmployees';
import { useAiQuery } from '../useAi';
import { useDashboardSummary } from '../useDashboard';
import { api } from '../../services/api';

// Globally mock the Axios client to completely prevent external HTTP calls
vi.mock('../../services/api', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('TanStack React Query Hooks', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    // Reinstantiate a fresh, cache-cleared query client before every test
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false, // Turn off retries so error tests fail instantly
        },
      },
    });
    vi.clearAllMocks();
  });

  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );

  describe('useEmployees Query Hook', () => {
    it('fetches and returns paginated employee data successfully', async () => {
      const mockData = {
        data: [{ id: '1', name: 'John Doe', status: 'ACTIVE' }],
        meta: { total: 1, page: 1, total_pages: 1 }
      };
      
      // Setup the mock response
      vi.mocked(api.get).mockResolvedValueOnce({ data: mockData });

      const { result } = renderHook(() => useEmployees({ page: 1 }), { wrapper });

      // Initially it should be pending
      expect(result.current.isLoading).toBe(true);

      // Wait for it to resolve
      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true);
      });

      expect(result.current.data).toEqual(mockData);
      expect(api.get).toHaveBeenCalledWith('/employees/', {
        params: { page: 1, page_size: 10, search: undefined, status: undefined, project_id: undefined }
      });
    });

    it('handles REST API exceptions gracefully, pushing them to React Query Error state', async () => {
      vi.mocked(api.get).mockRejectedValueOnce(new Error('Network offline'));

      const { result } = renderHook(() => useEmployees({ page: 1 }), { wrapper });

      await waitFor(() => {
        expect(result.current.isError).toBe(true);
      });

      expect(result.current.error).toBeDefined();
    });
  });
  
  describe('useDashboardSummary Query Hook', () => {
    it('fetches aggregated metric totals', async () => {
      const mockData = { total_employees: 50, occupied_seats: 40 };
      vi.mocked(api.get).mockResolvedValueOnce({ data: mockData });

      const { result } = renderHook(() => useDashboardSummary(), { wrapper });

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true);
      });

      expect(result.current.data).toEqual(mockData);
    });
  });

  describe('useAiQuery Mutation Hook', () => {
    it('executes a POST request to the Gemini router and returns the text response', async () => {
      const mockResponse = { answer: 'John is currently seated on Floor 2, Zone B.' };
      vi.mocked(api.post).mockResolvedValueOnce({ data: mockResponse });

      const { result } = renderHook(() => useAiQuery(), { wrapper });

      // Trigger the mutation
      result.current.mutate('Where is John?');

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true);
      });

      expect(api.post).toHaveBeenCalledWith('/ai/query', { query: 'Where is John?' });
      expect(result.current.data).toEqual(mockResponse);
    });
  });
});
