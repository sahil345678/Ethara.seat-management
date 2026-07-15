export type EmployeeStatus = 'ACTIVE' | 'INACTIVE' | 'ON_LEAVE' | 'TERMINATED';
export type ProjectStatus = 'ACTIVE' | 'COMPLETED' | 'ON_HOLD' | 'CANCELLED';
export type SeatStatus = 'AVAILABLE' | 'OCCUPIED' | 'RESERVED' | 'MAINTENANCE';
export type AllocationStatus = 'ACTIVE' | 'RELEASED' | 'PENDING';

export interface PaginationMeta {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  meta: PaginationMeta;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  manager_name?: string;
  status: ProjectStatus;
  created_at: string;
  updated_at: string;
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
  updated_at: string;
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
  created_at: string;
  updated_at: string;
}

export interface DashboardSummary {
  total_employees: number;
  total_seats: number;
  available_seats: number;
  occupied_seats: number;
  reserved_seats: number;
  pending_allocations: number;
  occupancy_rate: number;
}

export interface ProjectUtilization {
  project_id?: string;
  project_name: string;
  allocated_seats: number;
}

export interface FloorUtilization {
  floor: number;
  total_seats: number;
  occupied_seats: number;
  available_seats: number;
}

export interface AiQueryRequest {
  query: string;
}

export interface AiQueryResponse {
  answer: string;
  data?: any;
}
