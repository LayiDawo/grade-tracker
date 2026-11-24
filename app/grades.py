"""Core logic for recording students and calculating grades."""
import json
import os

PASS_MARK = 50
HONOURS_MARK = 80

# (minimum average, letter) checked from highest to lowest
GRADE_THRESHOLDS = [(90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D")]


class GradeBook:
    def __init__(self, course_code):
        self.course_code = course_code
        self.students = {}

    def add_student(self, student_id, name):
        if student_id in self.students:
            raise ValueError("Student already exists")
        self.students[student_id] = {"name": name, "scores": []}

    def add_score(self, student_id, score):
        if student_id not in self.students:
            raise KeyError("Student not found")
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100")
        self.students[student_id]["scores"].append(score)

    def average(self, student_id):
        scores = self.students[student_id]["scores"]
        if not scores:
            raise ValueError("Student has no scores recorded")
        return sum(scores) / len(scores)

    def letter_grade(self, student_id):
        avg = self.average(student_id)
        for minimum, letter in GRADE_THRESHOLDS:
            if avg >= minimum:
                return letter
        return "F"

    def _student_average_or_zero(self, student_id):
        if not self.students[student_id]["scores"]:
            return 0
        return self.average(student_id)

    def class_report(self, include_failing, sort_by_name, only_honours):
        if only_honours:
            minimum = HONOURS_MARK
        elif include_failing:
            minimum = 0
        else:
            minimum = PASS_MARK

        report = []
        for sid, data in self.students.items():
            if only_honours and not data["scores"]:
                continue
            avg = self._student_average_or_zero(sid)
            if avg >= minimum:
                report.append((sid, data["name"], avg))

        if sort_by_name:
            report.sort(key=lambda r: r[1])
        else:
            report.sort(key=lambda r: r[2], reverse=True)
        return report

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"course_code": self.course_code, "students": self.students}, f)

    def load(self, path):
        if not os.path.exists(path):
            return False
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        self.course_code = data["course_code"]
        self.students = data["students"]
        return True


def format_student_line(student_id, name, avg):
    status = "PASS" if avg >= PASS_MARK else "FAIL"
    return f"{student_id} | {name} | {avg:.1f} | Student status: {status}"