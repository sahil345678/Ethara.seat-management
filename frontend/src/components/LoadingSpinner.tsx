import { Loader2 } from 'lucide-react';
import clsx from 'clsx';

interface LoadingSpinnerProps {
  className?: string;
  size?: number;
  message?: string;
  fullHeight?: boolean;
}

export const LoadingSpinner = ({ 
  className, 
  size = 32, 
  message = "Loading...", 
  fullHeight = false 
}: LoadingSpinnerProps) => {
  return (
    <div 
      className={clsx(
        'flex flex-col items-center justify-center p-8 text-gray-500', 
        fullHeight ? 'h-full min-h-[400px]' : '',
        className
      )}
      role="status"
    >
      <Loader2 
        className="animate-spin text-blue-600" 
        size={size} 
        aria-hidden="true" 
      />
      {message && (
        <span className="mt-4 text-sm font-medium animate-pulse">{message}</span>
      )}
      <span className="sr-only">Loading indicator</span>
    </div>
  );
};
