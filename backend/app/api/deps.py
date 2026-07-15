"""Shared FastAPI dependencies for dependency injection.

All dependencies defined here are injected into route handlers
via FastAPI's `Depends()` mechanism.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy database session with automatic cleanup.

    The session is created from `SessionLocal` and is guaranteed to
    be closed after the request completes, even if an exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
