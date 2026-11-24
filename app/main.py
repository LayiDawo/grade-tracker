"""Small command-line demo for the grade tracker."""
from app.grades import GradeBook, format_student_line


def run_demo():
    book = GradeBook("CSCN73010")
    book.add_student("1001", "Ada")
    book.add_student("1002", "Linus")
    book.add_score("1001", 95)
    book.add_score("1001", 88)
    book.add_score("1002", 45)
    for sid, name, avg in book.class_report(True, True, False):
        print(format_student_line(sid, name, avg))


if __name__ == "__main__":
    run_demo()
