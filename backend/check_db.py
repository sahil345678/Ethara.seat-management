import psycopg2
import sys

def check_postgres(password="postgres"):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=password,
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'ethara_db'")
        exists = cursor.fetchone()
        
        if not exists:
            print("Creating ethara_db...")
            cursor.execute("CREATE DATABASE ethara_db")
            print("Created.")
        else:
            print("ethara_db already exists.")
            
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Failed with password {password}: {e}")
        return False

if not check_postgres("postgres"):
    if not check_postgres("root"):
        if not check_postgres(""):
            print("Could not connect to PostgreSQL.")
            sys.exit(1)

print("Success!")
sys.exit(0)
