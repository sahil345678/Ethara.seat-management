import { ReactNode } from 'react';
import { FileQuestion } from 'lucide-react';
import clsx from 'clsx';

interface EmptyStateProps {
  title: string;
  description: string;
  icon?: ReactNode;
  action?: ReactNode;
  className?: string;
}

export const EmptyState = ({ 
  title, 
  description, 
  icon, 
  action,
  className 
}: EmptyStateProps) => {
  return (
    <div className={clsx("flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-200 bg-gray-50/50 p-12 text-center transition-colors hover:bg-gray-50", className)}>
      <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-white shadow-sm ring-1 ring-gray-900/5 text-gray-500">
        {icon || <FileQuestion className="h-8 w-8 text-gray-400" aria-hidden="true" />}
      </div>
      <h3 className="mb-1.5 text-lg font-bold text-gray-900 tracking-tight">{title}</h3>
      <p className="mb-6 text-sm text-gray-500 max-w-sm leading-relaxed">{description}</p>
      {action && (
        <div className="mt-2">
          {action}
        </div>
      )}
    </div>
  );
};
