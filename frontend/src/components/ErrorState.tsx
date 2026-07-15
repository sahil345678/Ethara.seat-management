import { AlertTriangle, RefreshCcw } from 'lucide-react';
import clsx from 'clsx';

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  className?: string;
}

export const ErrorState = ({ 
  title = 'An Error Occurred', 
  message = 'Something went wrong while fetching data. Please try again.', 
  onRetry,
  className 
}: ErrorStateProps) => {
  return (
    <div className={clsx("flex flex-col items-center justify-center rounded-xl border border-red-200 bg-red-50 p-8 text-center text-red-800 shadow-sm", className)}>
      <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-red-100">
        <AlertTriangle className="h-7 w-7 text-red-600" aria-hidden="true" />
      </div>
      <h3 className="mb-2 text-lg font-bold tracking-tight">{title}</h3>
      <p className="mb-6 text-sm text-red-700 max-w-sm leading-relaxed">{message}</p>
      
      {onRetry && (
        <button 
          onClick={onRetry} 
          className="inline-flex items-center justify-center rounded-lg bg-red-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-all hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:ring-offset-red-50"
        >
          <RefreshCcw className="mr-2 h-4 w-4" />
          Try Again
        </button>
      )}
    </div>
  );
};
