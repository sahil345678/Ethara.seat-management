import { DashboardSummary } from '../types';
import { Users, Armchair, CheckCircle, Clock, Archive } from 'lucide-react';
import clsx from 'clsx';

interface DashboardCardsProps {
  summary: DashboardSummary;
}

export const DashboardCards = ({ summary }: DashboardCardsProps) => {
  const cards = [
    { title: 'Total Employees', value: summary.total_employees, icon: Users, color: 'text-blue-600', bg: 'bg-blue-100' },
    { title: 'Total Seats', value: summary.total_seats, icon: Armchair, color: 'text-indigo-600', bg: 'bg-indigo-100' },
    { title: 'Occupied Seats', value: summary.occupied_seats, icon: CheckCircle, color: 'text-green-600', bg: 'bg-green-100' },
    { title: 'Available Seats', value: summary.available_seats, icon: CheckCircle, color: 'text-teal-600', bg: 'bg-teal-100' },
    { title: 'Reserved Seats', value: summary.reserved_seats, icon: Archive, color: 'text-purple-600', bg: 'bg-purple-100' },
    { title: 'Pending Allocations', value: summary.pending_allocations, icon: Clock, color: 'text-orange-600', bg: 'bg-orange-100' },
  ];

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {cards.map((card, idx) => (
        <div key={idx} className="card p-6 flex items-center shadow-sm transition-shadow hover:shadow-md">
          <div className={clsx('mr-4 flex h-14 w-14 items-center justify-center rounded-full', card.bg, card.color)}>
            <card.icon className="h-7 w-7" aria-hidden="true" />
          </div>
          <div>
            <p className="text-sm font-semibold text-gray-500 uppercase tracking-wide">{card.title}</p>
            <p className="text-3xl font-black text-gray-900 tracking-tight">{card.value.toLocaleString()}</p>
          </div>
        </div>
      ))}
    </div>
  );
};
