import re
from Multiagent.find_files.find_files import workspace_scanner_agent
from Multiagent.log_filter.log_filter import log_filter_agent

state = {}

state.update(workspace_scanner_agent(state))
state.update(log_filter_agent(state))

record = state["errors"]
log = record[0]["content"]

def detect_code_error(log: str):
    log_lower = log.lower()

    score = 0

    # Strong signals
    strong_patterns = [
        "exception",
        "traceback",
        "stack trace",
        "fatal",
        "failed"
    ]

    #  Medium signals
    medium_patterns = [
        " error ",
        "runtime",
        "syntax",
        "undefined",
        "nullpointer",
        "typeerror",
        "attributeerror",
        "keyerror",
        "indexerror",
        "importerror",
        "valueerror",
        "zerodivisionerror",
        "rangeerror"
        
    ]

    # Structural patterns (VERY IMPORTANT)
    structural_patterns = [
        r'file ".*?", line \d+',         # Python
        r'at .*\(.*:\d+:\d+\)',         # Node.js
        r'at .*\(.*\.java:\d+\)',       # Java
        r'line \d+'                     # generic
    ]

    # Count strong signals
    for p in strong_patterns:
        if p in log_lower:
            score += 2

    # Count medium signals
    for p in medium_patterns:
        if p in log_lower:
            score += 1

    # Match structural patterns
    for pattern in structural_patterns:
        if re.search(pattern, log):
            score += 2

    #  Decision threshold
    if score >= 2:
        return "code-level error"
    else:
        return None

temp = detect_code_error(log)
print(temp)