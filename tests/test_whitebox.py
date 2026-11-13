import pytest

from registration import (
    Student,
    Course,
    registration_decision,
    register_course,
    withdraw_course
)


# These tests check the different decision paths in registration.py.
# The expected results are taken from the project requirements.


def make_student(dues=0, credits=0, completed=None, registered=None):
    if completed is None:
        completed = set()
    if registered is None:
        registered = set()

    return Student(
        student_id="S101",
        completed_courses=completed,
        current_credits=credits,
        outstanding_dues=dues,
        registered_courses=registered
    )


def make_course(enrolled=0, capacity=30, prerequisites=None, credits=3):
    if prerequisites is None:
        prerequisites = set()

    return Course(
        code="CS201",
        credit_hours=credits,
        capacity=capacity,
        enrolled=enrolled,
        prerequisites=prerequisites
    )


# D1 and D2: input validation paths


def test_negative_dues_raise_error():
    student = make_student(dues=-1)
    course = make_course()

    with pytest.raises(ValueError, match="Invalid dues"):
        registration_decision(student, course)


@pytest.mark.parametrize(
    "enrolled, capacity",
    [
        (-1, 10),  # enrolled cannot be negative
        (11, 10),  # enrolled cannot be greater than capacity
        (0, 0)     # capacity must be at least 1
    ]
)
def test_invalid_course_capacity_values_raise_error(enrolled, capacity):
    student = make_student()
    course = make_course(enrolled=enrolled, capacity=capacity)

    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(student, course)


def test_valid_course_capacity_does_not_raise_error():
    student = make_student()
    course = make_course(enrolled=5, capacity=10)

    assert registration_decision(student, course) == "REGISTERED"


# D3: outstanding dues decision


def test_any_positive_dues_block_registration():
    student = make_student(dues=1)
    course = make_course()

    assert registration_decision(student, course) == "DUES_BLOCK"


# D4: already registered decision


def test_already_registered_course_is_blocked():
    student = make_student(registered={"CS201"})
    course = make_course()

    assert registration_decision(student, course) == "ALREADY_REGISTERED"


# D5: prerequisite decision


def test_registration_allowed_when_all_prerequisites_are_completed():
    student = make_student(completed={"CS101", "MATH101"})
    course = make_course(prerequisites={"CS101", "MATH101"})

    assert registration_decision(student, course) == "REGISTERED"


def test_registration_blocked_when_one_prerequisite_is_missing():
    student = make_student(completed={"CS101"})
    course = make_course(prerequisites={"CS101", "MATH101"})

    assert registration_decision(student, course) == "PREREQUISITES_MISSING"


def test_empty_prerequisites_are_satisfied():
    student = make_student()
    course = make_course(prerequisites=set())

    assert registration_decision(student, course) == "REGISTERED"


# D6: credit limit decision


def test_total_credits_equal_to_18_are_allowed():
    student = make_student(credits=15)
    course = make_course(credits=3)

    assert registration_decision(student, course) == "REGISTERED"


def test_total_credits_above_18_are_rejected():
    student = make_student(credits=16)
    course = make_course(credits=3)

    assert registration_decision(student, course) == "CREDIT_LIMIT"


# D7: course availability decision


def test_course_with_available_seats_is_registered():
    student = make_student()
    course = make_course(enrolled=9, capacity=10)

    assert registration_decision(student, course) == "REGISTERED"


def test_full_course_student_is_waitlisted():
    student = make_student()
    course = make_course(enrolled=10, capacity=10)

    assert registration_decision(student, course) == "WAITLISTED"


# The decision function should only return a result.
# It should not change the student or course data.


def test_registration_decision_does_not_change_objects():
    student = make_student(credits=6)
    course = make_course(enrolled=4, capacity=10)

    old_registered = student.registered_courses.copy()
    old_credits = student.current_credits
    old_enrolled = course.enrolled
    old_waitlist = course.waitlist.copy()

    registration_decision(student, course)

    assert student.registered_courses == old_registered
    assert student.current_credits == old_credits
    assert course.enrolled == old_enrolled
    assert course.waitlist == old_waitlist


# Tests for register_course state changes


def test_register_course_updates_student_and_course():
    student = make_student(credits=6)
    course = make_course(enrolled=4, capacity=10, credits=3)

    result = register_course(student, course)

    assert result == "REGISTERED"
    assert "CS201" in student.registered_courses
    assert student.current_credits == 9
    assert course.enrolled == 5


def test_waitlisted_student_is_added_only_once():
    student = make_student()
    course = make_course(enrolled=10, capacity=10)

    first_result = register_course(student, course)
    second_result = register_course(student, course)

    assert first_result == "WAITLISTED"
    assert second_result == "WAITLISTED"
    assert course.waitlist.count("S101") == 1


# Tests for withdraw_course paths


def test_withdraw_registered_course_updates_records():
    student = make_student(credits=6, registered={"CS201"})
    course = make_course(enrolled=5, capacity=10, credits=3)

    result = withdraw_course(student, course)

    assert result is True
    assert "CS201" not in student.registered_courses
    assert student.current_credits == 3
    assert course.enrolled == 4


def test_withdraw_course_when_not_registered_returns_false():
    student = make_student(credits=6)
    course = make_course(enrolled=5, capacity=10)

    old_credits = student.current_credits
    old_enrolled = course.enrolled
    old_registered = student.registered_courses.copy()

    result = withdraw_course(student, course)

    assert result is False
    assert student.current_credits == old_credits
    assert course.enrolled == old_enrolled
    assert student.registered_courses == old_registered


def test_dues_above_1000_reaches_dues_block_branch():
    student = make_student(dues=1001)
    course = make_course()

    result = registration_decision(student, course)

    assert result == "DUES_BLOCK"

def test_waitlisted_student_is_added_once(monkeypatch):
    student = make_student()
    course = make_course()

    monkeypatch.setattr(
        "registration.registration_decision",
        lambda student, course: "WAITLISTED"
    )

    result = register_course(student, course)

    assert result == "WAITLISTED"
    assert course.waitlist == ["S101"]

def test_existing_waitlist_student_is_not_added_again(monkeypatch):
    student = make_student()
    course = make_course()
    course.waitlist.append("S101")

    monkeypatch.setattr(
        "registration.registration_decision",
        lambda student, course: "WAITLISTED"
    )

    result = register_course(student, course)

    assert result == "WAITLISTED"
    assert course.waitlist == ["S101"]
    