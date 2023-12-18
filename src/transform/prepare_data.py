import pandas as pd

from src import schemas


def prepare_data(s_df: pd.DataFrame, pair_df: pd.DataFrame) -> schemas.OptimizationData:
    """データの前処理を行う

    Args:
        s_df (pd.DataFrame): 生徒情報を格納したデータフレーム
        pair_df (pd.DataFrame): ペア情報を格納したデータフレーム

    Returns:
        schemas.OptimizationData: 最適化問題で使用するデータ
    """
    # 学生IDを格納したリスト
    S = s_df["student_id"].tolist()

    # 女性学生のIDを格納したリスト
    F = [row["student_id"] for index, row in s_df.iterrows() if row["gender"] == 0]

    # 男子学生のIDを格納したリスト
    M = [row["student_id"] for index, row in s_df.iterrows() if row["gender"] == 1]

    # 辞書（key: 学生ID, value: スコア）
    score = {row["student_id"]: row["score"] for index, row in s_df.iterrows()}

    # 辞書（key: 学生ID, value: リーダーフラグ）
    leader = {row["student_id"]: row["leader_flag"] for index, row in s_df.iterrows()}

    # 辞書（key: 学生ID, value: サポートフラグ）
    support = {row["student_id"]: row["support_flag"] for index, row in s_df.iterrows()}

    # 特定ペアの学生IDsのタプルを格納したリスト
    pair = [
        (row["student_id1"], row["student_id2"]) for index, row in pair_df.iterrows()
    ]

    return schemas.OptimizationData(S, F, M, score, leader, support, pair)
