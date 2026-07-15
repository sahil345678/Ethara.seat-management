import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { SeatGrid } from '../SeatGrid';
import { Seat } from '../../types';

const mockSeats: Seat[] = [
  { id: '1', floor: 1, zone: 'A', bay: 1, seat_number: '1A-01', status: 'AVAILABLE', created_at: '', updated_at: '' },
  { id: '2', floor: 1, zone: 'A', bay: 1, seat_number: '1A-02', status: 'OCCUPIED', created_at: '', updated_at: '' },
  { id: '3', floor: 1, zone: 'A', bay: 1, seat_number: '1A-03', status: 'RESERVED', created_at: '', updated_at: '' },
];

describe('SeatGrid Component', () => {
  it('renders a loading skeleton when isLoading is set to true', () => {
    const { container } = render(<SeatGrid seats={[]} isLoading={true} />);
    // The skeleton renders 30 pulsing placeholder divs
    expect(container.querySelectorAll('.animate-pulse > div').length).toBe(30);
  });

  it('renders a beautiful empty state when no seats match filters', () => {
    render(<SeatGrid seats={[]} />);
    expect(screen.getByText(/no seats match the current filters/i)).toBeInTheDocument();
  });

  it('renders seat elements with text corresponding to their label and status', () => {
    render(<SeatGrid seats={mockSeats} />);
    
    // Validate Labels
    expect(screen.getByText('1A-01')).toBeInTheDocument();
    expect(screen.getByText('1A-02')).toBeInTheDocument();
    
    // Validate Status Texts
    expect(screen.getByText('AVAILABLE')).toBeInTheDocument();
    expect(screen.getByText('OCCUPIED')).toBeInTheDocument();
    expect(screen.getByText('RESERVED')).toBeInTheDocument();
  });

  it('handles click interactions correctly based on seat status', () => {
    const clickMock = vi.fn();
    render(<SeatGrid seats={mockSeats} onSeatClick={clickMock} />);
    
    const availableSeatBtn = screen.getByText('1A-01').closest('button');
    const occupiedSeatBtn = screen.getByText('1A-02').closest('button');
    
    // Available seats should be clickable if onSeatClick is provided
    expect(availableSeatBtn).not.toBeDisabled();
    fireEvent.click(availableSeatBtn!);
    expect(clickMock).toHaveBeenCalledWith(mockSeats[0]);
    
    // Occupied/Reserved seats should be permanently disabled from interactions
    expect(occupiedSeatBtn).toBeDisabled();
  });
  
  it('applies selected styling when a seat ID matches selectedSeatId', () => {
    render(<SeatGrid seats={mockSeats} selectedSeatId="1" />);
    
    const availableSeatBtn = screen.getByText('1A-01').closest('button');
    // We check for our exact Tailwind utility ring classes
    expect(availableSeatBtn).toHaveClass('ring-4', 'ring-blue-500/50', 'border-blue-600', 'scale-105');
  });
});
