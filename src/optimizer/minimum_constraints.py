from typing import List, Tuple

from mip import Model, minimize, xsum

from src import schemas


def minimum_constraints(
    data: schemas.OptimizationData, C: List[str]
) -> Tuple[Model, dict]:
    n = len(data.S)  # n: 学生数

    SC = [(s, c) for s in data.S for c in C]  # 学生IDとクラス名のタプルを格納したリスト

    p = Model("assignment")

    # 決定変数の定義
    x = {}
    for s, c in SC:
        x[s, c] = p.add_var("x({},{})".format(s, c), var_type="B")

    # 目的関数の設定
    p.objective = minimize(xsum(x[s, c] for s in data.S for c in C))

    # 制約の設定
    # 各学生は1つのクラスに割り当てられる
    for s in data.S:
        p += xsum(x[s, c] for c in C) == 1  # 各学生は1つのクラスに割り当てられる

    # 各クラスの生徒数はできるだけ均等にする
    for c in C:
        p += xsum(x[s, c] for s in data.S) >= n // len(C)
        p += xsum(x[s, c] for s in data.S) <= (n // len(C)) + 1

    # 各クラスの男性の人数をできるだけ均等にする
    for c in C:
        p += xsum(x[s, c] for s in data.M) >= len(data.M) // len(C)
        p += xsum(x[s, c] for s in data.M) <= (len(data.M) // len(C)) + 1

    # 各クラスの女性の人数をできるだけ均等にする
    for c in C:
        p += xsum(x[s, c] for s in data.F) >= len(data.F) // len(C)
        p += xsum(x[s, c] for s in data.F) <= (len(data.F) // len(C)) + 1

    # 各クラスの学力をできるだけ均等にする
    total_score = sum(data.score.values())
    for c in C:
        p += xsum(data.score[s] * x[s, c] for s in data.S) >= total_score // len(C)
        # p += xsum(score[s] * x[s, c] for s in S) <= (total_score // len(C)) + 1
        p += xsum(data.score[s] * x[s, c] for s in data.S) <= (
            total_score // len(C)
        ) + max(data.score.values())

    # 各クラスにできるだけ均等にリーダー気質の学生を割り当てる
    total_leaders = sum(data.leader.values())
    for c in C:
        p += xsum(data.leader[s] * x[s, c] for s in data.S) >= total_leaders // len(C)
        p += (
            xsum(data.leader[s] * x[s, c] for s in data.S)
            <= (total_leaders // len(C)) + 1
        )

    # 特別な支援が必要な生徒はできるだけ分散させて割り当てる
    total_support = sum(data.support.values())
    for c in C:
        p += xsum(data.support[s] * x[s, c] for s in data.S) >= total_support // len(C)
        p += (
            xsum(data.support[s] * x[s, c] for s in data.S)
            <= (total_support // len(C)) + 1
        )

    # 特定ペアの学生は同じクラスに割り当てない
    for s1, s2 in data.pair:
        for c in C:
            p += x[s1, c] + x[s2, c] <= 1

    return p, x
