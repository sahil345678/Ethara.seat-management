import { Menu, Bell, UserCircle } from 'lucide-react';

interface NavbarProps {
  onMenuClick: () => void;
}

export const Navbar = ({ onMenuClick }: NavbarProps) => {
  return (
    <header className="sticky top-0 z-10 flex h-16 flex-shrink-0 items-center justify-between border-b border-gray-200 bg-white/80 backdrop-blur-md px-4 sm:px-6 lg:px-8 shadow-sm">
      <div className="flex flex-1 items-center justify-between lg:justify-end">
        {/* Mobile menu button */}
        <button
          type="button"
          className="-ml-2.5 rounded-lg p-2.5 text-gray-600 lg:hidden hover:bg-gray-100 transition-colors"
          onClick={onMenuClick}
        >
          <span className="sr-only">Open sidebar</span>
          <Menu className="h-6 w-6" aria-hidden="true" />
        </button>
        
        {/* Top Right Actions */}
        <div className="flex items-center space-x-5">
          <button className="relative p-1.5 rounded-full text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors">
            <span className="sr-only">View notifications</span>
            <Bell className="h-5 w-5" aria-hidden="true" />
            <span className="absolute top-1.5 right-1.5 flex h-2 w-2 rounded-full bg-red-500 shadow-sm"></span>
          </button>
          
          <div className="flex items-center space-x-3 border-l border-gray-200 pl-5">
            <UserCircle className="h-8 w-8 text-blue-600 opacity-90" aria-hidden="true" />
            <div className="hidden sm:block text-sm text-left">
              <p className="font-semibold text-gray-900 leading-tight">Admin User</p>
              <p className="text-gray-500 text-xs mt-0.5">admin@ethara.com</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
