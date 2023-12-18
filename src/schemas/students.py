import pandera as pa
from pandera.typing import DataFrame, Series


class Student(pa.SchemaModel):
    student_id: Series[int] = pa.Field(unique=True)
    gender: Series[int] = pa.Field(isin=([0, 1]))
    score: Series[int] = pa.Field(ge=0, le=500)
    leader_flag: Series[int] = pa.Field(isin=([0, 1]))
    support_flag: Series[int] = pa.Field(isin=([0, 1]))
    
    class Config:
        strict = True


def validate_students(df: DataFrame) -> DataFrame:
    """Studentデータのバリデーション

    Args:
        df (DataFrame): Studentデータ

    Returns:
        DataFrame: バリデーション後のStudentデータ
    """
    return Student.validate(df)
