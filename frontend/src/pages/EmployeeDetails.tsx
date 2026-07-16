import { useParams, useNavigate } from 'react-router-dom';
import { useEmployee } from '../hooks/useEmployees';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorState } from '../components/ErrorState';
import { ArrowLeft, Briefcase, Mail, Building, Fingerprint, FolderKanban, Info } from 'lucide-react';
import clsx from 'clsx';

export const EmployeeDetails = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  // Utilize TanStack Query to fetch single employee via ID
  const { data: employee, isLoading, isError, refetch } = useEmployee(id);

  if (isLoading) return <LoadingSpinner fullHeight message="Loading employee profile..." />;
  if (isError || !employee) return <div className="py-12"><ErrorState onRetry={() => refetch()} message="We could not find that employee in the system." /></div>;

  return (
    <div className="space-y-6 max-w-5xl mx-auto animate-in fade-in duration-500">
      {/* Navigation Header */}
      <div className="flex items-center gap-4">
        <button onClick={() => navigate(-1)} className="btn-secondary rounded-full p-2.5 shadow-sm" aria-label="Go back">
          <ArrowLeft className="w-5 h-5 text-gray-600" />
        </button>
        <div>
          <h1 className="text-3xl font-black text-gray-900 tracking-tight">Employee Profile</h1>
        </div>
      </div>

      <div className="card overflow-hidden shadow-md border-0 ring-1 ring-gray-200">
        {/* Profile Hero Banner */}
        <div className="bg-gradient-to-r from-blue-700 via-blue-600 to-indigo-700 px-6 py-10 sm:px-12 flex flex-col sm:flex-row items-center sm:items-start gap-6 sm:gap-8">
          <div className="h-28 w-28 flex-shrink-0 rounded-full bg-white flex items-center justify-center text-5xl font-black text-blue-600 shadow-xl ring-4 ring-white/20">
            {employee.name.charAt(0)}
          </div>
          <div className="text-white text-center sm:text-left mt-2 sm:mt-0">
            <h2 className="text-4xl font-black tracking-tight">{employee.name}</h2>
            <p className="text-blue-100 font-semibold text-lg flex items-center justify-center sm:justify-start gap-2 mt-2">
              <Briefcase className="w-5 h-5 opacity-80" /> {employee.role}
            </p>
            <div className="mt-4 inline-flex items-center rounded-full bg-white/20 px-3 py-1 text-sm font-bold backdrop-blur-sm">
              <span className={clsx("w-2 h-2 rounded-full mr-2", employee.status === 'Active' ? 'bg-green-400' : 'bg-gray-300')}></span>
              {employee.status}
            </div>
          </div>
        </div>

        {/* Details Grid */}
        <div className="p-6 sm:p-10 grid grid-cols-1 md:grid-cols-2 gap-10 bg-white">
          
          {/* Column 1: Core Information */}
          <div className="space-y-6">
            <h3 className="text-xl font-bold text-gray-900 border-b border-gray-100 pb-3 flex items-center">
              <Info className="w-5 h-5 mr-2 text-blue-600" /> Core Information
            </h3>
            <dl className="space-y-5">
              <div className="flex items-start">
                <Fingerprint className="w-5 h-5 text-gray-400 mt-0.5 mr-3 flex-shrink-0" />
                <div>
                  <dt className="text-sm font-bold text-gray-500 uppercase tracking-wider">Employee Code</dt>
                  <dd className="mt-1.5 text-base text-gray-900 font-mono bg-gray-50 px-2.5 py-1 rounded-md inline-block border border-gray-200 shadow-sm">{employee.employee_code}</dd>
                </div>
              </div>
              <div className="flex items-start">
                <Mail className="w-5 h-5 text-gray-400 mt-0.5 mr-3 flex-shrink-0" />
                <div>
                  <dt className="text-sm font-bold text-gray-500 uppercase tracking-wider">Email Address</dt>
                  <dd className="mt-1 text-base font-medium text-gray-900">{employee.email}</dd>
                </div>
              </div>
              <div className="flex items-start">
                <Building className="w-5 h-5 text-gray-400 mt-0.5 mr-3 flex-shrink-0" />
                <div>
                  <dt className="text-sm font-bold text-gray-500 uppercase tracking-wider">Department</dt>
                  <dd className="mt-1 text-base font-medium text-gray-900">{employee.department}</dd>
                </div>
              </div>
            </dl>
          </div>

          {/* Column 2: Assignments & Allocation */}
          <div className="space-y-6">
            <h3 className="text-xl font-bold text-gray-900 border-b border-gray-100 pb-3 flex items-center">
              <FolderKanban className="w-5 h-5 mr-2 text-indigo-600" /> Workspace & Projects
            </h3>
            
            {/* Project Card */}
            <div className="rounded-xl border border-gray-200 bg-gray-50 p-5 shadow-sm transition-shadow hover:shadow-md">
              <h4 className="text-sm font-bold text-gray-500 uppercase tracking-wider flex items-center mb-3">
                Current Project Assignment
              </h4>
              {employee.project ? (
                <div>
                  <p className="font-black text-indigo-700 text-xl">{employee.project.name}</p>
                  {employee.project.description && (
                    <p className="text-sm text-gray-600 mt-2 leading-relaxed">{employee.project.description}</p>
                  )}
                  <div className="mt-4 flex items-center gap-3">
                    <span className="inline-flex items-center rounded-md bg-indigo-100 px-2.5 py-1 text-xs font-bold text-indigo-800 border border-indigo-200">
                      Status: {employee.project.status}
                    </span>
                  </div>
                </div>
              ) : (
                <p className="text-sm font-medium text-gray-500 italic bg-white p-3 rounded-lg border border-gray-200 border-dashed">
                  This employee is not currently assigned to any active project.
                </p>
              )}
            </div>

            {/* Seat Allocation Note */}
            <div className="rounded-xl border border-blue-100 bg-blue-50/50 p-5 shadow-sm">
              <h4 className="text-sm font-bold text-blue-800 uppercase tracking-wider flex items-center mb-2">
                Seat Allocation Protocol
              </h4>
              <p className="text-sm text-blue-900/80 leading-relaxed font-medium">
                Physical seat allocations are managed globally by the Allocation Engine. 
                Please navigate to the <span className="font-bold underline decoration-blue-300 underline-offset-2">Seats Dashboard</span> to view or modify this employee's spatial coordinates.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
