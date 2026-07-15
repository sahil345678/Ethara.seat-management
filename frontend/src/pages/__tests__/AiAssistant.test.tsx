import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { AiAssistant } from '../AiAssistant';
import * as hooks from '../../hooks/useAi';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../../hooks/useAi');

describe('AI Assistant Page', () => {
  let mutateAsyncMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    vi.clearAllMocks();
    mutateAsyncMock = vi.fn();
    // Prevent JSDom scrollIntoView from crashing
    window.HTMLElement.prototype.scrollIntoView = vi.fn();

    vi.mocked(hooks.useAiQuery).mockReturnValue({
      mutateAsync: mutateAsyncMock,
      isPending: false
    } as any);
  });

  const renderComponent = () => render(<BrowserRouter><AiAssistant /></BrowserRouter>);

  it('renders the initial greeting message', () => {
    renderComponent();
    expect(screen.getByText(/hello! i am the ethara ai assistant/i)).toBeInTheDocument();
  });

  it('allows user to send a message and renders the AI response', async () => {
    mutateAsyncMock.mockResolvedValueOnce({ answer: 'John is seated on Floor 2.' });
    renderComponent();
    
    const input = screen.getByPlaceholderText(/ask/i);
    const form = input.closest('form')!;
    
    fireEvent.change(input, { target: { value: 'Where is John?' } });
    fireEvent.submit(form);
    
    // User message should appear immediately
    expect(screen.getByText('Where is John?')).toBeInTheDocument();
    
    // Wait for mock API resolve
    await waitFor(() => {
      expect(screen.getByText('John is seated on Floor 2.')).toBeInTheDocument();
    });
    
    expect(mutateAsyncMock).toHaveBeenCalledWith('Where is John?');
  });

  it('handles backend exceptions and displays an error bubble', async () => {
    mutateAsyncMock.mockRejectedValueOnce(new Error('Network disconnected'));
    renderComponent();
    
    const input = screen.getByPlaceholderText(/ask/i);
    fireEvent.change(input, { target: { value: 'Crash' } });
    fireEvent.submit(input.closest('form')!);
    
    await waitFor(() => {
      expect(screen.getByText('Network disconnected')).toBeInTheDocument();
    });
  });
});
