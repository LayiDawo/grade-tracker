import pytest

from app.grades import GradeBook


@pytest.fixture
def book():
    b = GradeBook("CSCN73010")
    b.add_student("1001", "Ada")
    return b


def test_add_student_duplicate_raises(book):
    with pytest.raises(ValueError):
        book.add_student("1001", "Ada again")


def test_add_score_and_average(book):
    book.add_score("1001", 80)
    book.add_score("1001", 90)
    assert book.average("1001") == 85


def test_add_score_out_of_range(book):
    with pytest.raises(ValueError):
        book.add_score("1001", 101)


def test_letter_grade_a_plus(book):
    book.add_score("1001", 95)
    assert book.letter_grade("1001") == "A+"
