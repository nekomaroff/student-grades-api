import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "grades_db",
    "user": "grades_user",
    "password": "grades_password",
    "host": "localhost",
    "port": 5432,
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def execute_query(query: str, params=None, fetch: bool = False):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            conn.commit()
    finally:
        conn.close()