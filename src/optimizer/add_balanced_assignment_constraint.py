from mip import Model, xsum


def add_balanced_assignment_constraint(
    model: Model, x: dict, scores: dict, classes: list, students: list
):
    sorted_students = sorted(students, key=lambda s: scores[s])
    num_classes = len(classes)

    for i in range(num_classes):
        # 上位と下位から学生を選び、それぞれを異なるクラスに割り当てる
        top_student = sorted_students[i]
        bottom_student = sorted_students[-i - 1]
        model += xsum(x[top_student, c] for c in classes) == 1
        model += xsum(x[bottom_student, c] for c in classes) == 1
        model += xsum(x[top_student, c] + x[bottom_student, c] for c in classes) == 2

    return model
