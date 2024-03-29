import pandera as pa
from pandera.typing import DataFrame, Series
from pydantic import BaseModel


class Student(pa.SchemaModel):
    student_id: Series[int] = pa.Field(unique=True)
    gender: Series[int] = pa.Field(isin=([0, 1]))
    score: Series[int] = pa.Field(ge=0, le=500)
    leader_flag: Series[int] = pa.Field(isin=([0, 1]))
    support_flag: Series[int] = pa.Field(isin=([0, 1]))

    class Config:
        strict = True


def validate_students(df: DataFrame, num_classes: int) -> DataFrame:
    """Studentデータのバリデーション

    Args:
        df (DataFrame): Studentデータ
        num_classes (int): クラス数

    Returns:
        DataFrame: バリデーション後のStudentデータ
    """
    assert len(df) >= num_classes * 2, "学生数はクラス数の2倍以上である必要があります"
    return Student.validate(df)


class StudentInfo(BaseModel):
    student_id: int
    gender: int
    score: int
    leader_flag: bool
    support_flag: bool
