import re

def detect_auth_error(log: str):
    log_lower = log.lower()

    score = 0
    category = None

    # 🔥 AUTHENTICATION (who you are)
    auth_patterns = [
        "authentication failed",
        "invalid credentials",
        "invalid username",
        "invalid password",
        "login failed",
        "user not found",
        "account locked",
        "account disabled",
        "too many failed attempts"
    ]

    # 🔥 TOKEN / JWT / API KEY
    token_patterns = [
        "invalid token",
        "token expired",
        "token revoked",
        "token missing",
        "jwt expired",
        "jwt malformed",
        "invalid signature",
        "api key invalid",
        "api key missing",
        "api key expired"
    ]

    # 🔥 AUTHORIZATION (what you can access)
    authorization_patterns = [
        "access denied",
        "permission denied",
        "forbidden",
        "not authorized",
        "insufficient permissions",
        "operation not permitted",
        "scope invalid",
        "insufficient scope"
    ]

    # 🔥 SESSION ERRORS
    session_patterns = [
        "session expired",
        "invalid session",
        "session not found",
        "session timeout"
    ]

    # 🔥 OAUTH / SSO
    oauth_patterns = [
        "invalid grant",
        "unauthorized client",
        "invalid scope",
        "authorization code expired",
        "oauth error"
    ]

    # 🔥 MFA / SECURITY
    security_patterns = [
        "mfa failed",
        "invalid mfa code",
        "authentication required",
        "suspicious activity",
        "security violation"
    ]

    # 🔥 RATE LIMIT (auth related)
    rate_patterns = [
        "too many requests",
        "rate limit exceeded",
        "quota exceeded"
    ]

    # 🔥 HTTP AUTH STATUS
    http_auth_patterns = [
        " 401 ",
        " 403 ",
        "unauthorized",
        "forbidden"
    ]

    # 🔹 Matcher
    def match(patterns, weight, label):
        nonlocal score, category
        for p in patterns:
            if p in log_lower:
                score += weight
                category = label

    match(auth_patterns, 3, "AUTHENTICATION_ERROR")
    match(token_patterns, 3, "TOKEN_ERROR")
    match(authorization_patterns, 3, "AUTHORIZATION_ERROR")
    match(session_patterns, 2, "SESSION_ERROR")
    match(oauth_patterns, 2, "OAUTH_ERROR")
    match(security_patterns, 2, "SECURITY_ERROR")
    match(rate_patterns, 2, "AUTH_RATE_LIMIT")
    match(http_auth_patterns, 2, "HTTP_AUTH_ERROR")

    # 🔥 Structural detection (headers / JWT style)
    if re.search(r'www-authenticate', log_lower):
        score += 2
        category = "AUTH_HEADER_ERROR"

    # 🔥 JSON auth error
    if '"error"' in log_lower and "token" in log_lower:
        score += 2

    # 🔥 Final decision
    if score >= 2:
        return {
            "is_auth_error": True,
            "category": category,
            "confidence": score
        }

    return {
        "is_auth_error": False,
        "category": None,
        "confidence": score
    }