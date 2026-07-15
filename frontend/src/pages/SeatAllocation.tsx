import { useState } from 'react';
import { useAvailableSeats, useAllocateSeat } from '../hooks/useSeats';
import { useEmployees } from '../hooks/useEmployees';
import { SeatGrid } from '../components/SeatGrid';
import { Search, CheckCircle2, AlertCircle } from 'lucide-react';
import { Employee, Seat } from '../types';
import clsx from 'clsx';

export const SeatAllocation = () => {
  const [employeeSearch, setEmployeeSearch] = useState('');
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null);
  const [selectedSeat, setSelectedSeat] = useState<Seat | null>(null);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  // Fetch pending employees using the powerful search endpoint
  const { data: employeesData, isLoading: isEmpLoading } = useEmployees({
    page: 1,
    page_size: 5,
    search: employeeSearch || undefined,
    status: 'ACTIVE',
  });

  // Fetch only AVAILABLE seats
  const { data: seatsData, isLoading: isSeatsLoading } = useAvailableSeats({
    page: 1,
    page_size: 40,
    floor: undefined, // Could add filters here if desired
  });

  const allocateMutation = useAllocateSeat();

  const handleAllocate = async () => {
    if (!selectedEmployee) return;
    setSuccessMsg('');
    setErrorMsg('');
    
    try {
      await allocateMutation.mutateAsync({
        employee_id: selectedEmployee.id,
        seat_id: selectedSeat ? selectedSeat.id : undefined, // undefined triggers the Auto-Allocation Engine from Phase 7!
      });
      setSuccessMsg(`Successfully allocated seat to ${selectedEmployee.name}.`);
      setSelectedEmployee(null);
      setSelectedSeat(null);
      setEmployeeSearch('');
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to allocate seat.");
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500 max-w-7xl mx-auto">
      <div>
        <h1 className="text-3xl font-black text-gray-900 tracking-tight">Seat Allocation Engine</h1>
        <p className="mt-1 text-base text-gray-500">Manually select a seat or let the proximity algorithm auto-allocate.</p>
      </div>

      {(successMsg || errorMsg) && (
        <div className={clsx("p-4 rounded-xl flex items-center border-2", successMsg ? "bg-green-50 border-green-200 text-green-800" : "bg-red-50 border-red-200 text-red-800")}>
          {successMsg ? <CheckCircle2 className="w-5 h-5 mr-3 flex-shrink-0" /> : <AlertCircle className="w-5 h-5 mr-3 flex-shrink-0" />}
          <p className="font-semibold text-sm">{successMsg || errorMsg}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Step 1: Employee Selection */}
        <div className="card p-6 h-fit border-2 border-transparent focus-within:border-blue-100 transition-colors">
          <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-blue-600 text-xs text-white mr-2">1</span>
            Select Employee
          </h2>
          <div className="relative mb-4">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search by name or code..."
              value={employeeSearch}
              onChange={(e) => setEmployeeSearch(e.target.value)}
              className="w-full rounded-lg border-gray-300 pl-10 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm py-2 border"
            />
          </div>
          
          <div className="space-y-2 max-h-80 overflow-y-auto pr-2">
            {isEmpLoading && <div className="text-sm text-gray-500 animate-pulse">Searching...</div>}
            {!isEmpLoading && employeesData?.data.map((emp) => (
              <button
                key={emp.id}
                onClick={() => setSelectedEmployee(emp)}
                className={clsx(
                  "w-full text-left p-3 rounded-lg border-2 transition-all",
                  selectedEmployee?.id === emp.id 
                    ? "border-blue-500 bg-blue-50" 
                    : "border-transparent bg-gray-50 hover:bg-gray-100"
                )}
              >
                <div className="font-bold text-gray-900 text-sm">{emp.name}</div>
                <div className="text-xs text-gray-500 font-mono mt-0.5">{emp.employee_code}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Step 2: Seat Selection (Optional) */}
        <div className="card p-6 lg:col-span-2">
          <h2 className="text-lg font-bold text-gray-900 mb-2 flex items-center">
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-blue-600 text-xs text-white mr-2">2</span>
            Select Target Seat <span className="ml-2 text-sm font-medium text-gray-400 bg-gray-100 px-2 py-0.5 rounded-full">Optional</span>
          </h2>
          <p className="text-sm text-gray-500 mb-6 border-b border-gray-100 pb-4">
            Pick a specific physical seat, or leave this unselected to trigger the <strong className="text-blue-600">Smart Proximity Algorithm</strong> which auto-assigns based on project teammates.
          </p>

          <SeatGrid 
            seats={seatsData?.data || []} 
            isLoading={isSeatsLoading}
            selectedSeatId={selectedSeat?.id}
            onSeatClick={(seat) => setSelectedSeat(seat.id === selectedSeat?.id ? null : seat)}
          />
        </div>
      </div>

      {/* Action Footer */}
      <div className="card p-6 flex items-center justify-between bg-gray-900 text-white shadow-xl">
        <div>
          <h3 className="font-bold text-lg">Ready to Allocate</h3>
          <p className="text-sm text-gray-400 mt-1">
            {selectedEmployee ? (
              <>Allocating <strong>{selectedEmployee.name}</strong> to {selectedSeat ? `Seat ${selectedSeat.seat_number}` : <span className="text-blue-400">Auto-Assigned Proximity Seat</span>}</>
            ) : "Select an employee to proceed."}
          </p>
        </div>
        <button
          onClick={handleAllocate}
          disabled={!selectedEmployee || allocateMutation.isPending}
          className="btn-primary bg-blue-500 hover:bg-blue-400 text-white px-8 py-3 text-base font-bold shadow-lg disabled:opacity-50 transition-all focus:ring-white"
        >
          {allocateMutation.isPending ? "Allocating..." : "Confirm Allocation"}
        </button>
      </div>
    </div>
  );
};
