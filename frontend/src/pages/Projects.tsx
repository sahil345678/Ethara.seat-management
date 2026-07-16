import { useState } from 'react';
import { useProjects, useProjectEmployees } from '../hooks/useProjects';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorState } from '../components/ErrorState';
import { EmptyState } from '../components/EmptyState';
import { Search, ChevronLeft, ChevronRight, FolderKanban, Users, ChevronDown, ChevronUp } from 'lucide-react';
import { ProjectStatus, Project } from '../types';
import clsx from 'clsx';

export const Projects = () => {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState<ProjectStatus | undefined>();
  const [expandedProjectId, setExpandedProjectId] = useState<string | null>(null);
  const pageSize = 10;

  const { data, isLoading, isError, refetch, isFetching } = useProjects({
    page,
    page_size: pageSize,
    search: search || undefined,
    status,
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    refetch();
  };

  const toggleExpand = (projectId: string) => {
    setExpandedProjectId(prev => prev === projectId ? null : projectId);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-gray-900 tracking-tight">Projects</h1>
          <p className="mt-1 text-base text-gray-500">Manage client projects and view assigned teams.</p>
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
              placeholder="Search projects..."
            />
          </div>
          
          <select
            value={status || ''}
            onChange={(e) => {
              setStatus((e.target.value as ProjectStatus) || undefined);
              setPage(1);
            }}
            className="block w-full rounded-lg border-0 py-2.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-blue-600 sm:text-sm sm:leading-6 font-medium"
          >
            <option value="">All Statuses</option>
            <option value="ACTIVE">Active</option>
            <option value="COMPLETED">Completed</option>
            <option value="ON_HOLD">On Hold</option>
            <option value="CANCELLED">Cancelled</option>
          </select>
        </form>
      </div>

      <div className="card overflow-hidden">
        {isLoading ? (
          <LoadingSpinner fullHeight message="Loading projects..." />
        ) : isError ? (
          <div className="p-12"><ErrorState onRetry={() => refetch()} /></div>
        ) : !data || data.data.length === 0 ? (
          <EmptyState 
            icon={<FolderKanban className="h-8 w-8 text-gray-400" />}
            title="No projects found" 
            description="Try adjusting your search query or status filter." 
          />
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50/50">
                  <tr>
                    <th scope="col" className="py-4 pl-4 pr-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider sm:pl-6">Project Name</th>
                    <th scope="col" className="px-3 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Manager</th>
                    <th scope="col" className="px-3 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
                    <th scope="col" className="px-3 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Created</th>
                    <th scope="col" className="relative py-4 pl-3 pr-4 sm:pr-6"><span className="sr-only">Actions</span></th>
                  </tr>
                </thead>
                <tbody className={clsx("divide-y divide-gray-200 bg-white", isFetching && "opacity-60 transition-opacity")}>
                  {data.data.map((project) => (
                    <ProjectRow 
                      key={project.id} 
                      project={project} 
                      isExpanded={expandedProjectId === project.id} 
                      onToggle={() => toggleExpand(project.id)} 
                    />
                  ))}
                </tbody>
              </table>
            </div>
            
            <div className="flex items-center justify-between border-t border-gray-200 bg-gray-50/50 px-4 py-3 sm:px-6">
              <div className="flex flex-1 justify-between sm:hidden">
                <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1} className="btn-secondary">Previous</button>
                <button onClick={() => setPage(p => p + 1)} disabled={page >= data.total_pages} className="btn-secondary ml-3">Next</button>
              </div>
              <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm text-gray-700">
                    Showing <span className="font-bold">{(page - 1) * pageSize + 1}</span> to <span className="font-bold">{Math.min(page * pageSize, data.total)}</span> of <span className="font-bold">{data.total}</span> projects
                  </p>
                </div>
                <div>
                  <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
                    <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1} className="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 disabled:opacity-50 transition-colors">
                      <ChevronLeft className="h-5 w-5" aria-hidden="true" />
                    </button>
                    <button onClick={() => setPage(p => p + 1)} disabled={page >= data.total_pages} className="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 disabled:opacity-50 transition-colors">
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

// Extracted Sub-Component for handling nested data
const ProjectRow = ({ project, isExpanded, onToggle }: { project: Project, isExpanded: boolean, onToggle: () => void }) => {
  // Only fetch employees when expanded to save bandwidth
  const { data: teamData, isLoading } = useProjectEmployees(project.id, { page: 1, page_size: 50 });

  return (
    <>
      <tr className="hover:bg-gray-50/80 transition-colors cursor-pointer" onClick={onToggle}>
        <td className="whitespace-nowrap py-4 pl-4 pr-3 sm:pl-6">
          <div className="flex items-center">
            <div className="h-10 w-10 flex-shrink-0 rounded-lg bg-indigo-100 flex items-center justify-center text-indigo-700">
              <FolderKanban className="h-5 w-5" />
            </div>
            <div className="ml-4">
              <div className="font-bold text-gray-900">{project.name}</div>
              <div className="text-gray-500 text-xs w-48 truncate">{project.description}</div>
            </div>
          </div>
        </td>
        <td className="whitespace-nowrap px-3 py-4 text-sm font-medium text-gray-700">{project.manager_name || 'Unassigned'}</td>
        <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
          <span className={clsx("inline-flex items-center rounded-md px-2 py-1 text-xs font-bold uppercase tracking-wider ring-1 ring-inset", 
            project.status === 'Active' ? "bg-green-50 text-green-700 ring-green-600/20" : 
            project.status === 'Completed' ? "bg-blue-50 text-blue-700 ring-blue-600/20" :
            "bg-gray-50 text-gray-600 ring-gray-500/10"
          )}>
            {project.status}
          </span>
        </td>
        <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{new Date(project.created_at).toLocaleDateString()}</td>
        <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
          <button className="text-gray-400 hover:text-gray-600">
            {isExpanded ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
          </button>
        </td>
      </tr>
      {isExpanded && (
        <tr>
          <td colSpan={5} className="bg-gray-50/50 px-6 py-4 border-b border-gray-200">
            <div className="pl-14">
              <h4 className="text-xs font-bold text-gray-500 uppercase flex items-center mb-3">
                <Users className="w-4 h-4 mr-2" /> Assigned Team Members
              </h4>
              {isLoading ? (
                <div className="animate-pulse flex space-x-4"><div className="h-4 bg-gray-200 rounded w-1/4"></div></div>
              ) : !teamData || teamData.data.length === 0 ? (
                <p className="text-sm text-gray-500 italic">No employees assigned to this project yet.</p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {teamData.data.map(emp => (
                    <span key={emp.id} className="inline-flex items-center rounded-full bg-white px-2.5 py-1 text-xs font-semibold text-gray-700 border border-gray-300 shadow-sm">
                      {emp.name}
                    </span>
                  ))}
                  {teamData.total > 50 && (
                    <span className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-1 text-xs font-semibold text-gray-500 border border-gray-200">
                      +{teamData.total - 50} more
                    </span>
                  )}
                </div>
              )}
            </div>
          </td>
        </tr>
      )}
    </>
  );
};
