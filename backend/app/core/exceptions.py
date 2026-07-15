"""Custom business exception classes.

All domain exceptions inherit from `AppException`, which carries a
`status_code` and `message`.  The global exception handler in
`app.middleware.error_handler` translates these into standardized
JSON error responses.
"""


class AppException(Exception):
    """Base exception for all application-level errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        detail: str | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)


# ── 404 Not Found ────────────────────────────────────────────────────────────


class EmployeeNotFoundError(AppException):
    """Raised when an employee lookup fails."""

    def __init__(self, identifier: str | int) -> None:
        super().__init__(
            message=f"Employee with identifier '{identifier}' not found.",
            status_code=404,
        )


class ProjectNotFoundError(AppException):
    """Raised when a project lookup fails."""

    def __init__(self, identifier: str | int) -> None:
        super().__init__(
            message=f"Project with identifier '{identifier}' not found.",
            status_code=404,
        )


class SeatNotFoundError(AppException):
    """Raised when a seat lookup fails."""

    def __init__(self, identifier: str | int) -> None:
        super().__init__(
            message=f"Seat with identifier '{identifier}' not found.",
            status_code=404,
        )


class NoAvailableSeatsError(AppException):
    """Raised when the allocation engine cannot find any available seat."""

    def __init__(self, context: str = "") -> None:
        msg = "No available seats found"
        if context:
            msg = f"{msg} {context}"
        super().__init__(message=f"{msg}.", status_code=404)


# ── 409 Conflict ─────────────────────────────────────────────────────────────


class DuplicateEmailError(AppException):
    """Raised when an employee email already exists in the system."""

    def __init__(self, email: str) -> None:
        super().__init__(
            message=f"Employee with email '{email}' already exists.",
            status_code=409,
        )


class DuplicateSeatError(AppException):
    """Raised when a seat with the same floor/zone/bay/number already exists."""

    def __init__(self, seat_label: str) -> None:
        super().__init__(
            message=f"Seat '{seat_label}' already exists.",
            status_code=409,
        )


class EmployeeAlreadyAllocatedError(AppException):
    """Raised when trying to allocate a seat to an employee who already has one."""

    def __init__(self, employee_id: str | int) -> None:
        super().__init__(
            message=f"Employee '{employee_id}' already has an active seat allocation.",
            status_code=409,
        )


class SeatOccupiedError(AppException):
    """Raised when trying to allocate an already-occupied seat."""

    def __init__(self, seat_id: str | int) -> None:
        super().__init__(
            message=f"Seat '{seat_id}' is already occupied.",
            status_code=409,
        )


# ── 400 Bad Request ──────────────────────────────────────────────────────────


class SeatReservedError(AppException):
    """Raised when trying to allocate a reserved seat."""

    def __init__(self, seat_id: str | int) -> None:
        super().__init__(
            message=f"Seat '{seat_id}' is reserved and cannot be allocated.",
            status_code=400,
        )


class SeatMaintenanceError(AppException):
    """Raised when trying to allocate a seat under maintenance."""

    def __init__(self, seat_id: str | int) -> None:
        super().__init__(
            message=f"Seat '{seat_id}' is under maintenance and cannot be allocated.",
            status_code=400,
        )


class InactiveEmployeeError(AppException):
    """Raised when an operation targets an inactive employee."""

    def __init__(self, employee_id: str | int) -> None:
        super().__init__(
            message=f"Employee '{employee_id}' is inactive and cannot be allocated a seat.",
            status_code=400,
        )
