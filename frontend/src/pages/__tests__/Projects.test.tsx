import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { Projects } from '../Projects';
import * as hooks from '../../hooks/useProjects';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../../hooks/useProjects');

describe('Projects Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(hooks.useProjects).mockReturnValue({ data: null, isLoading: true } as any);
    vi.mocked(hooks.useProjectEmployees).mockReturnValue({ data: null, isLoading: true } as any);
  });

  const renderComponent = () => render(<BrowserRouter><Projects /></BrowserRouter>);

  it('renders loading state initially', () => {
    renderComponent();
    expect(screen.getByText(/loading projects/i)).toBeInTheDocument();
  });

  it('renders project rows successfully', () => {
    vi.mocked(hooks.useProjects).mockReturnValue({
      data: {
        data: [{ id: '1', name: 'Alpha Project', description: 'Secret', manager_name: 'Alice', status: 'ACTIVE', created_at: '2025-01-01' }],
        meta: { total: 1, page: 1, total_pages: 1 }
      },
      isLoading: false
    } as any);
    
    renderComponent();
    
    expect(screen.getByText('Alpha Project')).toBeInTheDocument();
    expect(screen.getByText('Alice')).toBeInTheDocument();
  });

  it('expands a project row to show assigned employees when clicked', () => {
    vi.mocked(hooks.useProjects).mockReturnValue({
      data: {
        data: [{ id: '1', name: 'Alpha Project', status: 'ACTIVE', created_at: '2025-01-01' }],
        meta: { total: 1, page: 1, total_pages: 1 }
      },
      isLoading: false
    } as any);
    
    // Setup nested employee mock
    vi.mocked(hooks.useProjectEmployees).mockReturnValue({
      data: {
        data: [{ id: '100', name: 'Bob TeamMember' }],
        meta: { total: 1, page: 1, total_pages: 1 }
      },
      isLoading: false
    } as any);
    
    renderComponent();
    
    // Initially nested row is hidden
    expect(screen.queryByText('Bob TeamMember')).not.toBeInTheDocument();
    
    // Click row to expand
    fireEvent.click(screen.getByText('Alpha Project'));
    
    // The team member from useProjectEmployees should now be in the DOM
    expect(screen.getByText('Bob TeamMember')).toBeInTheDocument();
  });
});
