import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';
import { Navbar } from '../components/Navbar';

/**
 * Main Layout wrapper for the authenticated portion of the application.
 * Manages the responsive sidebar state and provides the main scrollable content area.
 */
export const MainLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen w-full overflow-hidden bg-gray-50 font-sans">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      
      <div className="flex flex-1 flex-col overflow-hidden min-w-0">
        <Navbar onMenuClick={() => setSidebarOpen(true)} />
        
        <main className="flex-1 overflow-y-auto bg-gray-50 p-4 sm:p-6 lg:p-8 relative z-0">
          <div className="mx-auto max-w-7xl h-full">
            {/* The Outlet renders the nested child routes (pages) */}
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};
