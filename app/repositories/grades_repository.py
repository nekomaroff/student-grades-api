
from datetime import date
from app.db import execute_query
def insert_grade(
    grade_date: date,
    group_id: int,
    full_name: str,
    grade: int,
) -> None:
    ...


def fetch_students_more_than_3_twos() -> list[dict]:
    ...


def fetch_students_less_than_5_twos() -> list[dict]:
    ...