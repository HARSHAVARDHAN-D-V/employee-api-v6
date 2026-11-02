NOT_FOUND_RESPONSE = {404: {"description": "Employee not found"}}

BAD_REQUEST_RESPONSE = {
    400: {
        "description": "Data breaks a rule: bad emp_no format, salary not positive, or no fields provided"
    }
}

DUPLICATE_RESPONSE = {409: {"description": "An employee with this emp_no already exists"}}