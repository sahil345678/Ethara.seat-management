import { useState } from 'react';
import { useAvailableSeats, useAllocateSeat } from '../hooks/useSeats';
import { useEmployees } from '../hooks/useEmployees';
import { SeatGrid } from '../components/SeatGrid';
import { Dialog } from '../components/Dialog';
import { Search, CheckCircle2, AlertCircle, CalendarCheck } from 'lucide-react';
import { Employee, Seat } from '../types';
import { useToast } from '../contexts/ToastContext';
import { useNotification } from '../contexts/NotificationContext';
import clsx from 'clsx';

export const SeatAllocation = () => {
  const [employeeSearch, setEmployeeSearch] = useState('');
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null);
  const [selectedSeat, setSelectedSeat] = useState<Seat | null>(null);
  const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);
  
  const { addToast } = useToast();
  const { addNotification } = useNotification();

  // Fetch pending employees using the powerful search endpoint
  const { data: employeesData, isLoading: isEmpLoading } = useEmployees({
    page: 1,
    page_size: 5,
    search: employeeSearch || undefined,
    status: 'Active',
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
    
    try {
      await allocateMutation.mutateAsync({
        employee_id: selectedEmployee.id,
        seat_id: selectedSeat ? selectedSeat.id : undefined, // undefined triggers the Auto-Allocation Engine from Phase 7!
      });
      addToast(`Successfully allocated seat to ${selectedEmployee.name}.`, 'success');
      addNotification(
        'Seat Allocated', 
        `${selectedEmployee.name} has been assigned to ${selectedSeat ? `Seat ${selectedSeat.seat_number}` : 'a smart proximity seat'}.`, 
        'success'
      );
      setSelectedEmployee(null);
      setSelectedSeat(null);
      setEmployeeSearch('');
      setIsConfirmModalOpen(false);
    } catch (err: any) {
      addToast(err.message || "Failed to allocate seat.", 'error');
      setIsConfirmModalOpen(false);
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500 max-w-7xl mx-auto">
      <div>
        <h1 className="text-3xl font-black text-gray-900 tracking-tight">Seat Allocation Engine</h1>
        <p className="mt-1 text-base text-gray-500">Manually select a seat or let the proximity algorithm auto-allocate.</p>
      </div>



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
          onClick={() => setIsConfirmModalOpen(true)}
          disabled={!selectedEmployee}
          className="btn-primary bg-blue-500 hover:bg-blue-400 text-white px-8 py-3 text-base font-bold shadow-lg disabled:opacity-50 transition-all focus:ring-white"
        >
          Review Assignment
        </button>
      </div>

      <Dialog
        isOpen={isConfirmModalOpen}
        onClose={() => !allocateMutation.isPending && setIsConfirmModalOpen(false)}
        title="Confirm Allocation"
        footer={
          <>
            <button
              type="button"
              className="btn-secondary"
              onClick={() => setIsConfirmModalOpen(false)}
              disabled={allocateMutation.isPending}
            >
              Cancel
            </button>
            <button
              type="button"
              className="btn-primary bg-blue-600 hover:bg-blue-700"
              onClick={handleAllocate}
              disabled={allocateMutation.isPending}
            >
              {allocateMutation.isPending ? "Allocating..." : "Confirm Assignment"}
            </button>
          </>
        }
      >
        <div className="flex flex-col items-center justify-center text-center p-4">
          <div className="h-16 w-16 rounded-full bg-blue-50 flex items-center justify-center mb-4">
            <CalendarCheck className="h-8 w-8 text-blue-500" />
          </div>
          <p className="text-gray-900 font-medium mb-1">
            Please confirm the seat assignment for <strong className="text-brand-600">{selectedEmployee?.name}</strong>.
          </p>
          
          <div className="w-full mt-6 bg-gray-50 rounded-xl p-4 border border-gray-100 text-left">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-500 text-xs font-semibold uppercase tracking-wider mb-1">Employee</p>
                <p className="font-bold text-gray-900">{selectedEmployee?.name}</p>
                <p className="text-xs text-gray-500 font-mono mt-0.5">{selectedEmployee?.employee_code}</p>
              </div>
              <div>
                <p className="text-gray-500 text-xs font-semibold uppercase tracking-wider mb-1">Department</p>
                <p className="font-bold text-gray-900">{selectedEmployee?.department || 'N/A'}</p>
              </div>
              <div className="col-span-2 pt-3 border-t border-gray-200 mt-1">
                <p className="text-gray-500 text-xs font-semibold uppercase tracking-wider mb-1">Target Seat</p>
                {selectedSeat ? (
                  <p className="font-bold text-gray-900 text-lg">
                    {selectedSeat.seat_number} 
                    <span className="text-sm font-medium text-gray-500 ml-2">
                      (Floor {selectedSeat.floor}, Zone {selectedSeat.zone}, Bay {selectedSeat.bay})
                    </span>
                  </p>
                ) : (
                  <p className="font-bold text-blue-600 text-lg flex items-center">
                    Auto-Assigned Proximity Seat
                    <span className="ml-2 inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10">
                      Smart Algorithm
                    </span>
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </Dialog>
    </div>
  );
};
