import os
import sys
import psycopg2


database_url = os.getenv("DATABASE_URL")

if not database_url:
    print("DATABASE_URL not found")
    sys.exit(1)

try:
    conn = psycopg2.connect(database_url)
    conn.close()
    print("Database connection successful!")
    sys.exit(0)
except Exception as e:
    print(f"Database connection failed: {e}")
    sys.exit(1)
