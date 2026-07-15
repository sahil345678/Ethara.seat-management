# Ethara — End-to-End QA Testing Checklist

This document provides the standard operating procedure for manual Quality Assurance (QA) testing of the Ethara application. It verifies that all business rules strictly established in the Python architecture translate perfectly through the API up to the React frontend.

---

## 1. Backend Core & API Validation
_Verify via Swagger UI (`http://localhost:8000/docs`) or HTTP clients like Postman._

- [ ] **Employee CRUD**
  - [ ] POST `/api/v1/employees/`: Verify successful creation.
  - [ ] POST `/api/v1/employees/`: Verify failure on duplicate email (409 Conflict).
  - [ ] POST `/api/v1/employees/`: Verify failure on duplicate employee code (409 Conflict).
- [ ] **Project CRUD**
  - [ ] POST `/api/v1/projects/`: Verify project creation with active status.
- [ ] **Seat Allocation Engine**
  - [ ] POST `/api/v1/seats/allocate`: Verify manual allocation to an `AVAILABLE` seat transitions it to `OCCUPIED`.
  - [ ] POST `/api/v1/seats/allocate`: Verify attempt to allocate a `RESERVED` seat fails with 400.
  - [ ] POST `/api/v1/seats/allocate`: Verify attempt to allocate an employee who already holds an active allocation fails.
  - [ ] POST `/api/v1/seats/release/{id}`: Verify releasing transitions seat back to `AVAILABLE`.
- [ ] **AI Assistant Router**
  - [ ] POST `/api/v1/ai/query`: Send natural language query ("where is john") and verify structured string response.

---

## 2. Frontend User Interface Validation
_Verify by browsing the Vite application (`http://localhost:5173`)._

### 2.1 Navigation & Responsive Layout
- [ ] Shrink browser to mobile width (<768px). Verify Sidebar transitions into a hidden drawer with a hamburger menu.
- [ ] Verify active NavLink highlighting works when transitioning between pages.

### 2.2 Dashboard
- [ ] Validate the 6 metric cards successfully render numbers without NaN or undefined.
- [ ] Verify the Pie Chart correctly sizes proportionally to Occupied/Available splits.

### 2.3 Employees Directory
- [ ] Type a name into the Search input and hit Enter; verify table updates.
- [ ] Change the Status dropdown filter to "Inactive"; verify table updates.
- [ ] Click "Next" on pagination; verify page 2 fetches and renders smoothly.
- [ ] Click "View" on a row to navigate to `EmployeeDetails`. Verify URL changes to `/employees/:id`.

### 2.4 Projects Page
- [ ] Verify the table renders all projects.
- [ ] Click a Project row to expand the accordion. Verify the `Assigned Team Members` chip list renders.

### 2.5 Seats & Facilities
- [ ] Verify the Grid renders.
- [ ] Filter by Floor 1 and Zone A. Verify the grid shrinks to match parameters.
- [ ] Validate color codes: Teal (Available), Blue (Occupied), Purple (Reserved).

### 2.6 Seat Allocation Wizard
- [ ] Search for an employee and select them.
- [ ] **Manual Workflow:** Select an available seat on the grid. Click "Confirm". Verify success toast and check Dashboard metrics.
- [ ] **Smart Workflow:** Deselect the seat. Click "Confirm" to trigger the backend Proximity Algorithm. Verify success toast.

### 2.7 AI Assistant Chat
- [ ] Submit a message. Verify the loading spinner pulses inside the chat bubble.
- [ ] Ask "Seat utilization by project". Verify the AI responds with data instead of an error.

---

## 3. Resilience & Error States
- [ ] Disconnect the backend terminal (`Ctrl+C` on FastAPI).
- [ ] Refresh the React dashboard. Verify the `ErrorState` component renders cleanly on all charts with a "Try Again" button, instead of a white screen crash.
- [ ] Restart backend, click "Try Again" on the frontend. Verify application recovers instantly without page reload.
