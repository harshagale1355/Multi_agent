import re

def detect_timeout_availability(log: str):
    log_lower = log.lower()

    score = 0
    category = None

    # 🔥 TIMEOUT PATTERNS
    timeout_patterns = [
        "timeout", "timed out", "time out",
        "deadline exceeded",          # gRPC
        "request timeout",
        "connection timeout",
        "read timeout",
        "write timeout",
        "operation timed out",
        "execution timed out",
        "wait timeout",
        "lock timeout",
        "context deadline exceeded"
    ]

    # 🔥 AVAILABILITY PATTERNS (service not reachable)
    availability_patterns = [
        "service unavailable",
        "unreachable",
        "connection refused",
        "connection failed",
        "host down",
        "server down",
        "not responding",
        "no healthy upstream",
        "upstream failure",
        "backend down",
        "dependency failed",
        "health check failed",
        "not ready",
        "pod not ready",
        "node not ready",
        "target unavailable"
    ]

    # 🔥 HTTP STATUS (availability signals)
    http_patterns = [
        " 503 ", " 502 ", " 504 ",
        "bad gateway",
        "gateway timeout",
        "service unavailable"
    ]

    # 🔥 DNS / endpoint availability
    dns_patterns = [
        "dns failure",
        "resolve failed",
        "host not found",
        "name resolution failed"
    ]

    # 🔥 RATE LIMIT / THROTTLING (availability degradation)
    throttle_patterns = [
        "rate limit exceeded",
        "too many requests",
        "throttled",
        "quota exceeded"
    ]

    # 🔹 Pattern matcher
    def match(patterns, weight, label):
        nonlocal score, category
        for p in patterns:
            if p in log_lower:
                score += weight
                category = label

    match(timeout_patterns, 3, "TIMEOUT_ERROR")
    match(availability_patterns, 3, "AVAILABILITY_ERROR")
    match(http_patterns, 2, "SERVICE_AVAILABILITY")
    match(dns_patterns, 2, "DNS_AVAILABILITY")
    match(throttle_patterns, 2, "THROTTLING")

    # 🔥 Structural timeout patterns
    if re.search(r'\b\d+ms timeout\b', log_lower):
        score += 2
        category = "TIMEOUT_ERROR"

    if re.search(r'timeout after \d+', log_lower):
        score += 2
        category = "TIMEOUT_ERROR"

    # 🔥 Final decision
    if score >= 2:
        return {
            "is_timeout_or_availability": True,
            "category": category,
            "confidence": score
        }

    return {
        "is_timeout_or_availability": False,
        "category": None,
        "confidence": score
    }