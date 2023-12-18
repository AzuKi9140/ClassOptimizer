import pandera as pa
from pandera.typing import DataFrame, Series


class Pair(pa.SchemaModel):
    student_id1: Series[int] = pa.Field()
    student_id2: Series[int] = pa.Field()

    class Config:
        strict = True


def validate_student_pairs(df: DataFrame) -> DataFrame:
    return Pair.validate(df)
