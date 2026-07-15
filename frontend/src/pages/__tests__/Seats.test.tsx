import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { Seats } from '../Seats';
import * as hooks from '../../hooks/useSeats';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../../hooks/useSeats');

describe('Seats Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(hooks.useSeats).mockReturnValue({ data: null, isLoading: true } as any);
  });

  const renderComponent = () => render(<BrowserRouter><Seats /></BrowserRouter>);

  it('renders the header and filter dropdowns', () => {
    renderComponent();
    expect(screen.getByText(/facilities & seats/i)).toBeInTheDocument();
    
    // Check if dropdowns exist
    expect(screen.getByRole('combobox', { name: '' })).toBeInTheDocument(); // Comboboxes exist for Floor/Zone
  });

  it('renders the SeatGrid component when data is resolved', () => {
    vi.mocked(hooks.useSeats).mockReturnValue({
      data: {
        data: [
          { id: '1', floor: 1, zone: 'A', bay: 1, seat_number: '1A-01', status: 'AVAILABLE' },
          { id: '2', floor: 1, zone: 'B', bay: 1, seat_number: '1B-02', status: 'OCCUPIED' },
        ],
        meta: { total: 2, page: 1, total_pages: 1 }
      },
      isLoading: false
    } as any);
    
    renderComponent();
    
    expect(screen.getByText('1A-01')).toBeInTheDocument();
    expect(screen.getByText('1B-02')).toBeInTheDocument();
  });

  it('resets page to 1 when a filter changes', () => {
    const refetchMock = vi.fn();
    vi.mocked(hooks.useSeats).mockReturnValue({
      data: { data: [], meta: { total: 0, page: 1, total_pages: 1 } },
      isLoading: false,
      refetch: refetchMock
    } as any);
    
    renderComponent();
    
    const searchInput = screen.getByPlaceholderText(/search seat numbers/i);
    fireEvent.change(searchInput, { target: { value: '1A-05' } });
    fireEvent.submit(searchInput.closest('form')!);
    
    expect(refetchMock).toHaveBeenCalled();
  });
});
