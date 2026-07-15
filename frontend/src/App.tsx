import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

// We will create these components in the next batches.
// For now, they are empty functional components to establish the routing scaffold.
const MainLayout = () => <div className="min-h-screen flex items-center justify-center text-gray-500">Layout (Pending Batch 3)</div>;
const Dashboard = () => <div>Dashboard</div>;
const Employees = () => <div>Employees</div>;
const Projects = () => <div>Projects</div>;
const Seats = () => <div>Seats</div>;
const AiAssistant = () => <div>AI Assistant</div>;

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="employees" element={<Employees />} />
          <Route path="projects" element={<Projects />} />
          <Route path="seats" element={<Seats />} />
          <Route path="ai" element={<AiAssistant />} />
          <Route path="*" element={<div className="p-8 text-center text-red-500">404 - Page Not Found</div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
