from fastapi import APIRouter, UploadFile, File
from typing import List

from app.schemas.grades import (
    UploadGradesResponse,
    StudentTwosStats,
)
from app.services.grades_service import (
    upload_grades_from_csv,
    get_students_more_than_3_twos,
    get_students_less_than_5_twos,
)

router = APIRouter()


@router.post(
    "/upload-grades",
    response_model=UploadGradesResponse,
)
def upload_grades(file: UploadFile = File(...)):
    return upload_grades_from_csv(file)


@router.get(
    "/students/more-than-3-twos",
    response_model=List[StudentTwosStats],
)
def students_more_than_3_twos():
    return get_students_more_than_3_twos()


@router.get(
    "/students/less-than-5-twos",
    response_model=List[StudentTwosStats],
)
def students_less_than_5_twos():
    return get_students_less_than_5_twos()

@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}