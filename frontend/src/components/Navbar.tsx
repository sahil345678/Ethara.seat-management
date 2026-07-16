import { Menu, Bell, UserCircle } from 'lucide-react';

interface NavbarProps {
  onMenuClick: () => void;
}

export const Navbar = ({ onMenuClick }: NavbarProps) => {
  return (
    <header className="sticky top-0 z-10 flex h-20 flex-shrink-0 items-center justify-between border-b border-surface-200/60 bg-surface-50/80 backdrop-blur-xl px-4 sm:px-6 lg:px-8 shadow-sm transition-all duration-300">
      <div className="flex flex-1 items-center justify-between lg:justify-end">
        {/* Mobile menu button */}
        <button
          type="button"
          className="-ml-2.5 rounded-lg p-2.5 text-surface-500 lg:hidden hover:bg-surface-200 hover:text-surface-900 transition-colors"
          onClick={onMenuClick}
        >
          <span className="sr-only">Open sidebar</span>
          <Menu className="h-6 w-6" aria-hidden="true" />
        </button>
        
        {/* Top Right Actions */}
        <div className="flex items-center space-x-6">
          <button className="relative p-2 rounded-full text-surface-400 hover:text-brand-600 hover:bg-brand-50 transition-all duration-300">
            <span className="sr-only">View notifications</span>
            <Bell className="h-5 w-5" aria-hidden="true" />
            <span className="absolute top-2 right-2 flex h-2 w-2 rounded-full bg-red-500 shadow-sm animate-pulse-slow border-2 border-white"></span>
          </button>
          
          <div className="flex items-center space-x-3 border-l border-surface-200/60 pl-6">
            <div className="h-9 w-9 rounded-full bg-gradient-to-tr from-brand-500 to-accent-DEFAULT flex items-center justify-center text-white shadow-sm shadow-brand-200">
              <UserCircle className="h-6 w-6" aria-hidden="true" />
            </div>
            <div className="hidden sm:block text-sm text-left">
              <p className="font-semibold text-surface-900 leading-tight">Admin User</p>
              <p className="text-surface-500 text-xs mt-0.5">admin@ethara.com</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
