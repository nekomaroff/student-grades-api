from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
import csv
import io

from app.db import execute_query

router = APIRouter()


@router.post("/upload-grades")
def upload_grades(file: UploadFile = File(...)):
    content = file.file.read().decode("utf-8-sig")
    buffer = io.StringIO(content)

    try:
        dialect = csv.Sniffer().sniff(content[:1000], delimiters=";,")
    except csv.Error:
        raise HTTPException(status_code=400, detail="Cannot detect CSV delimiter")

    reader = csv.reader(buffer, dialect)

    headers = next(reader, None)
    expected_headers = ["Дата", "Номер группы", "ФИО", "Оценка"]

    headers = [h.strip() for h in headers]
    if headers != expected_headers:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid CSV header. Expected {expected_headers}, got {headers}"
        )

    insert_query = """
        INSERT INTO grades (grade_date, group_id, full_name, grade)
        VALUES (%s, %s, %s, %s)
    """

    inserted = 0
    skipped = 0
    students = set()

    for row in reader:
        if len(row) != 4:
            skipped += 1
            continue

        date_str, group_id, full_name, grade_str = [x.strip() for x in row]

        try:
            grade_date = datetime.strptime(date_str, "%d.%m.%Y").date()
            grade = int(grade_str)
        except ValueError:
            skipped += 1
            continue

        if grade not in (2, 3, 4, 5):
            skipped += 1
            continue

        execute_query(
            insert_query,
            params=(grade_date, group_id, full_name, grade),
            fetch=False
        )

        inserted += 1
        students.add(full_name)

    return {
        "status": "ok",
        "records_loaded": inserted,
        "records_skipped": skipped,
        "students": len(students)
    }


@router.get("/students/more-than-3-twos")
def students_more_than_3_twos():
    query = """
        SELECT
            full_name,
            COUNT(*) AS count_twos
        FROM grades
        WHERE grade = 2
        GROUP BY full_name
        HAVING COUNT(*) > 3
        ORDER BY count_twos DESC
    """

    rows = execute_query(query, fetch=True)

    return [
        {"full_name": row["full_name"], "count_twos": row["count_twos"]}
        for row in rows
    ]


@router.get("/students/less-than-5-twos")
def students_less_than_5_twos():
    query = """
        SELECT
            full_name,
            COUNT(*) AS count_twos
        FROM grades
        WHERE grade = 2
        GROUP BY full_name
        HAVING COUNT(*) < 5
        ORDER BY count_twos DESC
    """

    rows = execute_query(query, fetch=True)

    return [
        {"full_name": row["full_name"], "count_twos": row["count_twos"]}
        for row in rows
    ]