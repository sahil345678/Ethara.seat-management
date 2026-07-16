import { useState, useRef, useEffect } from 'react';
import { Menu, Bell, UserCircle, CheckCircle2, AlertCircle, Info, Trash2 } from 'lucide-react';
import { useNotification } from '../contexts/NotificationContext';
import { Link } from 'react-router-dom';
import clsx from 'clsx';

interface NavbarProps {
  onMenuClick: () => void;
}

export const Navbar = ({ onMenuClick }: NavbarProps) => {
  const { notifications, unreadCount, markAsRead, markAllAsRead } = useNotification();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

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
          <div className="relative" ref={dropdownRef}>
            <button 
              className={clsx(
                "relative p-2 rounded-full transition-all duration-300",
                isDropdownOpen ? "bg-brand-100 text-brand-700" : "text-surface-400 hover:text-brand-600 hover:bg-brand-50"
              )}
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            >
              <span className="sr-only">View notifications</span>
              <Bell className="h-5 w-5" aria-hidden="true" />
              {unreadCount > 0 && (
                <span className="absolute top-1.5 right-1.5 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[9px] font-bold text-white border-2 border-white shadow-sm">
                  {unreadCount > 9 ? '9+' : unreadCount}
                </span>
              )}
            </button>

            {isDropdownOpen && (
              <div className="absolute right-0 mt-3 w-80 sm:w-96 rounded-xl bg-white shadow-2xl ring-1 ring-black/5 animate-in slide-in-from-top-2 fade-in duration-200 z-50">
                <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100">
                  <h3 className="text-sm font-bold text-gray-900">Notifications</h3>
                  {unreadCount > 0 && (
                    <button 
                      onClick={() => markAllAsRead()}
                      className="text-xs font-semibold text-brand-600 hover:text-brand-800"
                    >
                      Mark all as read
                    </button>
                  )}
                </div>
                
                <div className="max-h-[400px] overflow-y-auto">
                  {notifications.length === 0 ? (
                    <div className="p-6 text-center text-sm text-gray-500 flex flex-col items-center">
                      <Bell className="h-8 w-8 text-gray-300 mb-2" />
                      <p>You're all caught up!</p>
                    </div>
                  ) : (
                    <div className="divide-y divide-gray-100">
                      {notifications.map((notif) => (
                        <div 
                          key={notif.id} 
                          className={clsx(
                            "p-4 transition-colors hover:bg-gray-50",
                            !notif.read && "bg-brand-50/30"
                          )}
                          onClick={() => {
                            if (!notif.read) markAsRead(notif.id);
                          }}
                        >
                          <div className="flex gap-3">
                            <div className="mt-0.5">
                              {notif.type === 'success' && <CheckCircle2 className="h-5 w-5 text-green-500" />}
                              {notif.type === 'error' && <AlertCircle className="h-5 w-5 text-red-500" />}
                              {notif.type === 'info' && <Info className="h-5 w-5 text-blue-500" />}
                              {notif.type === 'warning' && <AlertCircle className="h-5 w-5 text-orange-500" />}
                            </div>
                            <div className="flex-1">
                              <p className={clsx("text-sm font-semibold", !notif.read ? "text-gray-900" : "text-gray-700")}>
                                {notif.title}
                              </p>
                              <p className="text-sm text-gray-500 mt-0.5 leading-snug">{notif.description}</p>
                              <p className="text-xs text-gray-400 mt-2 font-medium">
                                {notif.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                              </p>
                            </div>
                            {!notif.read && (
                              <div className="flex-shrink-0 flex items-center">
                                <span className="h-2 w-2 rounded-full bg-brand-500"></span>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
          
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
