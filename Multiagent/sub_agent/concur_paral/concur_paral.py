import re

# -------------------------------
# Concurrency Error Patterns
# -------------------------------
CATEGORIES = {
    "deadlock": [
        r"deadlock", r"dead lock", r"circular wait", r"lock cycle"
    ],
    "lock_error": [
        r"lock timeout", r"lock failed", r"lock not available",
        r"mutex", r"semaphore", r"rwlock", r"spinlock", r"lock contention"
    ],
    "race_condition": [
        r"race condition", r"data race", r"concurrent write",
        r"stale data", r"lost update"
    ],
    "thread_error": [
        r"thread failed", r"thread error", r"thread aborted",
        r"thread interrupted", r"cannot create thread",
        r"thread limit", r"thread starvation"
    ],
    "thread_pool": [
        r"thread pool exhausted", r"task rejected",
        r"no available threads", r"queue full", r"executor rejected"
    ],
    "synchronization": [
        r"monitor wait timeout", r"condition timeout",
        r"barrier broken", r"semaphore timeout"
    ],
    "concurrent_collection": [
        r"concurrentmodificationexception",
        r"collection modified", r"concurrent access"
    ],
    "atomicity": [
        r"atomic operation failed", r"cas failed",
        r"compare and swap", r"partial commit"
    ],
    "parallel_processing": [
        r"parallel task failed", r"forkjoin",
        r"task dependency", r"subtask failed"
    ],
    "async_error": [
        r"future timeout", r"promise rejected",
        r"async timeout", r"await error", r"callback failed"
    ],
    "event_loop": [
        r"event loop blocked", r"event queue full"
    ],
    "distributed_concurrency": [
        r"distributed lock failed", r"leader election failed",
        r"quorum not achieved", r"split brain"
    ],
    "resource_contention": [
        r"contention", r"resource busy", r"cpu starvation",
        r"thrashing", r"io contention"
    ],
    # Fallback
    "generic_error": [
        r"exception", r"error", r"failed", r"failure", r"fatal"
    ]
}

# -------------------------------
# Function to classify log
# -------------------------------
def classify_log(log_line):
    log_line = log_line.lower()

    for category, patterns in CATEGORIES.items():
        for pattern in patterns:
            if re.search(pattern, log_line):
                return category

    return "unknown"


# -------------------------------
# Test logs
# -------------------------------
