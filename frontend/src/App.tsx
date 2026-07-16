import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Import real components built in Batches 3, 4, and 5
import { MainLayout } from './layouts/MainLayout';
import { Dashboard } from './pages/Dashboard';
import { Employees } from './pages/Employees';
import { EmployeeDetails } from './pages/EmployeeDetails';
import { Projects } from './pages/Projects';
import { Seats } from './pages/Seats';
import { SeatAllocation } from './pages/SeatAllocation';
import { AiAssistant } from './pages/AiAssistant';
import { ToastProvider } from './contexts/ToastContext';
import { NotificationProvider } from './contexts/NotificationContext';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ToastProvider>
        <NotificationProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<MainLayout />}>
                <Route index element={<Navigate to="/dashboard" replace />} />
                <Route path="dashboard" element={<Dashboard />} />
                <Route path="employees" element={<Employees />} />
                <Route path="employees/:id" element={<EmployeeDetails />} />
                <Route path="projects" element={<Projects />} />
                <Route path="seats" element={<Seats />} />
                <Route path="seats/allocate" element={<SeatAllocation />} />
                <Route path="ai" element={<AiAssistant />} />
                <Route path="*" element={<div className="p-12 text-center text-red-500 font-bold text-xl">404 - Page Not Found</div>} />
              </Route>
            </Routes>
          </BrowserRouter>
        </NotificationProvider>
      </ToastProvider>
    </QueryClientProvider>
  );
}

export default App;
