import re
import os
from collections import Counter


ERROR_PATTERNS = {
    r'\bERROR\b': 'General Error',
    r'\bFAIL(ED)?\b': 'Failure',
    r'\bEXCEPTION\b': 'Exception',
    r'\bCRITICAL\b': 'Critical Error',
    r'\bFATAL\b': 'Fatal Error',
    r'\bPANIC\b': 'System Panic',
    r'\bTIMEOUT\b': 'Timeout',
    r'\bDENIED\b': 'Access Denied',
    r'\bREJECTED\b': 'Request Rejected',
    r'\bABORT\b': 'Operation Aborted',
    r'\bSEGMENTATION FAULT\b': 'Segmentation Fault',
    r'\bOUT OF MEMORY\b': 'Out of Memory',
    r'\bSTACK TRACE\b': 'Stack Trace',
    r'\bTRACEBACK\b': 'Python Traceback',
    r'\bUNHANDLED\b': 'Unhandled Error',
    r'HTTP/\d\.\d"\s(5\d\d|4\d\d)': 'HTTP Error',
    r'\s(5\d\d|4\d\d)\s': 'HTTP Status Code',
    r'\[error\]': 'Nginx/Apache Error',
    r'\[emerg\]': 'Emergency Error',
    r'\[crit\]': 'Critical Log',
    r'\[alert\]': 'Alert',
}


def categorize_error(line):

    line_lower = line.lower()

    category_keywords = {
        'database': ['database', 'sql', 'mysql', 'postgres', 'oracle', 'mongodb'],
        'performance': ['timeout', 'slow', 'latency', 'performance'],
        'security': ['auth', 'login', 'password', 'permission', 'access'],
        'resource': ['memory', 'heap', 'disk', 'cpu', 'oom'],
        'network': ['network', 'connection', 'socket', 'http', 'https'],
        'io': ['file', 'read', 'write', 'permission denied', 'file not found'],
        'application': ['exception', 'null pointer', 'type error', 'syntax error']
    }

    for category, keywords in category_keywords.items():
        if any(keyword in line_lower for keyword in keywords):
            return category

    return "application"


def extract_error_code(line):

    http_match = re.search(r'\b(\d{3})\b', line)
    if http_match and http_match.group(1).startswith(('4', '5')):
        return f"HTTP_{http_match.group(1)}"

    patterns = [
        r'ERR[_-](\w+)',
        r'ERROR[_-](\w+)',
        r'code[:\s]+(\w+)',
        r'error\s+code\s*[=:]\s*(\w+)',
        r'\[(\w+)\]'
    ]

    for pattern in patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return match.group(1).upper()

    return None


def process_log_stream(text_stream, selected_patterns):

    errors = []

    stats = {
        "total_lines": 0,
        "error_count": 0,
        "categories": Counter(),
        "error_codes": Counter(),
        "pattern_matches": Counter()
    }

    compiled_patterns = [
        (re.compile(pattern, re.IGNORECASE), desc)
        for pattern, desc in ERROR_PATTERNS.items()
        if pattern in selected_patterns
    ]

    for line_num, line in enumerate(text_stream, 1):

        line = line.rstrip("\n")
        stats["total_lines"] += 1

        matched = False
        matched_pattern = None

        for pattern, desc in compiled_patterns:
            if pattern.search(line):
                matched = True
                matched_pattern = desc
                stats["pattern_matches"][desc] += 1
                break

        if matched:

            stats["error_count"] += 1

            category = categorize_error(line)
            stats["categories"][category] += 1

            error_code = extract_error_code(line)

            if error_code:
                stats["error_codes"][error_code] += 1

            errors.append({
                "line_number": line_num,
                "content": line,
                "category": category,
                "error_code": error_code,
                "matched_pattern": matched_pattern
            })

    return errors, stats


def process_latest_log_file(all_files, selected_patterns=None):

    log_files = [f for f in all_files if f.endswith(".log")]

    if not log_files:
        return [], None

    log_files.sort(reverse=True)

    latest_log = log_files[0]

    if selected_patterns is None:
        selected_patterns = list(ERROR_PATTERNS.keys())

    if not os.path.exists(latest_log):
        latest_log = os.path.join(os.getcwd(), latest_log)

    try:

        with open(latest_log, "r", encoding="utf-8", errors="ignore") as file:

            errors, stats = process_log_stream(
                file,
                selected_patterns
            )

        file_name = os.path.basename(latest_log)

        for error in errors:
            error["file"] = file_name
            error["file_path"] = latest_log

        return errors, stats

    except Exception:
        return [], None


def log_filter_agent(state):
    """
    Agent that extracts errors from the latest log file
    """

    all_files = state["all_files"]

    errors, stats = process_latest_log_file(all_files)

    return {
        "errors": errors,
        "log_stats": stats,
    }
