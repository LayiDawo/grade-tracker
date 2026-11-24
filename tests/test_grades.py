import pytest

from app.grades import GradeBook, format_student_line
from app.main import run_demo


@pytest.fixture
def book():
    b = GradeBook("CSCN73010")
    b.add_student("1001", "Ada")
    return b


@pytest.fixture
def full_book():
    b = GradeBook("CSCN73010")
    b.add_student("1", "Zed")
    b.add_student("2", "Amy")
    b.add_student("3", "Bob")
    b.add_student("4", "New")  # no scores yet
    b.add_score("1", 85)
    b.add_score("2", 65)
    b.add_score("3", 40)
    return b


def test_add_student_duplicate_raises(book):
    with pytest.raises(ValueError):
        book.add_student("1001", "Ada again")


def test_add_score_unknown_student_raises(book):
    with pytest.raises(KeyError):
        book.add_score("9999", 50)


def test_add_score_and_average(book):
    book.add_score("1001", 80)
    book.add_score("1001", 90)
    assert book.average("1001") == 85


def test_add_score_out_of_range(book):
    with pytest.raises(ValueError):
        book.add_score("1001", 101)
    with pytest.raises(ValueError):
        book.add_score("1001", -1)


def test_average_with_no_scores_raises_clear_error(book):
    # Independently tested risk: the baseline crashed with ZeroDivisionError here
    with pytest.raises(ValueError, match="no scores"):
        book.average("1001")


@pytest.mark.parametrize(
    "score, expected",
    [(95, "A+"), (90, "A+"), (85, "A"), (75, "B"), (65, "C"), (55, "D"), (49, "F")],
)
def test_letter_grade_boundaries(book, score, expected):
    book.add_score("1001", score)
    assert book.letter_grade("1001") == expected


def test_class_report_include_failing_sorted_by_name(full_book):
    names = [r[1] for r in full_book.class_report(True, True, False)]
    assert names == ["Amy", "Bob", "New", "Zed"]


def test_class_report_passing_only_sorted_by_average(full_book):
    report = full_book.class_report(False, False, False)
    assert [r[1] for r in report] == ["Zed", "Amy"]


def test_class_report_honours_only(full_book):
    report = full_book.class_report(False, False, True)
    assert [r[1] for r in report] == ["Zed"]


def test_save_and_load_round_trip(full_book, tmp_path):
    path = tmp_path / "grades.json"
    full_book.save(path)
    loaded = GradeBook("other")
    assert loaded.load(path) is True
    assert loaded.course_code == "CSCN73010"
    assert loaded.students == full_book.students


def test_load_missing_file_returns_false(tmp_path):
    assert GradeBook("x").load(tmp_path / "missing.json") is False


def test_save_to_bad_path_raises(book, tmp_path):
    # Independently tested risk: the baseline silently swallowed this error
    with pytest.raises(OSError):
        book.save(tmp_path / "no_such_dir" / "grades.json")


@pytest.mark.parametrize(
    "avg, status", [(91.5, "PASS"), (50, "PASS"), (45, "FAIL")]
)
def test_format_student_line(avg, status):
    line = format_student_line("1001", "Ada", avg)
    assert line.endswith(f"Student status: {status}")


def test_run_demo_prints_report(capsys):
    run_demo()
    out = capsys.readouterr().out
    assert "1001 | Ada | 91.5 | Student status: PASS" in out
    assert "1002 | Linus | 45.0 | Student status: FAIL" in out