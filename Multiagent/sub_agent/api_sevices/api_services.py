import re

def detect_api_service_error(log: str):
    log_lower = log.lower()

    score = 0
    category = None

    # 🔥 HTTP STATUS CODES
    http_4xx = [
        "400", "401", "403", "404", "405", "408", "409",
        "410", "413", "415", "422", "429"
    ]

    http_5xx = [
        "500", "501", "502", "503", "504"
    ]

    # 🔥 AUTHENTICATION / AUTHORIZATION
    auth_patterns = [
        "unauthorized", "forbidden", "invalid token",
        "token expired", "authentication failed",
        "access denied", "permission denied",
        "invalid api key", "jwt expired"
    ]

    # 🔥 RATE LIMIT / THROTTLING
    rate_patterns = [
        "rate limit exceeded", "too many requests",
        "quota exceeded", "throttled"
    ]

    # 🔥 VALIDATION / DATA ERRORS
    validation_patterns = [
        "validation failed", "invalid input",
        "invalid format", "missing field",
        "bad request", "unprocessable entity"
    ]

    # 🔥 SERVICE COMMUNICATION
    service_patterns = [
        "service unavailable", "upstream failure",
        "no healthy upstream", "backend down",
        "dependency failed", "connection to upstream failed",
        "rpc failed", "grpc error"
    ]

    # 🔥 API GATEWAY / ROUTING
    gateway_patterns = [
        "gateway timeout", "bad gateway",
        "route not found", "endpoint not found",
        "method not allowed"
    ]

    # 🔥 CIRCUIT BREAKER / MICROSERVICE
    microservice_patterns = [
        "circuit open", "circuit breaker",
        "fallback executed", "retry exhausted",
        "service down"
    ]

    # 🔥 GENERIC API ERROR SIGNALS
    generic_patterns = [
        "api error", "request failed",
        "response error", "endpoint unreachable"
    ]

    # 🔹 Matcher
    def match(patterns, weight, label):
        nonlocal score, category
        for p in patterns:
            if p in log_lower:
                score += weight
                category = label

    # Apply matching
    match(http_4xx, 2, "CLIENT_ERROR")
    match(http_5xx, 3, "SERVER_ERROR")
    match(auth_patterns, 3, "AUTH_ERROR")
    match(rate_patterns, 3, "RATE_LIMIT")
    match(validation_patterns, 2, "VALIDATION_ERROR")
    match(service_patterns, 3, "SERVICE_COMMUNICATION_ERROR")
    match(gateway_patterns, 3, "API_GATEWAY_ERROR")
    match(microservice_patterns, 2, "MICROSERVICE_ERROR")
    match(generic_patterns, 1, "API_GENERIC_ERROR")

    # 🔥 Structural detection (HTTP codes in logs)
    if re.search(r'\b(4\d{2}|5\d{2})\b', log):
        score += 2

    # 🔥 JSON error pattern (common API response)
    if '"error"' in log_lower and '"message"' in log_lower:
        score += 2
        category = "API_RESPONSE_ERROR"

    # 🔥 Final decision
    if score >= 2:
        return {
            "is_api_service_error": True,
            "category": category,
            "confidence": score
        }

    return {
        "is_api_service_error": False,
        "category": None,
        "confidence": score
    }