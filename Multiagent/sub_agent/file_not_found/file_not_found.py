from Multiagent.find_files.find_files import workspace_scanner_agent
from Multiagent.log_filter.log_filter import log_filter_agent

import os 

state = {}

state.update(workspace_scanner_agent(state))
state.update(log_filter_agent(state))

all_files_path = state["all_files"]
record = state["errors"]
log = record[0]["content"]

all_file_names = [os.path.basename(p) for p in all_files_path]

import re

def detect_file_not_found(log: str):
    log_lower = log.lower()

    # 🔹 Universal patterns
    patterns = [
        "file not found",
        "filenotfounderror",        # Python
        "filenotfoundexception",    # Java
        "no such file or directory",
        "could not find file",
        "enoent",                   # Node/Linux
        "cannot find file",
        "failed to open file",
        "failed to read file"
    ]

    # 🔹 Detection
    is_error = any(p in log_lower for p in patterns)

    # 🔹 Extract file names
    files = set()

    # 1. Files inside quotes
    matches1 = re.findall(r"'([^']+\.[a-zA-Z0-9]+)'", log)

    # 2. Java / generic (no quotes after exception)
    matches2 = re.findall(r'filenotfoundexception:\s*([^\s]+)', log_lower)

    # 3. ENOENT style
    matches3 = re.findall(r'enoent.*?([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)', log_lower)

    # 4. General fallback (file.ext anywhere)
    matches4 = re.findall(r'\b([a-zA-Z0-9_\-]+\.(json|yml|yaml|txt|csv|xml|log))\b', log)

    # Clean tuple results
    def clean(matches):
        result = []
        for m in matches:
            if isinstance(m, tuple):
                result.append(m[0])
            else:
                result.append(m)
        return result

    files.update(clean(matches1))
    files.update(clean(matches2))
    files.update(clean(matches3))
    files.update(clean(matches4))

    return {
        "is_file_not_found": is_error,
        "files": list(files)
    }


test_file = detect_file_not_found(log)

print(test_file)

def found_error(state):

    main_error=detect_file_not_found(log)

    return{
        "main_error":main_error    
    }

    


