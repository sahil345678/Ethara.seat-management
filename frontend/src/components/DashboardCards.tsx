import { DashboardSummary } from '../types';
import { Users, Armchair, CheckCircle, Clock, Archive } from 'lucide-react';
import clsx from 'clsx';

interface DashboardCardsProps {
  summary: DashboardSummary;
}

export const DashboardCards = ({ summary }: DashboardCardsProps) => {
  const cards = [
    { title: 'Total Employees', value: summary.total_employees, icon: Users, color: 'text-brand-600', bg: 'bg-brand-50 border-brand-100' },
    { title: 'Total Seats', value: summary.total_seats, icon: Armchair, color: 'text-indigo-600', bg: 'bg-indigo-50 border-indigo-100' },
    { title: 'Occupied Seats', value: summary.occupied_seats, icon: CheckCircle, color: 'text-emerald-600', bg: 'bg-emerald-50 border-emerald-100' },
    { title: 'Available Seats', value: summary.available_seats, icon: CheckCircle, color: 'text-teal-600', bg: 'bg-teal-50 border-teal-100' },
    { title: 'Reserved Seats', value: summary.reserved_seats, icon: Archive, color: 'text-purple-600', bg: 'bg-purple-50 border-purple-100' },
    { title: 'Pending Allocations', value: summary.pending_allocation, icon: Clock, color: 'text-orange-600', bg: 'bg-orange-50 border-orange-100' },
  ];

  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
      {cards.map((card, idx) => (
        <div key={idx} className="card p-6 flex items-center shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-y-1 group relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-white/40 to-transparent pointer-events-none" />
          <div className={clsx('mr-5 flex h-16 w-16 items-center justify-center rounded-2xl border shadow-sm transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3', card.bg, card.color)}>
            <card.icon className="h-7 w-7" aria-hidden="true" />
          </div>
          <div className="relative z-10">
            <p className="text-xs font-bold text-surface-500 uppercase tracking-wider">{card.title}</p>
            <p className="mt-1 text-3xl font-display font-bold text-surface-900 tracking-tight">{card.value.toLocaleString()}</p>
          </div>
        </div>
      ))}
    </div>
  );
};
