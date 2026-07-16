import { useState } from 'react';
import { useSeats } from '../hooks/useSeats';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorState } from '../components/ErrorState';
import { SeatGrid } from '../components/SeatGrid';
import { Search, ChevronLeft, ChevronRight, Filter } from 'lucide-react';
import { SeatStatus } from '../types';

export const Seats = () => {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [floor, setFloor] = useState<number | undefined>();
  const [zone, setZone] = useState<string | undefined>();
  const [status, setStatus] = useState<SeatStatus | undefined>();
  const pageSize = 60; // Show a large grid

  const { data, isLoading, isError, refetch } = useSeats({
    page,
    page_size: pageSize,
    search: search || undefined,
    floor,
    zone,
    status,
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    refetch();
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-gray-900 tracking-tight">Facilities & Seats</h1>
          <p className="mt-1 text-base text-gray-500">View physical office layout and seat occupancy.</p>
        </div>
        
        <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-3">
          <div className="relative rounded-md shadow-sm">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              <Search className="h-4 w-4 text-gray-400" />
            </div>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="block w-full rounded-lg border-0 py-2 pl-10 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
              placeholder="Search seat numbers..."
            />
          </div>
          
          <select
            value={floor || ''}
            onChange={(e) => { setFloor(e.target.value ? Number(e.target.value) : undefined); setPage(1); }}
            className="block w-32 rounded-lg border-0 py-2 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-blue-600 sm:text-sm font-medium"
          >
            <option value="">All Floors</option>
            {[1, 2, 3, 4, 5].map(f => <option key={f} value={f}>Floor {f}</option>)}
          </select>

          <select
            value={zone || ''}
            onChange={(e) => { setZone(e.target.value || undefined); setPage(1); }}
            className="block w-32 rounded-lg border-0 py-2 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-blue-600 sm:text-sm font-medium"
          >
            <option value="">All Zones</option>
            {['A','B','C','D','E','F','G','H','I','J'].map(z => <option key={z} value={z}>Zone {z}</option>)}
          </select>
        </form>
      </div>

      <div className="card p-6">
        {/* Legend */}
        <div className="flex flex-wrap items-center gap-4 mb-6 pb-6 border-b border-gray-100">
          <div className="flex items-center text-sm font-semibold text-gray-600"><span className="w-3 h-3 rounded-full bg-teal-400 mr-2 shadow-inner"></span> Available</div>
          <div className="flex items-center text-sm font-semibold text-gray-600"><span className="w-3 h-3 rounded-full bg-blue-500 mr-2 shadow-inner"></span> Occupied</div>
          <div className="flex items-center text-sm font-semibold text-gray-600"><span className="w-3 h-3 rounded-full bg-purple-400 mr-2 shadow-inner"></span> Reserved</div>
        </div>

        {isError ? (
          <ErrorState onRetry={() => refetch()} />
        ) : (
          <SeatGrid seats={data?.data || []} isLoading={isLoading} />
        )}

        <div className="card p-6">
        {data && data.total_pages > 1 && (
          <div className="flex items-center justify-between">
            <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1} className="btn-secondary shadow-sm">
              <ChevronLeft className="w-4 h-4 mr-2" /> Previous
            </button>
            <span className="text-sm font-bold text-gray-700">Page {page} of {data.total_pages}</span>
            <button onClick={() => setPage(p => p + 1)} disabled={page >= data.total_pages} className="btn-secondary shadow-sm">
              Next <ChevronRight className="w-4 h-4 ml-2" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
