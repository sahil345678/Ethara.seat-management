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
    <div className="flex h-screen w-full overflow-hidden bg-surface-50 text-surface-900 font-sans selection:bg-brand-500 selection:text-white">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      
      <div className="flex flex-1 flex-col overflow-hidden min-w-0 bg-surface-50">
        <Navbar onMenuClick={() => setSidebarOpen(true)} />
        
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 relative z-0 animate-fade-in">
          <div className="mx-auto max-w-7xl h-full">
            {/* The Outlet renders the nested child routes (pages) */}
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};
