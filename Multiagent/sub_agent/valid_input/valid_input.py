import re

def detect_validation_error(log: str):
    log_lower = log.lower()

    score = 0
    category = None

    # 🔥 REQUIRED / MISSING FIELD
    required_patterns = [
        "required field",
        "field is required",
        "missing parameter",
        "missing field",
        "cannot be null",
        "null value not allowed",
        "field cannot be empty"
    ]

    # 🔥 FORMAT ERRORS
    format_patterns = [
        "invalid format",
        "invalid email",
        "invalid url",
        "invalid date",
        "invalid json",
        "invalid xml",
        "invalid uuid",
        "malformed",
        "parse error"
    ]

    # 🔥 LENGTH / SIZE
    length_patterns = [
        "too short",
        "too long",
        "max length",
        "min length",
        "length exceeded",
        "size exceeded"
    ]

    # 🔥 RANGE / VALUE
    range_patterns = [
        "out of range",
        "too large",
        "too small",
        "greater than allowed",
        "less than allowed",
        "invalid value"
    ]

    # 🔥 TYPE ERRORS
    type_patterns = [
        "type mismatch",
        "invalid type",
        "expected",
        "received",
        "cannot convert",
        "conversion failed"
    ]

    # 🔥 PATTERN / REGEX
    pattern_patterns = [
        "pattern mismatch",
        "regex failed",
        "invalid pattern",
        "does not match pattern"
    ]

    # 🔥 BUSINESS LOGIC
    business_patterns = [
        "constraint violation",
        "duplicate value",
        "already exists",
        "business rule violation",
        "state invalid",
        "invalid state transition"
    ]

    # 🔥 FILE / INPUT VALIDATION
    file_patterns = [
        "invalid file",
        "file too large",
        "file type not allowed",
        "mime type mismatch",
        "file corrupted"
    ]

    # 🔥 SECURITY VALIDATION
    security_patterns = [
        "sql injection",
        "xss",
        "malicious input",
        "invalid payload",
        "sanitization failed",
        "suspicious input"
    ]

    # 🔥 ENUM / LIST
    enum_patterns = [
        "invalid enum",
        "value not allowed",
        "unsupported value",
        "not in allowed list"
    ]

    # 🔥 SCHEMA VALIDATION
    schema_patterns = [
        "schema validation failed",
        "json schema failed",
        "property not allowed",
        "additional property",
        "missing required property"
    ]

    # 🔥 HTTP VALIDATION (API)
    http_patterns = [
        "400 bad request",
        "422 unprocessable entity",
        "validation failed"
    ]

    # 🔹 matcher
    def match(patterns, weight, label):
        nonlocal score, category
        for p in patterns:
            if p in log_lower:
                score += weight
                category = label

    match(required_patterns, 3, "REQUIRED_FIELD_ERROR")
    match(format_patterns, 3, "FORMAT_ERROR")
    match(length_patterns, 2, "LENGTH_ERROR")
    match(range_patterns, 2, "RANGE_ERROR")
    match(type_patterns, 2, "TYPE_ERROR")
    match(pattern_patterns, 2, "PATTERN_ERROR")
    match(business_patterns, 3, "BUSINESS_VALIDATION_ERROR")
    match(file_patterns, 2, "FILE_VALIDATION_ERROR")
    match(security_patterns, 3, "SECURITY_VALIDATION_ERROR")
    match(enum_patterns, 2, "ENUM_VALIDATION_ERROR")
    match(schema_patterns, 3, "SCHEMA_VALIDATION_ERROR")
    match(http_patterns, 2, "HTTP_VALIDATION_ERROR")

    # 🔥 STRUCTURAL DETECTION (very powerful)
    if re.search(r'field .* is required', log_lower):
        score += 3
        category = "REQUIRED_FIELD_ERROR"

    if re.search(r'invalid .* format', log_lower):
        score += 3
        category = "FORMAT_ERROR"

    if re.search(r'value .* (too short|too long)', log_lower):
        score += 2
        category = "LENGTH_ERROR"

    if re.search(r'must be .*', log_lower):
        score += 2  # common validation pattern

    # 🔥 JSON validation response detection
    if '"errors"' in log_lower and '"field"' in log_lower:
        score += 3
        category = "STRUCTURED_VALIDATION_ERROR"

    # 🔥 FINAL DECISION
    if score >= 2:
        return {
            "is_validation_error": True,
            "category": category,
            "confidence": score
        }

    return {
        "is_validation_error": False,
        "category": None,
        "confidence": score
    }