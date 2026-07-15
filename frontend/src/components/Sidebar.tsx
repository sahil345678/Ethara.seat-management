import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Users, FolderKanban, Armchair, MessageSquareCode, LogOut, X } from 'lucide-react';
import clsx from 'clsx';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const navItems = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Employees', path: '/employees', icon: Users },
  { name: 'Projects', path: '/projects', icon: FolderKanban },
  { name: 'Seats', path: '/seats', icon: Armchair },
  { name: 'AI Assistant', path: '/ai', icon: MessageSquareCode },
];

export const Sidebar = ({ isOpen, onClose }: SidebarProps) => {
  return (
    <>
      {/* Mobile Backdrop overlay for responsive design */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-20 bg-gray-900/50 backdrop-blur-sm lg:hidden transition-opacity"
          onClick={onClose}
          aria-hidden="true"
        />
      )}
      
      {/* Sidebar Container */}
      <aside
        className={clsx(
          "fixed inset-y-0 left-0 z-30 flex w-64 flex-col bg-white border-r border-gray-200 transition-transform duration-300 ease-in-out lg:static lg:flex lg:translate-x-0 shadow-lg lg:shadow-none",
          isOpen ? "translate-x-0 flex" : "-translate-x-full"
        )}
      >
        {/* Brand Header */}
        <div className="flex h-16 flex-shrink-0 items-center justify-between border-b border-gray-200 px-6">
          <span className="text-2xl font-black text-blue-600 tracking-tighter">Ethara.</span>
          <button onClick={onClose} className="lg:hidden p-1 rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-100 transition-colors">
            <X size={20} aria-label="Close sidebar" />
          </button>
        </div>
        
        {/* Navigation Links */}
        <nav className="flex-1 space-y-1.5 overflow-y-auto p-4">
          {navItems.map((item) => (
            <NavLink
              key={item.name}
              to={item.path}
              onClick={() => {
                if (window.innerWidth < 1024) onClose();
              }}
              className={({ isActive }) =>
                clsx(
                  "group flex items-center rounded-lg px-3 py-2.5 text-sm font-semibold transition-all duration-200",
                  isActive
                    ? "bg-blue-50 text-blue-700 shadow-sm ring-1 ring-blue-600/10"
                    : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                )
              }
            >
              <item.icon
                className={clsx("mr-3 h-5 w-5 flex-shrink-0 transition-colors", "text-current opacity-70 group-hover:opacity-100")}
                aria-hidden="true"
              />
              {item.name}
            </NavLink>
          ))}
        </nav>
        
        {/* Footer Area */}
        <div className="border-t border-gray-200 p-4">
          <button className="group flex w-full items-center rounded-lg px-3 py-2.5 text-sm font-semibold text-gray-600 transition-all duration-200 hover:bg-red-50 hover:text-red-700">
            <LogOut className="mr-3 h-5 w-5 flex-shrink-0 opacity-70 group-hover:opacity-100" aria-hidden="true" />
            Logout
          </button>
        </div>
      </aside>
    </>
  );
};
