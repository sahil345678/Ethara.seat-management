import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { Employees } from '../Employees';
import * as hooks from '../../hooks/useEmployees';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../../hooks/useEmployees');

describe('Employees Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(hooks.useEmployees).mockReturnValue({ data: null, isLoading: true } as any);
  });

  const renderComponent = () => render(<BrowserRouter><Employees /></BrowserRouter>);

  it('renders loading state initially', () => {
    renderComponent();
    expect(screen.getByText(/loading directory/i)).toBeInTheDocument();
  });

  it('renders ErrorState when API request fails', () => {
    vi.mocked(hooks.useEmployees).mockReturnValue({ isError: true } as any);
    renderComponent();
    expect(screen.getByText(/an error occurred/i)).toBeInTheDocument();
  });

  it('renders EmptyState when API returns 0 employees', () => {
    vi.mocked(hooks.useEmployees).mockReturnValue({ 
      data: { data: [], meta: { total: 0, page: 1, total_pages: 1 } },
      isLoading: false 
    } as any);
    renderComponent();
    expect(screen.getByText(/no employees found/i)).toBeInTheDocument();
  });

  it('renders the employee table correctly when data is provided', () => {
    vi.mocked(hooks.useEmployees).mockReturnValue({
      data: {
        data: [{ id: '1', name: 'John Doe', email: 'john@doe.com', employee_code: 'ETH-123', department: 'Eng', status: 'ACTIVE' }],
        meta: { total: 1, page: 1, total_pages: 1 }
      },
      isLoading: false
    } as any);
    
    renderComponent();
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('ETH-123')).toBeInTheDocument();
    expect(screen.getByText('john@doe.com')).toBeInTheDocument();
  });

  it('triggers a refetch when the search form is submitted', () => {
    const refetchMock = vi.fn();
    vi.mocked(hooks.useEmployees).mockReturnValue({
      data: { data: [], meta: { total: 0, page: 1, total_pages: 1 } },
      isLoading: false,
      refetch: refetchMock
    } as any);
    
    renderComponent();
    
    const searchInput = screen.getByPlaceholderText(/search names or emails/i);
    fireEvent.change(searchInput, { target: { value: 'Jane' } });
    
    // We didn't add a dedicated search button, it triggers on form submit via the input ENTER
    fireEvent.submit(searchInput.closest('form')!);
    
    expect(refetchMock).toHaveBeenCalledOnce();
  });
});
