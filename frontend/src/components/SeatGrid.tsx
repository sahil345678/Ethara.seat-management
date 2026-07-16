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
        return 'bg-blue-50 border-blue-200 text-blue-700 opacity-70 cursor-not-allowed';
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
      <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 xl:grid-cols-10 gap-4 animate-pulse">
        {Array.from({ length: 30 }).map((_, i) => (
          <div key={i} className="h-16 rounded-xl bg-gray-200"></div>
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
    <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 xl:grid-cols-10 gap-3">
      {seats.map((seat) => {
        const isInteractive = seat.status === 'Available' && !!onSeatClick;
        const isSelected = selectedSeatId === seat.id;
        
        return (
          <button
            key={seat.id}
            type="button"
            onClick={() => isInteractive && onSeatClick && onSeatClick(seat)}
            disabled={!isInteractive && !!onSeatClick && !isSelected}
            className={clsx(
              "relative flex flex-col items-center justify-center p-2 sm:p-3 rounded-xl border-2 transition-all duration-200",
              getStatusClasses(seat.status, isInteractive),
              isInteractive && !isSelected ? "shadow-sm" : "",
              isSelected ? "ring-4 ring-blue-500/50 border-blue-600 scale-105 shadow-md z-10 bg-blue-50" : "",
              !isInteractive && !isSelected && !!onSeatClick && "opacity-40 grayscale"
            )}
            title={`Floor ${seat.floor}, Zone ${seat.zone}, Bay ${seat.bay}\nStatus: ${seat.status}`}
          >
            <Armchair className="h-5 w-5 mb-1 opacity-80" />
            <span className="text-[11px] font-bold tracking-tight">{seat.seat_number}</span>
            <span className="text-[9px] mt-0.5 uppercase font-semibold opacity-70 tracking-wider hidden sm:block">
              {seat.status}
            </span>
          </button>
        );
      })}
    </div>
  );
};
