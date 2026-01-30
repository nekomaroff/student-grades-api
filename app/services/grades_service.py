from typing import List
from datetime import datetime
import csv
import io

from fastapi import UploadFile, HTTPException

from app.schemas.grades import UploadGradesResponse, StudentTwosStats
from app.repositories.grades_repository import (
    insert_grade,
    fetch_students_more_than_3_twos,
    fetch_students_less_than_5_twos,
)
from app.constants import ALLOWED_GRADES, CSV_HEADERS, CSV_DATE_FORMAT


def upload_grades_from_csv(file: UploadFile) -> UploadGradesResponse:
    content = file.file.read().decode("utf-8-sig")
    buffer = io.StringIO(content)
    reader = csv.reader(buffer)

    headers = next(reader, None)
    if headers != CSV_HEADERS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid CSV header. Expected {CSV_HEADERS}, got {headers}",
        )

    inserted = 0
    skipped = 0
    students = set()

    for row in reader:
        try:
            grade_date = datetime.strptime(row[0], CSV_DATE_FORMAT).date()
            group_id = int(row[1])
            full_name = row[2]
            grade = int(row[3])
        except Exception:
            skipped += 1
            continue

        if grade not in ALLOWED_GRADES:
            skipped += 1
            continue

        insert_grade(
            grade_date=grade_date,
            group_id=group_id,
            full_name=full_name,
            grade=grade,
        )

        inserted += 1
        students.add(full_name)

    return UploadGradesResponse(
        status="ok",
        records_loaded=inserted,
        records_skipped=skipped,
        students=len(students),
    )


def get_students_more_than_3_twos() -> List[StudentTwosStats]:
    return fetch_students_more_than_3_twos()


def get_students_less_than_5_twos() -> List[StudentTwosStats]:
    return fetch_students_less_than_5_twos()