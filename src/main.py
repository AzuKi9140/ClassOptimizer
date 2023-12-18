import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src import optimizer, schemas
from src.transform.format_result import format_results
from src.transform.prepare_data import prepare_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--add_score", action="store_true")
    args = parser.parse_args()

    s_df = pd.read_csv("data/students.csv")
    s_df = schemas.validate_students(s_df)

    pair_df = pd.read_csv("data/student_pairs.csv")
    pair_df = schemas.validate_student_pairs(pair_df)

    C = ["A", "B", "C", "D", "E", "F", "G", "H"]  # クラス名を格納したリスト

    data = prepare_data(s_df, pair_df)

    model, x = optimizer.minimum_constraints(data, C)
    if args.add_score:
        model = optimizer.add_balanced_assignment_constraint(
            model, x, data.score, C, data.S
        )

    model.optimize()

    # 各クラスの生徒情報を整形
    formatted_results = format_results(x, s_df, C, data.S)
    for c, students in formatted_results.items():
        print(c)
        for student in students:
            print(student)

    # 各クラスのスコアを格納するための辞書
    class_scores = {
        c: [student.score for student in students]
        for c, students in formatted_results.items()
    }

    # ヒストグラムを描画
    for c, scores in class_scores.items():
        plt.hist(scores, bins=10, alpha=0.5, label=c)
        print(f"Class {c}:")
        print(f"Mean: {np.mean(scores):.2f}")
        print(f"Median: {np.median(scores):.2f}")
        print(f"Standard Deviation: {np.std(scores):.2f}")
        print(f"Min: {np.min(scores):.2f}")
        print(f"Max: {np.max(scores):.2f}")
        print(f"Range: {np.max(scores) - np.min(scores):.2f}")
        print("-" * 30)

    plt.legend(loc="upper right")
    if args.add_score:
        plt.title("score added")
        plt.savefig("image/histogram_add_score_constraint.png")
    else:
        plt.savefig("image/normal_histogram.png")

    # pyplotインスタンスをクリア
    plt.clf()

    # ボックスプロットを描画
    plt.figure(figsize=(10, 6))
    plt.boxplot(class_scores.values(), labels=class_scores.keys())

    # ボックスプロットを画像として保存
    if args.add_score:
        plt.title("score added")
        plt.savefig("image/boxplot_add_score_constraint.png")
    else:
        plt.savefig("image/normal_boxplot.png")


if __name__ == "__main__":
    main()
