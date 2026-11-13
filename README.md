
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

**Status: Pending**

Planned activities:

- Control Flow Graph (CFG)
- Cyclomatic Complexity
- Statement Coverage
- Branch Coverage
- Condition Coverage
- MC/DC Testing
- White-box Pytest test cases

## GitHub Collaboration

Git and GitHub are used for version control and team collaboration.

Planned collaboration activities include:

- Feature branches
- Meaningful commits
- GitHub Issues
- Pull Requests
- GitHub Actions

## Important Note

Expected results are derived from the system requirements, not from the existing implementation.

Failing tests are recorded honestly. Any defect fixes will be performed separately through a Pull Request with regression tests.

---

**Course:** SE3002 Software Quality Engineering
**Assignment:** Assignment 2 — System Under Test
**Project:** Student Course Registration Module
