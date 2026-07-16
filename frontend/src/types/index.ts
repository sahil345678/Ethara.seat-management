export type EmployeeStatus = 'Active' | 'Inactive';
export type ProjectStatus = 'Active' | 'Completed';
export type SeatStatus = 'Available' | 'Occupied' | 'Reserved' | 'Maintenance';
export type AllocationStatus = 'Active' | 'Released';

export interface PaginationMeta {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  manager_name?: string;
  status: ProjectStatus;
  created_at: string;
}

export interface Employee {
  id: string;
  employee_code: string;
  name: string;
  email: string;
  department: string;
  role: string;
  joining_date: string;
  status: EmployeeStatus;
  project_id?: string;
  project?: Project;
  created_at: string;
  updated_at: string;
}

export interface Seat {
  id: string;
  floor: number;
  zone: string;
  bay: string;
  seat_number: string;
  status: SeatStatus;
  created_at: string;
}

export interface SeatAllocation {
  id: string;
  employee_id: string;
  seat_id: string;
  project_id?: string;
  allocation_status: AllocationStatus;
  allocation_date: string;
  released_date?: string;
  employee?: Employee;
  seat?: Seat;
  project?: Project;
}

export interface DashboardSummary {
  total_employees: number;
  total_seats: number;
  available_seats: number;
  occupied_seats: number;
  reserved_seats: number;
  maintenance_seats: number;
  pending_allocation: number;
  occupancy_rate: number;
}

export interface ProjectUtilization {
  project_id?: string;
  project_name: string;
  allocated_seats: number;
  employee_count: number;
}

export interface FloorUtilization {
  floor: number;
  total_seats: number;
  occupied: number;
  available: number;
  reserved: number;
  maintenance: number;
}

export interface AiQueryRequest {
  query: string;
}

export interface AiQueryResponse {
  answer: string;
  data?: any;
}

