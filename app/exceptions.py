class EmployeeNotFoundError(Exception):
    """No employee exists with the given emp_no."""


class DuplicateEmployeeError(Exception):
    """An employee with this emp_no already exists."""


class InvalidEmployeeDataError(Exception):
    """Data breaks a business rule (bad emp_no format, bad salary)."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message