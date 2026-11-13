
# SE3002 Assignment 2 — Student Registration Module

## Project Overview

This project is part of **SE3002 Software Quality Engineering – Assignment 2**.

The Student Registration Module is the **System Under Test (SUT)**. The purpose of this assignment is to perform Black-box and White-box testing on the provided Python application, identify defects, and document testing results.

This is not a reference-correct solution. Some test cases may fail intentionally because of defects in the supplied implementation.

## Project Structure

```text
student-course-registration-testing/
│
├── registration.py
├── REQUIREMENTS.md
├── requirements.txt
├── README.md
│
├── tests/
│   ├── test_blackbox.py
│   └── test_whitebox.py
│
└── documentation/
    ├── ECP.xlsx
    ├── BVA.xlsx
    |── Bug_report.xlsx
    ├── Decision_Table.xlsx
    ├── Black_Box_Test_Cases.xlsx
    └── Bug_Report.xlsx
```

*Note: The documentation folder and filenames should match the actual files in the repository.*

## Technologies Used

- Python
- Pytest
- Git and GitHub
- Excel

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Open the Project Directory

```bash
cd student-course-registration-testing
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

**Windows CMD:**

```bash
venv\Scripts\activate
```

**PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Running the Application

Run the following command to check the registration module:

```bash
python -c "from registration import Student, Course, register_course; print(register_course(Student('S001'), Course('CS201', 3, 30)))"
```

## Testing

Tests are implemented using Pytest.

Run all tests from the project root directory:

```bash
python -m pytest -v
```

Run only Black-box tests:

```bash
python -m pytest tests/test_blackbox.py -v
```

## Black-box Testing

Black-box testing is performed using the requirements documented in `REQUIREMENTS.md`, without relying on implementation behavior to determine expected results.

Testing techniques used:

- Equivalence Class Partitioning (ECP)
- Boundary Value Analysis (BVA)
- Decision Table Testing
- State Change Testing

### Test Execution Results

| Result           | Count |
| ---------------- | ----: |
| Total Test Cases |    39 |
| Passed           |    27 |
| Failed           |    12 |

### Identified Defects

Five implementation defects were identified:

1. Credit limit incorrectly rejects exactly 18 credits.
2. Prerequisite validation accepts a student who has completed only one of multiple required prerequisites.
3. Registration is blocked only when outstanding dues exceed 1000 instead of any positive amount.
4. A full course does not correctly place eligible students on the waiting list.
5. Course enrollment is not decremented after withdrawal.

The original `registration.py` is kept unchanged during initial testing. Failed test cases and defects are documented according to the specified requirements.

## White-box Testing

White-box testing was performed on the `registration_decision()` function to analyze its control flow, decision complexity, and condition-level behavior.

### Testing Activities

The following techniques were used:

- Control Flow Graph (CFG)
- Cyclomatic Complexity
- Independent Basis Path Testing
- Condition Coverage
- Modified Condition/Decision Coverage (MC/DC)

### Control Flow Graph and Cyclomatic Complexity

The CFG was analyzed using an expanded short-circuit evaluation approach.

| Metric | Result |
|---|---:|
| CFG Nodes | 19 |
| CFG Edges | 27 |
| Cyclomatic Complexity | 10 |
| Independent Basis Paths | 10 |

The analysis also identified an unreachable WAITLISTED branch because earlier capacity validation rejects the condition required to reach it.

### Condition Coverage and MC/DC

The compound capacity validation was analyzed using three atomic conditions:

- A: `0 <= course.enrolled`
- B: `course.enrolled <= course.capacity`
- C: `course.capacity < 1`

All three conditions demonstrated both True and False outcomes through the selected test inputs. Three independent-effect pairs were documented for MC/DC, including the short-circuit behavior of Python.

### Test Execution Results

White-box tests were executed using Pytest.

| Result | Count |
|---|---:|
| Total Test Cases | 19 |
| Passed | 13 |
| Failed | 6 |

The six failed tests exposed implementation defects related to outstanding dues, prerequisite validation, credit limits, waiting-list handling, duplicate waiting-list entries, and withdrawal records.

The original implementation was not modified during initial testing. Failed tests were documented against the expected system requirements.

Detailed CFG analysis, basis paths, condition coverage, MC/DC pairs, and test execution results are available in the assignment deliverable documentation.

### B2 – Statement and Branch Coverage

- Measured initial statement and branch coverage using pytest-cov.
- Identified uncovered statements and branches.
- Added additional white-box test cases to improve code coverage.
- Compared initial and final coverage results.

**Coverage Results:**

| Coverage Type | Initial | Final |
|---|---:|---:|
| Statement Coverage | 92.45% | 98.11% |
| Branch Coverage | 80.77% | 96.15% |

### B4 – White-Box Testing

- Created and updated `tests/test_whitebox.py`.
- Added test cases to execute specific branches in the registration system.
- Tested waitlist functionality using pytest monkeypatch.
- Tested different conditions, including dues, prerequisites, credit limits, and course withdrawal.
- Identified existing defects through failed test cases.

### C5 – GitHub Actions

- Created the workflow file `.github/workflows/tests.yml`.
- Configured automatic test execution on every push and pull request.
- Configured Python 3.14 and installed pytest and pytest-cov.
- Generated statement and branch coverage reports.
- Configured GitHub Actions to upload coverage reports as downloadable artifacts.

**Final Combined Test Results:**

| Result | Count |
|---|---:|
| Total Tests | 61 |
| Passed | 43 |
| Failed | 18 |

The failing tests were preserved because they revealed defects in the original implementation. The implementation code was not modified during the initial testing and coverage evaluation.

### Files Worked On

- `tests/test_whitebox.py`
- `.github/workflows/tests.yml`
- `initial_coverage.json`
- `updated_coverage.json`
