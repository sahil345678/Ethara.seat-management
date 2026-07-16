import { Seat, SeatStatus } from '../types';
import clsx from 'clsx';
import { Armchair } from 'lucide-react';

interface SeatGridProps {
  seats: Seat[];
  onSeatClick?: (seat: Seat) => void;
  selectedSeatId?: string;
  isLoading?: boolean;
}

export const SeatGrid = ({ seats, onSeatClick, selectedSeatId, isLoading }: SeatGridProps) => {
  const getStatusClasses = (status: SeatStatus, isInteractive: boolean) => {
    switch (status) {
      case 'Available': 
        return clsx('bg-teal-50 border-teal-200 text-teal-700', isInteractive && 'hover:bg-teal-100 hover:border-teal-400');
      case 'Occupied': 
        // We now make occupied interactive for release workflows
        return clsx('bg-blue-50 border-blue-200 text-blue-700', isInteractive && 'hover:bg-blue-100 hover:border-blue-400 cursor-pointer');
      case 'Reserved': 
        return 'bg-purple-50 border-purple-200 text-purple-700 opacity-70 cursor-not-allowed';
      case 'Maintenance': 
        return 'bg-gray-100 border-gray-300 text-gray-500 opacity-60 cursor-not-allowed';
      default: 
        return 'bg-gray-50 border-gray-200 text-gray-400';
    }
  };

  if (isLoading) {
    return (
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4 animate-pulse">
        {Array.from({ length: 30 }).map((_, i) => (
          <div key={i} className="h-24 rounded-xl bg-gray-200"></div>
        ))}
      </div>
    );
  }

  if (seats.length === 0) {
    return (
      <div className="text-center p-12 bg-white rounded-xl border-2 border-dashed border-gray-200">
        <Armchair className="mx-auto h-12 w-12 text-gray-300 mb-3" />
        <p className="text-gray-500 font-medium text-sm">No seats match the current filters.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3">
      {seats.map((seat) => {
        // Now BOTH Available and Occupied can be interactive if onSeatClick is provided
        const isInteractive = (seat.status === 'Available' || seat.status === 'Occupied') && !!onSeatClick;
        const isSelected = selectedSeatId === seat.id;
        
        const tooltipText = `Seat: ${seat.seat_number}
Status: ${seat.status}
Floor: ${seat.floor} | Zone: ${seat.zone} | Bay: ${seat.bay}
${seat.occupant_name ? `\nOccupant: ${seat.occupant_name}` : ''}
${seat.project_name ? `Project: ${seat.project_name}` : ''}`;

        return (
          <button
            key={seat.id}
            type="button"
            onClick={() => isInteractive && onSeatClick && onSeatClick(seat)}
            disabled={!isInteractive && !!onSeatClick && !isSelected}
            className={clsx(
              "relative flex flex-col items-center justify-center p-3 sm:p-4 rounded-xl border-2 transition-all duration-200 h-28 overflow-hidden",
              getStatusClasses(seat.status, isInteractive),
              isInteractive && !isSelected ? "shadow-sm" : "",
              isSelected ? "ring-4 ring-blue-500/50 border-blue-600 scale-105 shadow-md z-10 bg-blue-50" : "",
              !isInteractive && !isSelected && !!onSeatClick && "opacity-40 grayscale"
            )}
            title={tooltipText}
          >
            <Armchair className={clsx("h-6 w-6 mb-1", seat.status === 'Occupied' ? "opacity-100 text-blue-600" : "opacity-80")} />
            <span className="text-xs font-black tracking-tight mb-1">{seat.seat_number}</span>
            <span className="text-[10px] uppercase font-bold opacity-70 tracking-wider">
              {seat.status}
            </span>
            {seat.status === 'Occupied' && (
              <div className="mt-1 flex flex-col items-center w-full px-1">
                <span className="text-[10px] font-semibold text-blue-900 truncate w-full text-center">
                  {seat.occupant_name || 'Assigned'}
                </span>
                <span className="text-[9px] font-medium text-blue-700/80 truncate w-full text-center">
                  {seat.project_name || ''}
                </span>
              </div>
            )}
          </button>
        );
      })}
    </div>
  );
};
