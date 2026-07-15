import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { LoadingSpinner } from '../LoadingSpinner';
import { ErrorState } from '../ErrorState';
import { EmptyState } from '../EmptyState';

describe('Shared State Components', () => {
  describe('LoadingSpinner', () => {
    it('renders with the default accessible message', () => {
      render(<LoadingSpinner />);
      // We look for the visible message and the hidden screen-reader label
      expect(screen.getByText('Loading...')).toBeInTheDocument();
      expect(screen.getByRole('status')).toBeInTheDocument();
    });

    it('renders a custom message when provided', () => {
      render(<LoadingSpinner message="Aggregating metrics..." />);
      expect(screen.getByText('Aggregating metrics...')).toBeInTheDocument();
    });

    it('applies full height classes if requested', () => {
      const { container } = render(<LoadingSpinner fullHeight />);
      expect(container.firstChild).toHaveClass('h-full min-h-[400px]');
    });
  });

  describe('ErrorState', () => {
    it('renders the default error title', () => {
      render(<ErrorState />);
      expect(screen.getByText('An Error Occurred')).toBeInTheDocument();
    });

    it('renders the retry button only if the callback is provided', () => {
      const { rerender } = render(<ErrorState />);
      // Should not exist
      expect(screen.queryByRole('button', { name: /try again/i })).not.toBeInTheDocument();

      const retryMock = vi.fn();
      rerender(<ErrorState onRetry={retryMock} />);
      // Now it should exist
      const btn = screen.getByRole('button', { name: /try again/i });
      expect(btn).toBeInTheDocument();
    });

    it('fires the retry callback on click', () => {
      const retryMock = vi.fn();
      render(<ErrorState onRetry={retryMock} />);
      fireEvent.click(screen.getByRole('button', { name: /try again/i }));
      expect(retryMock).toHaveBeenCalledOnce();
    });
  });

  describe('EmptyState', () => {
    it('renders title and description texts', () => {
      render(<EmptyState title="No Employees Found" description="Try adjusting your filters." />);
      expect(screen.getByText('No Employees Found')).toBeInTheDocument();
      expect(screen.getByText('Try adjusting your filters.')).toBeInTheDocument();
    });

    it('renders the custom injected action component', () => {
      render(
        <EmptyState 
          title="Empty" 
          description="Empty" 
          action={<button>Create Employee</button>} 
        />
      );
      expect(screen.getByRole('button', { name: /create employee/i })).toBeInTheDocument();
    });
  });
});
