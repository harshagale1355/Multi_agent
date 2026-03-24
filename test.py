from Multiagent.find_files.find_files import workspace_scanner_agent
from Multiagent.log_filter.log_filter import log_filter_agent
from Multiagent.find_files.find_files import refers_to_same_file
from Multiagent.find_files.find_files import find_all_files


state = {}

state.update(workspace_scanner_agent(state))
state.update(log_filter_agent(state))

record = state["errors"]
#print(record)
error = record[0]["content"]

important_extensions = ['.py', '.html', '.htm', '.js', '.css', '.json', 
                       '.xml', '.yaml', '.yml', '.md', '.txt', '.csv', 
                        '.ipynb', '.php', '.java', '.cpp', '.c', '.h', 
                        '.rb', '.go', '.rs', '.swift', '.kt', '.sh', 
                        '.bat', '.ps1', '.md', '.rst', '.ini', '.cfg', 
                        '.conf', '.toml', '.sql', '.db', '.sqlite3']

runtime_errors = ["TypeError", "ValueError", "IndexError", "KeyError",
                  "ZeroDivisionError", "FileNotFoundError", "ModuleNotFoundError",
                  "AttributeError", "MemoryError", "NullPointerException",
                  "ArrayIndexOutOfBoundsException", "ArithmeticException",
                  "ClassCastException", "IllegalArgumentException",
                  "NumberFormatException", "ReferenceError", "RangeError",
                  "SyntaxError", "URIError", "EvalError", "AggregateError"]

syntax_error = ["SyntaxError","IndentationError","TabError","Syntax error"," ';' expected",
                "illegal start of expression","class, interface, or enum expected","SyntaxError",
                "Unexpected token","Unexpected identifier","Missing ) after argument list","Unexpected end of input"]

compilation_error = ["cannot find symbol","';' expected","illegal start of expression","incompatible types",
                    "class not found","package does not exist","method not found"]
            
memory_errors = [
    "MemoryError", "OutOfMemoryError", "std::bad_alloc",
    "heap overflow", "stack overflow", "buffer overflow",
    "segmentation fault", "core dumped", "memory leak"
]

file_system_errors = [
    "FileNotFoundError", "No such file or directory",
    "Permission denied", "Is a directory", "Not a directory",
    "Disk full", "Read-only file system",
    "Input/output error", "File exists", "Path not found"
]

network_errors = [
    "ConnectionError", "Connection refused", "Connection reset",
    "Connection timed out", "TimeoutError", "Network is unreachable",
    "Host unreachable", "DNS lookup failed",
    "Broken pipe", "SSL error"
]

database_errors = [
    "DatabaseError", "OperationalError", "IntegrityError",
    "ProgrammingError", "DataError",
    "connection failed", "too many connections",
    "deadlock detected", "constraint violation",
    "duplicate key", "syntax error in SQL"
]

auth_errors = [
    "AuthenticationError", "AuthorizationError",
    "Access denied", "Unauthorized", "Forbidden",
    "Invalid credentials", "Token expired",
    "Permission denied", "Login failed"
]

api_errors = [
    "400 Bad Request", "401 Unauthorized", "403 Forbidden",
    "404 Not Found", "405 Method Not Allowed",
    "408 Request Timeout", "429 Too Many Requests",
    "500 Internal Server Error", "502 Bad Gateway",
    "503 Service Unavailable", "504 Gateway Timeout"
]

dependency_errors = [
    "ModuleNotFoundError", "ImportError",
    "No module named", "Cannot find module",
    "Package not found", "Dependency not found",
    "Version mismatch", "Failed to resolve dependency"
]

config_errors = [
    "ConfigurationError", "Invalid configuration",
    "Missing configuration", "Invalid config file",
    "Environment variable not set",
    "KeyError", "ValueError",
    "Invalid value", "Missing required field"
]

error_categories = {
    "runtime": runtime_errors,
    "syntax": syntax_error,
    "compilation": compilation_error,
    "memory": memory_errors,
    "file_system": file_system_errors,
    "network": network_errors,
    "database": database_errors,
    "auth": auth_errors,
    "api": api_errors,
    "dependency": dependency_errors,
    "config": config_errors
}


def identify_error(error_categories, error):
    error = error.lower()
    scores = {}

    for category, patterns in error_categories.items():
        scores[category] = sum(
            1 for p in patterns if p.lower() in error
        )

    best_match = max(scores, key=scores.get)

    return best_match if scores[best_match] > 0 else "unknown"




'''
if record:
    error = record[0]["content"]
    ans = identify_error(error_categories, error)
    print(ans)
else:
    print("No errors found")

'''

import re

def extract_all_file_references(log_line):
    """
    Extract all file references (filename.extension:line) from a log line.
    """
    pattern = r'([\w\-]+\.[\w]+):\d+'
    return re.findall(pattern, log_line)

# Example
log = error
files = extract_all_file_references(log)



import os

all_files = find_all_files()



