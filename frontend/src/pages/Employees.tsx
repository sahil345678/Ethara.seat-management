import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useEmployees } from '../hooks/useEmployees';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorState } from '../components/ErrorState';
import { EmptyState } from '../components/EmptyState';
import { Search, ChevronLeft, ChevronRight, Eye } from 'lucide-react';
import { EmployeeStatus } from '../types';
import clsx from 'clsx';

export const Employees = () => {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState<EmployeeStatus | undefined>();
  const pageSize = 10;

  const { data, isLoading, isError, error, refetch, isFetching } = useEmployees({
    page,
    page_size: pageSize,
    search: search || undefined,
    status,
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    refetch(); // Trigger TanStack query refetch
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-gray-900 tracking-tight">Employees</h1>
          <p className="mt-1 text-base text-gray-500">Manage employee directory and view assignments.</p>
        </div>
        
        <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-3">
          <div className="relative rounded-md shadow-sm">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              <Search className="h-4 w-4 text-gray-400" aria-hidden="true" />
            </div>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="block w-full rounded-lg border-0 py-2.5 pl-10 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
              placeholder="Search names or emails..."
            />
          </div>
          
          <select
            value={status || ''}
            onChange={(e) => {
              setStatus((e.target.value as EmployeeStatus) || undefined);
              setPage(1); // Reset pagination on filter change
            }}
            className="block w-full rounded-lg border-0 py-2.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-blue-600 sm:text-sm sm:leading-6 font-medium"
          >
            <option value="">All Statuses</option>
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
          </select>
        </form>
      </div>

      {/* Main Content Area */}
      <div className="card overflow-hidden">
        {isLoading ? (
          <LoadingSpinner fullHeight message="Loading directory..." />
        ) : isError ? (
          <div className="p-12"><ErrorState onRetry={() => refetch()} message={error?.message} /></div>
        ) : !data || data.data.length === 0 ? (
          <EmptyState title="No employees found" description="Try adjusting your search query or filters to find what you're looking for." />
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50/50">
                  <tr>
                    <th scope="col" className="py-4 pl-4 pr-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider sm:pl-6">Employee</th>
                    <th scope="col" className="px-3 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Code</th>
                    <th scope="col" className="px-3 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Department</th>
                    <th scope="col" className="px-3 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Project</th>
                    <th scope="col" className="px-3 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
                    <th scope="col" className="relative py-4 pl-3 pr-4 sm:pr-6">
                      <span className="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody className={clsx("divide-y divide-gray-200 bg-white", isFetching && "opacity-60 transition-opacity")}>
                  {data.data.map((employee) => (
                    <tr key={employee.id} className="hover:bg-gray-50/80 transition-colors">
                      <td className="whitespace-nowrap py-4 pl-4 pr-3 sm:pl-6">
                        <div className="flex items-center">
                          <div className="h-10 w-10 flex-shrink-0 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold shadow-inner">
                            {employee.name.charAt(0)}
                          </div>
                          <div className="ml-4">
                            <div className="font-semibold text-gray-900">{employee.name}</div>
                            <div className="text-gray-500 text-sm">{employee.email}</div>
                          </div>
                        </div>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm font-mono text-gray-500">{employee.employee_code}</td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        <div className="text-gray-900 font-medium">{employee.department}</div>
                        <div className="text-gray-500 text-xs mt-0.5">{employee.role}</div>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {employee.project ? (
                          <span className="inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-xs font-semibold text-indigo-700 ring-1 ring-inset ring-indigo-700/10">
                            {employee.project.name}
                          </span>
                        ) : (
                          <span className="text-gray-400 italic text-xs font-medium">Unassigned</span>
                        )}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        <span className={clsx("inline-flex items-center rounded-md px-2 py-1 text-xs font-bold uppercase tracking-wider ring-1 ring-inset", 
                          employee.status === 'Active' ? "bg-green-50 text-green-700 ring-green-600/20" : "bg-gray-50 text-gray-600 ring-gray-500/10"
                        )}>
                          {employee.status}
                        </span>
                      </td>
                      <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                        <button 
                          onClick={() => navigate(`/employees/${employee.id}`)}
                          className="text-blue-600 hover:text-blue-800 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-md inline-flex items-center transition-colors"
                        >
                          <Eye className="w-4 h-4 mr-1.5" /> View
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            
            {/* Pagination Component */}
            <div className="flex items-center justify-between border-t border-gray-200 bg-gray-50/50 px-4 py-3 sm:px-6">
              <div className="flex flex-1 justify-between sm:hidden">
                <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1} className="btn-secondary">Previous</button>
                <button onClick={() => setPage(p => p + 1)} disabled={page >= data.total_pages} className="btn-secondary ml-3">Next</button>
              </div>
              <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm text-gray-700">
                    Showing <span className="font-bold">{(page - 1) * pageSize + 1}</span> to <span className="font-bold">{Math.min(page * pageSize, data.total)}</span> of <span className="font-bold">{data.total}</span> employees
                  </p>
                </div>
                <div>
                  <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
                    <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1} className="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 disabled:opacity-50 transition-colors">
                      <ChevronLeft className="h-5 w-5" aria-hidden="true" />
                    </button>
                    <button onClick={() => setPage(p => p + 1)} disabled={page >= data.total_pages} className="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 disabled:opacity-50 transition-colors">
                      <span className="sr-only">Next</span>
                      <ChevronRight className="h-5 w-5" aria-hidden="true" />
                    </button>
                  </nav>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
