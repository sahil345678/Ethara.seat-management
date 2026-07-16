import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import clsx from 'clsx';
import { CheckCircle2, AlertCircle, X, Info } from 'lucide-react';

export type ToastType = 'success' | 'error' | 'info';

export interface ToastMessage {
  id: string;
  message: string;
  type: ToastType;
}

interface ToastContextType {
  addToast: (message: string, type: ToastType) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const addToast = useCallback((message: string, type: ToastType) => {
    setToasts((current) => {
      // Prevent exact duplicates within a short timeframe
      if (current.some(t => t.message === message)) return current;
      
      const newToast: ToastMessage = { id: Math.random().toString(36).substring(2, 9), message, type };
      return [...current, newToast];
    });
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts((current) => current.filter((toast) => toast.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ addToast }}>
      {children}
      <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
        {toasts.map((toast) => (
          <ToastItem key={toast.id} toast={toast} onRemove={removeToast} />
        ))}
      </div>
    </ToastContext.Provider>
  );
};

const ToastItem = ({ toast, onRemove }: { toast: ToastMessage; onRemove: (id: string) => void }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onRemove(toast.id);
    }, 4000);
    return () => clearTimeout(timer);
  }, [toast.id, onRemove]);

  return (
    <div 
      className={clsx(
        "flex items-center gap-3 min-w-[300px] max-w-sm rounded-xl p-4 shadow-lg border animate-in slide-in-from-right-8 fade-in duration-300",
        toast.type === 'success' && "bg-green-50 border-green-200 text-green-900",
        toast.type === 'error' && "bg-red-50 border-red-200 text-red-900",
        toast.type === 'info' && "bg-blue-50 border-blue-200 text-blue-900",
      )}
    >
      {toast.type === 'success' && <CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0" />}
      {toast.type === 'error' && <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0" />}
      {toast.type === 'info' && <Info className="h-5 w-5 text-blue-600 flex-shrink-0" />}
      
      <p className="text-sm font-semibold flex-1 leading-snug">{toast.message}</p>
      
      <button 
        onClick={() => onRemove(toast.id)}
        className="text-gray-400 hover:text-gray-600 focus:outline-none transition-colors rounded-full hover:bg-black/5 p-1"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
};
