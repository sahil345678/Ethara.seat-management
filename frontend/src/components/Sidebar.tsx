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
          className="fixed inset-0 z-20 bg-surface-900/40 backdrop-blur-sm lg:hidden transition-opacity"
          onClick={onClose}
          aria-hidden="true"
        />
      )}
      
      {/* Sidebar Container */}
      <aside
        className={clsx(
          "fixed inset-y-0 left-0 z-30 flex w-72 flex-col glass-panel border-r-0 transition-transform duration-300 ease-in-out lg:static lg:flex lg:translate-x-0 shadow-premium lg:shadow-none lg:border-r lg:border-surface-200/60",
          isOpen ? "translate-x-0 flex" : "-translate-x-full"
        )}
      >
        {/* Brand Header */}
        <div className="flex h-20 flex-shrink-0 items-center justify-between border-b border-surface-200/60 px-6 mt-2">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-brand-500 to-accent-DEFAULT flex items-center justify-center shadow-md">
              <span className="text-white font-bold text-lg">E</span>
            </div>
            <span className="text-2xl font-display font-bold bg-clip-text text-transparent bg-gradient-to-r from-surface-900 to-surface-600 tracking-tight">Ethara.</span>
          </div>
          <button onClick={onClose} className="lg:hidden p-1.5 rounded-lg text-surface-500 hover:text-surface-900 hover:bg-surface-100 transition-colors">
            <X size={20} aria-label="Close sidebar" />
          </button>
        </div>
        
        {/* Navigation Links */}
        <nav className="flex-1 space-y-2 overflow-y-auto p-4 mt-4">
          {navItems.map((item) => (
            <NavLink
              key={item.name}
              to={item.path}
              onClick={() => {
                if (window.innerWidth < 1024) onClose();
              }}
              className={({ isActive }) =>
                clsx(
                  "group flex items-center rounded-xl px-4 py-3 text-sm font-medium transition-all duration-300",
                  isActive
                    ? "bg-brand-50 text-brand-700 shadow-sm ring-1 ring-brand-500/20 shadow-brand-100/50"
                    : "text-surface-600 hover:bg-surface-100/80 hover:text-surface-900"
                )
              }
            >
              <item.icon
                className={clsx("mr-3 h-5 w-5 flex-shrink-0 transition-all duration-300", "group-hover:scale-110", "text-current opacity-70 group-hover:opacity-100")}
                aria-hidden="true"
              />
              {item.name}
            </NavLink>
          ))}
        </nav>
        
        {/* Footer Area */}
        <div className="border-t border-surface-200/60 p-4 mb-2">
          <button className="group flex w-full items-center rounded-xl px-4 py-3 text-sm font-medium text-surface-600 transition-all duration-300 hover:bg-red-50 hover:text-red-600">
            <LogOut className="mr-3 h-5 w-5 flex-shrink-0 opacity-70 group-hover:opacity-100 transition-transform duration-300 group-hover:-translate-x-1" aria-hidden="true" />
            Logout
          </button>
        </div>
      </aside>
    </>
  );
};
