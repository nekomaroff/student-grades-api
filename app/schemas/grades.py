from pydantic import BaseModel
from datetime import date


class GradeCreate(BaseModel):
    grade_date: date
    group_id: int
    full_name: str
    grade: int


class StudentTwosStats(BaseModel):
    full_name: str
    count_twos: int


class UploadGradesResponse(BaseModel):
    status: str
    records_loaded: int
    records_skipped: int
    students: int