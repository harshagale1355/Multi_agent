import re
from Multiagent.find_files.find_files import workspace_scanner_agent
from Multiagent.log_filter.log_filter import log_filter_agent

state = {}

state.update(workspace_scanner_agent(state))
state.update(log_filter_agent(state))

record = state["errors"]
log = record[0]["content"]

def detect_system_resource_error(log: str):
    log_lower = log.lower()

    score = 0
    category = None

    # 🔥 MEMORY
    memory_patterns = [
        "out of memory", "oom", "cannot allocate memory",
        "memory exhausted", "heap space", "segmentation fault",
        "stack overflow", "memory leak"
    ]

    # 🔥 DISK / STORAGE
    disk_patterns = [
        "no space left", "disk full", "disk quota exceeded",
        "read-only file system", "i/o error", "disk error",
        "bad sector", "device not ready"
    ]

    # 🔥 CPU / PROCESS
    cpu_patterns = [
        "cpu time exceeded", "process limit", "cannot fork",
        "resource temporarily unavailable", "process limit reached",
        "thread limit", "too many processes"
    ]

    # 🔥 FILE SYSTEM / LIMITS
    file_patterns = [
        "too many open files", "emfile",
        "file limit exceeded", "quota exceeded"
    ]

    # 🔥 NETWORK (resource-level, not logical)
    network_patterns = [
        "connection refused", "network unreachable",
        "connection reset", "connection timeout",
        "dns", "host unreachable"
    ]

    # 🔥 GENERIC RESOURCE SIGNALS (VERY IMPORTANT)
    generic_patterns = [
        "limit exceeded",
        "resource exhausted",
        "resource unavailable",
        "cannot allocate",
        "buffer overflow",
        "queue full",
        "timeout",
        "throttled"
    ]

    # 🔹 Pattern scoring
    def match_patterns(patterns, weight, label):
        nonlocal score, category
        for p in patterns:
            if p in log_lower:
                score += weight
                category = label

    match_patterns(memory_patterns, 3, "MEMORY_ERROR")
    match_patterns(disk_patterns, 3, "DISK_ERROR")
    match_patterns(cpu_patterns, 3, "CPU_PROCESS_ERROR")
    match_patterns(file_patterns, 2, "FILE_SYSTEM_LIMIT")
    match_patterns(network_patterns, 2, "NETWORK_RESOURCE")
    match_patterns(generic_patterns, 1, "RESOURCE_EXHAUSTION")

    # 🔥 Structural signals (OS-level logs)
    if re.search(r'killed process \d+', log_lower):
        score += 3
        category = "OOM_KILL"

    if re.search(r'sig(segv|kill|abrt)', log_lower):
        score += 3
        category = "SYSTEM_SIGNAL_ERROR"

    # 🔥 Final decision
    if score >= 2:
        return {
            "is_system_error": True,
            "category": category,
            "confidence": score
        }

    return {
        "is_system_error": False,
        "category": None,
        "confidence": score
    }

