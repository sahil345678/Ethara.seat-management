import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { SeatAllocation } from '../SeatAllocation';
import * as seatHooks from '../../hooks/useSeats';
import * as empHooks from '../../hooks/useEmployees';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../../hooks/useSeats');
vi.mock('../../hooks/useEmployees');

describe('Seat Allocation Engine Page', () => {
  let mutateAsyncMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    vi.clearAllMocks();
    mutateAsyncMock = vi.fn();
    
    vi.mocked(empHooks.useEmployees).mockReturnValue({
      data: { data: [{ id: 'E1', name: 'John Target', employee_code: 'ETH-1' }] },
      isLoading: false
    } as any);

    vi.mocked(seatHooks.useAvailableSeats).mockReturnValue({
      data: { data: [{ id: 'S1', seat_number: '1A-01', status: 'AVAILABLE' }] },
      isLoading: false
    } as any);

    vi.mocked(seatHooks.useAllocateSeat).mockReturnValue({
      mutateAsync: mutateAsyncMock,
      isPending: false
    } as any);
  });

  const renderComponent = () => render(<BrowserRouter><SeatAllocation /></BrowserRouter>);

  it('allows manual allocation by selecting both employee and seat', async () => {
    renderComponent();
    
    // Select Employee
    fireEvent.click(screen.getByText('John Target'));
    
    // Select Seat
    fireEvent.click(screen.getByText('1A-01').closest('button')!);
    
    // Allocate
    const allocBtn = screen.getByText('Confirm Allocation');
    expect(allocBtn).not.toBeDisabled();
    
    fireEvent.click(allocBtn);
    
    await waitFor(() => {
      expect(mutateAsyncMock).toHaveBeenCalledWith({
        employee_id: 'E1',
        seat_id: 'S1'
      });
    });
  });

  it('allows auto-allocation via proximity algorithm by skipping seat selection', async () => {
    renderComponent();
    
    // Select Employee ONLY
    fireEvent.click(screen.getByText('John Target'));
    
    // Allocate
    const allocBtn = screen.getByText('Confirm Allocation');
    fireEvent.click(allocBtn);
    
    await waitFor(() => {
      expect(mutateAsyncMock).toHaveBeenCalledWith({
        employee_id: 'E1',
        seat_id: undefined // Triggers engine logic in backend
      });
    });
  });

  it('displays success message when allocation completes successfully', async () => {
    mutateAsyncMock.mockResolvedValueOnce({});
    renderComponent();
    
    fireEvent.click(screen.getByText('John Target'));
    fireEvent.click(screen.getByText('Confirm Allocation'));
    
    await waitFor(() => {
      expect(screen.getByText(/successfully allocated seat/i)).toBeInTheDocument();
    });
  });
});
