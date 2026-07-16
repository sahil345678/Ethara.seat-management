"""AI Assistant Service with Gemini Integration and Fallback Logic."""

import json
import logging
import re
from typing import Any

from app.core.config import get_settings
from app.core.enums import AllocationStatus, SeatStatus
from app.services.allocation_service import AllocationService
from app.services.dashboard_service import DashboardService
from app.services.employee_service import EmployeeService
from app.services.project_service import ProjectService
from app.services.seat_service import SeatService

logger = logging.getLogger(__name__)
settings = get_settings()

HAS_GEMINI = False
try:
    import google.generativeai as genai
    HAS_GEMINI = True
    if settings.GEMINI_API_KEY:
        genai.configure(api_key=settings.GEMINI_API_KEY)
except ImportError:
    pass


class AiService:
    """Core AI Service connecting natural language queries to business logic.
    
    Implements a resilient query router that prefers the Gemini API for 
    advanced intent extraction, but automatically falls back to a robust 
    Regex-based keyword parser if the API fails, is not configured, or hits rate limits.
    """

    def __init__(
        self,
        employee_service: EmployeeService,
        project_service: ProjectService,
        seat_service: SeatService,
        dashboard_service: DashboardService,
        allocation_service: AllocationService,
    ) -> None:
        self.emp_svc = employee_service
        self.proj_svc = project_service
        self.seat_svc = seat_service
        self.dash_svc = dashboard_service
        self.alloc_svc = allocation_service

        self.model = None
        if HAS_GEMINI and settings.GEMINI_API_KEY:
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    def process_query(self, query: str) -> str:
        """Process a natural language query and return a human-readable string."""
        logger.info(f"Processing AI query: '{query}'")

        # 1. Attempt Gemini Intent Extraction
        intent, params = self._parse_intent_gemini(query)

        # 2. Fallback to Regex Parser
        if not intent:
            logger.info("Falling back to regex keyword parser.")
            intent, params = self._parse_intent_fallback(query)

        # 3. Handle Unknown / General Questions
        if not intent:
            if self.model:
                try:
                    logger.info("No specific intent matched. Using Gemini with live context for general Q&A.")
                    # Fetch live context
                    summary = self.dash_svc.get_summary()
                    floor_util = self.dash_svc.get_floor_utilization()
                    proj_util = self.dash_svc.get_project_utilization()
                    
                    context = f"""
                    LIVE OFFICE METRICS:
                    Total Employees: {summary.total_employees}
                    Total Seats: {summary.total_seats}
                    Available Seats: {summary.available_seats}
                    Occupied Seats: {summary.occupied_seats}
                    Reserved Seats: {summary.reserved_seats}
                    Maintenance Seats: {summary.maintenance_seats}
                    Pending Allocations: {summary.pending_allocation}
                    Occupancy Rate: {summary.occupancy_rate:.1f}%
                    
                    FLOOR UTILIZATION:
                    {chr(10).join([f"Floor {f.floor}: {f.occupied_seats}/{f.total_seats} occupied, {f.available} available" for f in floor_util])}
                    
                    TOP PROJECTS BY SEATS:
                    {chr(10).join([f"{p.project_name}: {p.allocated_seats} seats, {p.employee_count} employees" for p in proj_util[:15]])}
                    """
                    
                    prompt = f"""
                    You are Ethara's intelligent office seat management AI assistant.
                    The user asked: "{query}"
                    
                    Answer their question in a friendly, concise, and professional tone using ONLY the following live system context.
                    If the answer cannot be determined from this context, politely explain that you don't have that specific data, but offer a related metric from the context.
                    
                    Context:
                    {context}
                    """
                    response = self.model.generate_content(prompt)
                    return response.text.strip()
                except Exception as e:
                    logger.error(f"Gemini general context fallback failed: {e}")

            return (
                "I couldn't understand your request. Try asking something like: "
                "'What is the total occupancy rate?', 'Which project uses the most seats?', or 'Where is John seated?'"
            )

        # 4. Route and Execute Specific Intent
        logger.info(f"Executing intent '{intent}' with params {params}")
        result = self._execute_intent(intent, params)
        
        # 5. Make the specific intent response sound more natural using Gemini if available
        if self.model:
            try:
                prompt = f"""
                You are Ethara's friendly AI office assistant. 
                The user asked: "{query}"
                I have retrieved the raw data answer: "{result}"
                
                Rewrite this raw answer into a friendly, natural, and concise response. 
                Do NOT add any information that is not present in the raw answer.
                """
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception:
                return result
                
        return result

    def _parse_intent_gemini(self, query: str) -> tuple[str | None, dict[str, Any]]:
        """Use Gemini to extract structured intent."""
        if not self.model:
            return None, {}

        prompt = f"""
        You are an intelligent intent parser for an office seat allocation system.
        Analyze the user's query and extract the intent and parameters.

        Query: "{query}"

        Allowed Intents and parameters:
        - LOCATE_EMPLOYEE (param: name) e.g., "Where is John seated?", "Where is my seat?" (assume 'my' means finding the name if provided, else return 'me')
        - EMPLOYEE_PROJECT (param: name) e.g., "Which project is Alice assigned to?"
        - AVAILABLE_SEATS_FLOOR (param: floor_number) e.g., "Available seats on Floor 2"
        - AVAILABLE_SEATS_ZONE (param: zone_name) e.g., "Available seats in Zone A"
        - NEARBY_EMPLOYEES (param: name) e.g., "Who sits near Bob?"
        - UTILIZATION_FLOOR (no params) e.g., "Seat utilization by floor"
        - UTILIZATION_PROJECT (no params) e.g., "Seat utilization by project"
        - ALLOCATE_SEAT (no params) e.g., "Allocate a seat for a new employee"
        - PENDING_ALLOCATIONS (no params) e.g., "Pending seat allocations"

        Respond ONLY with a valid JSON object matching exactly this format:
        {{"intent": "INTENT_NAME", "params": {{"key": "value"}}}}
        If no intent matches, return an empty JSON object: {{}}.
        """
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3]
            elif text.startswith("```"):
                text = text[3:-3]

            data = json.loads(text.strip())
            return data.get("intent"), data.get("params", {})
        except Exception as e:
            logger.warning(f"Gemini API parsing failed: {e}")
            return None, {}

    def _parse_intent_fallback(self, query: str) -> tuple[str | None, dict[str, Any]]:
        """Robust Regex-based keyword parser for handling complex queries without Gemini."""
        q = query.lower().strip()

        # 1. Utilization
        if "utilization" in q or "occupancy" in q or "capacity" in q:
            if "project" in q or "team" in q:
                return "UTILIZATION_PROJECT", {}
            return "UTILIZATION_FLOOR", {}

        # 2. Pending Allocations
        if any(w in q for w in ["pending", "queue", "waiting"]):
            return "PENDING_ALLOCATIONS", {}

        # 3. Allocate / Book Seat
        if any(w in q for w in ["allocate", "book", "reserve", "new seat"]) and "project" not in q:
            return "ALLOCATE_SEAT", {}
        if "assign" in q and "seat" in q:
            return "ALLOCATE_SEAT", {}

        # 4. Available Seats Zone
        if m := re.search(r"(?:zone)\s+([a-z]+)", q):
            if any(w in q for w in ["available", "free", "empty", "space", "open"]):
                return "AVAILABLE_SEATS_ZONE", {"zone_name": m.group(1).strip().upper()}

        # 5. Available Seats Floor
        if m := re.search(r"(?:floor)\s*(\d+)", q):
            return "AVAILABLE_SEATS_FLOOR", {"floor_number": int(m.group(1))}

        # 6. Generic Fallbacks for Availability
        if any(w in q for w in ["available", "free", "empty", "space", "open"]) and "seat" in q:
            return "AVAILABLE_SEATS_FLOOR", {"floor_number": None}

        # 7. Nearby Employees
        if m := re.search(r"(?:near|next to|close to|around)\s+(.*)", q):
            name = re.sub(r"[^\w\s]", "", m.group(1)).strip()
            if name: return "NEARBY_EMPLOYEES", {"name": name}

        # 8. Locate Employee
        if m := re.search(r"(?:where is|where does|find|seat for|locate)\s+(.*?)(?:\s+sit|\s+seated|\s+seat|$)", q):
            name = m.group(1).replace("my", "me").replace("is", "").strip()
            if not any(w in name for w in ["open", "space", "available", "free", "empty", "seat"]):
                if name: return "LOCATE_EMPLOYEE", {"name": name}
        if "my seat" in q:
            return "LOCATE_EMPLOYEE", {"name": "me"}

        # 9. Employee Project
        if m := re.search(r"(?:project|team).*?(?:for|is)\s+(.*?)(?:\s+assigned|\s+on|$)", q):
            return "EMPLOYEE_PROJECT", {"name": m.group(1).replace("assigned", "").strip()}
        if m := re.search(r"(.*?)(?:'s)?\s+(?:project|team)", q):
            name = m.group(1).replace("what", "").replace("which", "").strip()
            if name and name not in ["a", "the", "any"]:
                return "EMPLOYEE_PROJECT", {"name": name}
            
        # 10. Bare Digits (Follow-up for Floor)
        if q.isdigit():
            return "AVAILABLE_SEATS_FLOOR", {"floor_number": int(q)}

        return None, {}

    def _execute_intent(self, intent: str, params: dict[str, Any]) -> str:
        """Route the intent to the respective internal handler."""
        try:
            if intent == "LOCATE_EMPLOYEE":
                return self._handle_locate_employee(params.get("name"))
            if intent == "EMPLOYEE_PROJECT":
                return self._handle_employee_project(params.get("name"))
            if intent == "AVAILABLE_SEATS_FLOOR":
                return self._handle_available_floor(params.get("floor_number"))
            if intent == "AVAILABLE_SEATS_ZONE":
                return self._handle_available_zone(params.get("zone_name"))
            if intent == "NEARBY_EMPLOYEES":
                return self._handle_nearby_employees(params.get("name"))
            if intent == "UTILIZATION_FLOOR":
                return self._handle_utilization_floor()
            if intent == "UTILIZATION_PROJECT":
                return self._handle_utilization_project()
            if intent == "ALLOCATE_SEAT":
                return (
                    "To allocate a seat, please navigate to the Seat Allocation "
                    "Dashboard or make a direct API call to POST /api/v1/seats/allocate."
                )
            if intent == "PENDING_ALLOCATIONS":
                return self._handle_pending_allocations()
            return "Sorry, I understand what you want but don't know how to execute it yet."
        except Exception as e:
            logger.error(f"Error executing AI intent '{intent}': {e}")
            return "An internal error occurred while fetching the requested data."

    def _handle_locate_employee(self, name: str) -> str:
        if not name or name.lower() == "me":
            return "Please specify the full name of the employee."
            
        emps, _ = self.emp_svc.list_employees(search=name)
        if not emps:
            return f"I couldn't find any employee matching '{name}'."
            
        emp = emps[0]
        alloc = self.alloc_svc.repo.get_active_for_employee(emp.id)
        if not alloc or not alloc.seat:
            return f"{emp.name} does not currently have an active seat allocation."
            
        s = alloc.seat
        return f"{emp.name} is seated on Floor {s.floor}, Zone {s.zone}, Bay {s.bay}, Seat {s.seat_number}."

    def _handle_employee_project(self, name: str) -> str:
        if not name:
            return "Please specify the employee name."
            
        emps, _ = self.emp_svc.list_employees(search=name)
        if not emps:
            return f"I couldn't find any employee matching '{name}'."
            
        emp = emps[0]
        if not emp.project:
            return f"{emp.name} is not currently assigned to any project."
            
        return f"{emp.name} is currently assigned to the '{emp.project.name}' project."

    def _handle_available_floor(self, floor: int) -> str:
        if floor is None:
            return "Please specify a valid floor number."
            
        seats, total = self.seat_svc.list_seats(floor=int(floor), status=SeatStatus.AVAILABLE, limit=10)
        if total == 0:
            return f"There are no available seats on Floor {floor}."
            
        available_labels = ", ".join([s.seat_number for s in seats])
        return f"There are {total} available seats on Floor {floor}. Here are some of them: {available_labels}."

    def _handle_available_zone(self, zone: str) -> str:
        if not zone:
            return "Please specify a valid zone."
            
        seats, total = self.seat_svc.list_seats(zone=str(zone).upper(), status=SeatStatus.AVAILABLE, limit=10)
        if total == 0:
            return f"There are no available seats in Zone {zone.upper()}."
            
        available_labels = ", ".join([s.seat_number for s in seats])
        return f"There are {total} available seats in Zone {zone.upper()}. Here are some of them: {available_labels}."

    def _handle_nearby_employees(self, name: str) -> str:
        if not name:
            return "Please specify the employee name."
            
        emps, _ = self.emp_svc.list_employees(search=name)
        if not emps:
            return f"I couldn't find any employee matching '{name}'."
            
        emp = emps[0]
        alloc = self.alloc_svc.repo.get_active_for_employee(emp.id)
        if not alloc or not alloc.seat:
            return f"{emp.name} does not have an active seat allocation, so I cannot find nearby teammates."
            
        s = alloc.seat
        # Find active allocations in the same floor and zone
        allocs, _ = self.alloc_svc.list_allocations(status=AllocationStatus.ACTIVE, limit=200)
        nearby = []
        for a in allocs:
            if a.employee_id != emp.id and a.seat and a.seat.floor == s.floor and a.seat.zone == s.zone:
                if a.employee:
                    nearby.append(a.employee.name)
                    
        if not nearby:
            return f"There is currently no one else seated near {emp.name} in Floor {s.floor}, Zone {s.zone}."
            
        return f"Employees seated near {emp.name} include: {', '.join(nearby[:5])}."

    def _handle_utilization_floor(self) -> str:
        data = self.dash_svc.get_floor_utilization()
        if not data:
            return "No floor utilization data is currently available."
            
        lines = ["Seat Utilization by Floor:"]
        for f in data:
            rate = (f.occupied_seats / f.total_seats * 100) if f.total_seats else 0
            lines.append(f"- Floor {f.floor}: {f.occupied_seats}/{f.total_seats} occupied ({rate:.1f}%)")
        return "\n".join(lines)

    def _handle_utilization_project(self) -> str:
        data = self.dash_svc.get_project_utilization()
        if not data:
            return "No project utilization data is currently available."
            
        lines = ["Seat Utilization by Project (Top 10):"]
        for p in data[:10]:
            lines.append(f"- {p.project_name}: {p.allocated_seats} active seats")
        return "\n".join(lines)

    def _handle_pending_allocations(self) -> str:
        summary = self.dash_svc.get_summary()
        return f"There are currently {summary.pending_allocation} employees pending seat allocation in the system."
