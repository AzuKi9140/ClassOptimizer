import matplotlib.pyplot as plt
import pandas as pd

from src import optimizer, schemas
from src.transform.prepare_data import prepare_data


def main():
    s_df = pd.read_csv("data/students.csv")
    s_df = schemas.validate_students(s_df)
    n = len(s_df)  # n: 学生数

    print("学生数 = {}".format(n))

    pair_df = pd.read_csv("data/student_pairs.csv")
    pair_df = schemas.validate_student_pairs(pair_df)
    p = len(pair_df)

    print("特定ペア数 = {}".format(p))
    print(pair_df.head())

    C = ["A", "B", "C", "D", "E", "F", "G", "H"]  # クラス名を格納したリスト

    data = prepare_data(s_df, pair_df)

    model, x = optimizer.minimum_constraints(data, C)
    model = optimizer.add_balanced_assignment_constraint(
        model, x, data.score, C, data.S
    )

    model.optimize()

    c2s = {}
    for c in C:
        c2s[c] = [s for s in data.S if x[s, c].x >= 0.5]
    print(c2s)

    # 各クラスのスコアを格納するための辞書
    class_scores = {c: [] for c in C}

    # 各クラスのスコアを計算
    for c, s_list in c2s.items():
        for s in s_list:
            class_scores[c].append(data.score[s])

    # ヒストグラムを描画
    for c, scores in class_scores.items():
        plt.hist(scores, bins=10, alpha=0.5, label=c)

    plt.legend(loc="upper right")
    plt.show()


if __name__ == "__main__":
    main()
