import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { Dashboard } from '../Dashboard';
import * as hooks from '../../hooks/useDashboard';
import { BrowserRouter } from 'react-router-dom';

// Mock the custom hooks since they were already rigorously tested in Batch 3
vi.mock('../../hooks/useDashboard');

// Recharts relies on ResizeObserver which isn't in JSDom by default
global.ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
};

describe('Dashboard Page', () => {
  const renderDashboard = () => render(<BrowserRouter><Dashboard /></BrowserRouter>);

  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(hooks.useDashboardSummary).mockReturnValue({ data: null, isLoading: true } as any);
    vi.mocked(hooks.useProjectUtilization).mockReturnValue({ data: null, isLoading: true } as any);
    vi.mocked(hooks.useFloorUtilization).mockReturnValue({ data: null, isLoading: true } as any);
  });

  it('renders loading state initially while hooks are pending', () => {
    renderDashboard();
    expect(screen.getByText(/aggregating real-time dashboard metrics/i)).toBeInTheDocument();
  });

  it('renders the ErrorState component if any API fetch fails', () => {
    vi.mocked(hooks.useDashboardSummary).mockReturnValue({ isError: true } as any);
    renderDashboard();
    expect(screen.getByText(/failed to load dashboard telemetry from the server/i)).toBeInTheDocument();
  });

  it('renders the DashboardCards and DashboardCharts when data is available', () => {
    vi.mocked(hooks.useDashboardSummary).mockReturnValue({ 
      data: { total_employees: 42, total_seats: 100, occupied_seats: 10, available_seats: 90, reserved_seats: 0, pending_allocations: 5 },
      isLoading: false 
    } as any);
    vi.mocked(hooks.useProjectUtilization).mockReturnValue({ data: [], isLoading: false } as any);
    vi.mocked(hooks.useFloorUtilization).mockReturnValue({ data: [], isLoading: false } as any);
    
    renderDashboard();
    
    // Check if the DashboardCards mounted and displayed the numeric data
    expect(screen.getByText('42')).toBeInTheDocument(); // Total employees
    expect(screen.getByText('100')).toBeInTheDocument(); // Total seats
    
    // Check if the headers of the charts are rendered
    expect(screen.getByText(/floor utilization/i)).toBeInTheDocument();
    expect(screen.getByText(/top projects by seat allocation/i)).toBeInTheDocument();
  });
});
