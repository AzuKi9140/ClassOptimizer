from typing import Dict, List

from pandas import DataFrame

from src import schemas


def format_results(
    x: dict, df: DataFrame, C: List[str], S: List[int]
) -> Dict[str, List[schemas.StudentInfo]]:
    """最適化結果を整形する

    Args:
        x (dict): 最適化結果
        df (DataFrame): 生徒情報を格納したデータフレーム
        C (List[str]): クラス名を格納したリスト
        S (List[int]): 学生IDを格納したリスト

    Returns:
        Dict[str, List[schemas.StudentInfo]]: 整形後の最適化結果
    """
    class_to_students = {}
    for c in C:
        class_to_students[c] = [s for s in S if x[s, c].x >= 0.5]

    formatted_results = {}
    for c, s_list in class_to_students.items():
        formatted_results[c] = [
            schemas.StudentInfo(
                student_id=student["student_id"],
                gender=student["gender"],
                score=student["score"],
                leader_flag=student["leader_flag"],
                support_flag=student["support_flag"],
            )
            for student in df[df["student_id"].isin(s_list)].to_dict("records")
        ]
    return formatted_results
