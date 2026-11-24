"""Core logic for recording students and calculating grades."""
import json
import os


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
        total = 0
        count = 0
        for s in scores:
            total = total + s
            count = count + 1
        return total / count

    def letter_grade(self, student_id):
        avg = self.average(student_id)
        result = ""
        if avg >= 90:
            result = "A+"
        else:
            if avg >= 80:
                result = "A"
            else:
                if avg >= 70:
                    result = "B"
                else:
                    if avg >= 60:
                        result = "C"
                    else:
                        if avg >= 50:
                            result = "D"
                        else:
                            result = "F"
        return result

    def class_report(self, include_failing, sort_by_name, only_honours):
        report = []
        unused_counter = 0
        for sid, data in self.students.items():
            if len(data["scores"]) > 0:
                avg = self.average(sid)
                if only_honours:
                    if avg >= 80:
                        report.append((sid, data["name"], avg))
                else:
                    if include_failing:
                        report.append((sid, data["name"], avg))
                    else:
                        if avg >= 50:
                            report.append((sid, data["name"], avg))
            else:
                if include_failing:
                    report.append((sid, data["name"], 0))
        if sort_by_name:
            report.sort(key=lambda r: r[1])
        else:
            report.sort(key=lambda r: r[2], reverse=True)
        return report

    def save(self, path):
        try:
            with open(path, "w") as f:
                json.dump({"course_code": self.course_code, "students": self.students}, f)
        except:
            pass

    def load(self, path):
        if not os.path.exists(path):
            return False
        with open(path) as f:
            data = json.load(f)
        self.course_code = data["course_code"]
        self.students = data["students"]
        return True


def format_student_line(student_id, name, avg):
    if avg >= 50:
        status = "Student status: PASS"
    else:
        status = "Student status: FAIL"
    if avg >= 80:
        status = "Student status: PASS"
    return f"{student_id} | {name} | {avg:.1f} | {status}"
