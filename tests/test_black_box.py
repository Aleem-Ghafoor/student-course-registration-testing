from registration import (
    check_credit_limit,
    prerequisites_satisfied,
    Student, 
    Course, 
    registration_decision, 
    register_course,
    withdraw_course
)

import pytest


#TC-01
def test_check_current_credit_limit_within_limit():
    result = check_credit_limit(10, 3)
    assert result == True

#TC-02
def test_check_current_credit_limit_exactly_at_limit():
    result = check_credit_limit(15, 3)
    assert result == True

#TC-03
def test_check_current_credit_limit_exceeds_limit():
    result = check_credit_limit(16, 3)
    assert result == False

#TC-04
def test_check_current_credit_limit_below_range():
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(-1, 3)

#TC-05
def test_check_current_credit_limit_above_range():
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(19, 3)

#TC-06
def test_check_new_credit_limit_below_range():
    with pytest.raises(ValueError, match="Invalid course credits"):
        check_credit_limit(10, 0)
    
#TC-07
def test_check_new_credit_limit_above_range():
    with pytest.raises(ValueError, match="Invalid course credits"):
        check_credit_limit(10, 5)

#TC-08
def test_No_prerequisites_required():
    result = prerequisites_satisfied({}, {})
    assert result == True

#TC-09
def test_All_prerequisites_completed():
    result = prerequisites_satisfied({"CS101", "MATH101"}, {"CS101", "MATH101"})
    assert result == True 

#TC-10
def test_Some_prerequisites_completed():
    result = prerequisites_satisfied({"CS101"}, {"CS101", "MATH101"})
    assert result == False

#TC-11
def test_No_prerequisites_completed():
    result = prerequisites_satisfied({""}, {"CS201", "MATH201"})
    assert result == False

#TC-12
def test_No_outstanding_dues():
    student = Student(
        student_id="S001", 
        completed_courses={"CS101"}, 
        current_credits=12, 
        outstanding_dues=0, 
        registered_courses=set()
    )

    course = Course(
        code="CS201", 
        credit_hours=3, 
        capacity=30, 
        enrolled=25, 
        prerequisites={"CS101"}
    )

    result = registration_decision(student, course)
    assert result == "REGISTERED"

#TC-13
def test_Positive_outstanding_dues():
    student = Student(
        student_id="S002", 
        completed_courses={"CS101"}, 
        current_credits=12, 
        outstanding_dues=1, 
        registered_courses=set()
    )

    course = Course(
        code="CS201", 
        credit_hours=3, 
        capacity=30, 
        enrolled=25, 
        prerequisites={"CS101"}
    )

    result = registration_decision(student, course)
    assert result == "DUES_BLOCK"

#TC-14
def test_Course_already_registered():
    student = Student(
        student_id="S003", 
        completed_courses={"CS101"}, 
        current_credits=12, 
        outstanding_dues=0, 
        registered_courses={"CS201"}
    )

    course = Course(
        code="CS201", 
        credit_hours=3, 
        capacity=30, 
        enrolled=25, 
        prerequisites={"CS101"}
    )

    result = registration_decision(student, course)
    assert result == "ALREADY_REGISTERED"


#TC-15
def test_Course_not_already_registered():
    student = Student(
        student_id="S004",
        completed_courses={"CS101"},
        current_credits=12,
        outstanding_dues=0,
        registered_courses={"CS101"}
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=25,
        prerequisites={"CS101"}
    )

    result = registration_decision(student, course)
    assert result == "REGISTERED"


#TC-16
def test_All_prerequisites_satisfied():
    student = Student(
        student_id="S005",
        completed_courses={"CS101"},
        current_credits=12
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=25,
        prerequisites={"CS101"}
    )

    result = registration_decision(student, course)
    assert result == "REGISTERED"


#TC-17
def test_At_least_one_prerequisite_missing():
    student = Student(
        student_id="S006",
        completed_courses={"CS101"},
        current_credits=12
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=25,
        prerequisites={"CS101", "MATH101"}
    )

    result = registration_decision(student, course)
    assert result == "PREREQUISITES_MISSING"


#TC-18
def test_Total_credits_exactly_18():
    student = Student(
        student_id="S007",
        current_credits=15
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=25
    )

    result = registration_decision(student, course)
    assert result == "REGISTERED"


#TC-19
def test_Total_credits_exceed_18():
    student = Student(
        student_id="S008",
        current_credits=16
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=25
    )

    result = registration_decision(student, course)
    assert result == "CREDIT_LIMIT"


#TC-20
def test_Course_has_available_seat():
    student = Student(student_id="S009")

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=29
    )

    result = registration_decision(student, course)
    assert result == "REGISTERED"


#TC-21
def test_Course_is_full():
    student = Student(student_id="S010")

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=30
    )

    result = registration_decision(student, course)
    assert result == "WAITLISTED"


#TC-22
def test_Dues_priority():
    student = Student(
        student_id="S011",
        outstanding_dues=1,
        current_credits=18,
        registered_courses={"CS201"}
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=30,
        prerequisites={"CS101"}
    )

    result = registration_decision(student, course)
    assert result == "DUES_BLOCK"


#TC-23
def test_Already_registered_priority():
    student = Student(
        student_id="S012",
        outstanding_dues=0,
        current_credits=18,
        registered_courses={"CS201"}
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=30,
        prerequisites={"CS101"}
    )

    result = registration_decision(student, course)
    assert result == "ALREADY_REGISTERED"


#TC-24
def test_Prerequisites_priority():
    student = Student(
        student_id="S013",
        outstanding_dues=0,
        current_credits=18
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=30,
        prerequisites={"CS101"}
    )

    result = registration_decision(student, course)
    assert result == "PREREQUISITES_MISSING"


#TC-25
def test_Credit_limit_priority_over_availability():
    student = Student(
        student_id="S014",
        outstanding_dues=0,
        current_credits=16
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=30
    )

    result = registration_decision(student, course)
    assert result == "CREDIT_LIMIT"


#TC-26
def test_Full_course_after_eligibility_checks():
    student = Student(
        student_id="S015",
        outstanding_dues=0,
        current_credits=12
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=30
    )

    result = registration_decision(student, course)
    assert result == "WAITLISTED"


#TC-27
def test_Available_seat_after_eligibility_checks():
    student = Student(
        student_id="S016",
        outstanding_dues=0,
        current_credits=12
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=29
    )

    result = registration_decision(student, course)
    assert result == "REGISTERED"


#TC-28
def test_Decision_does_not_mutate_objects():
    student = Student(
        student_id="S017",
        current_credits=12
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=25
    )

    result = registration_decision(student, course)

    assert result == "REGISTERED"
    assert student.current_credits == 12
    assert student.registered_courses == set()
    assert course.enrolled == 25


#TC-29
def test_Successful_registration_updates_state():
    student = Student(
        student_id="S018",
        current_credits=12
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=25
    )

    result = register_course(student, course)

    assert result == "REGISTERED"
    assert "CS201" in student.registered_courses
    assert student.current_credits == 15
    assert course.enrolled == 26


#TC-30
def test_Add_student_to_waitlist():
    student = Student(student_id="S019")

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=30
    )

    result = register_course(student, course)

    assert result == "WAITLISTED"
    assert "S019" in course.waitlist
    assert student.current_credits == 0
    assert student.registered_courses == set()
    assert course.enrolled == 30


#TC-31
def test_Avoid_duplicate_waitlist_entry():
    student = Student(student_id="S020")

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=30,
        waitlist=["S020"]
    )

    result = register_course(student, course)

    assert result == "WAITLISTED"
    assert course.waitlist.count("S020") == 1


#TC-32
def test_Failed_registration_does_not_mutate_state():
    student = Student(
        student_id="S021",
        outstanding_dues=1,
        current_credits=12
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=25
    )

    result = register_course(student, course)

    assert result == "DUES_BLOCK"
    assert student.current_credits == 12
    assert student.registered_courses == set()
    assert course.enrolled == 25
    assert course.waitlist == []


#TC-33
def test_Withdraw_registered_course():
    student = Student(
        student_id="S022",
        current_credits=6,
        registered_courses={"CS201"}
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=5
    )

    result = withdraw_course(student, course)

    assert result == True
    assert "CS201" not in student.registered_courses
    assert student.current_credits == 3
    assert course.enrolled == 4


#TC-34
def test_Withdraw_unregistered_course():
    student = Student(
        student_id="S023",
        current_credits=6
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=5
    )

    result = withdraw_course(student, course)

    assert result == False
    assert student.current_credits == 6
    assert student.registered_courses == set()
    assert course.enrolled == 5


#TC-35
def test_Negative_dues_rejected():
    student = Student(
        student_id="S024",
        outstanding_dues=-1
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=5
    )

    with pytest.raises(ValueError, match="Invalid dues"):
        registration_decision(student, course)


#TC-36
def test_Capacity_below_minimum():
    student = Student(
        student_id="S025",
        outstanding_dues=0
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=0,
        enrolled=0
    )

    with pytest.raises(
        ValueError,
        match="Invalid capacity or enrollment"
    ):
        registration_decision(student, course)


#TC-37
def test_Negative_enrollment():
    student = Student(
        student_id="S026",
        outstanding_dues=0
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=5,
        enrolled=-1
    )

    with pytest.raises(
        ValueError,
        match="Invalid capacity or enrollment"
    ):
        registration_decision(student, course)


#TC-38
def test_Enrollment_exceeds_capacity():
    student = Student(
        student_id="S027",
        outstanding_dues=0
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=5,
        enrolled=6
    )

    with pytest.raises(
        ValueError,
        match="Invalid capacity or enrollment"
    ):
        registration_decision(student, course)


#TC-39
def test_Valid_dues_capacity_enrollment():
    student = Student(
        student_id="S028",
        outstanding_dues=0
    )

    course = Course(
        code="CS201",
        credit_hours=3,
        capacity=5,
        enrolled=3
    )

    result = registration_decision(student, course)
    assert result == "REGISTERED"
