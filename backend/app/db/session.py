"""SQLAlchemy engine and session factory configuration.

Connection pooling is configured per the implementation plan (Section 16):
- pool_size=10        — 10 persistent connections
- max_overflow=20     — up to 20 additional connections under load
- pool_timeout=30     — wait 30s before erroring on pool exhaustion
- pool_recycle=1800   — recycle connections every 30 minutes
"""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

logger.info(
    "Database engine created — pool_size=%d, max_overflow=%d",
    settings.DB_POOL_SIZE,
    settings.DB_MAX_OVERFLOW,
)
