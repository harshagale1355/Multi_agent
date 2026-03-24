import re

def detect_security_error(log: str):
    log_lower = log.lower()

    score = 0
    category = None

    # 🔥 SQL INJECTION
    sql_patterns = [
        "sql injection",
        "union select",
        "or 1=1",
        "' or '1'='1",
        "information_schema",
        "sqlmap",
        "database error"
    ]

    # 🔥 XSS
    xss_patterns = [
        "<script>",
        "xss",
        "cross-site scripting",
        "javascript:",
        "onerror=",
        "alert(",
        "document.cookie"
    ]

    # 🔥 COMMAND / CODE INJECTION
    command_patterns = [
        "command injection",
        "os command",
        "eval(",
        "exec(",
        "system(",
        "base64_decode",
        "shell execution"
    ]

    # 🔥 PATH TRAVERSAL
    path_patterns = [
        "../",
        "..\\",
        "/etc/passwd",
        "directory traversal",
        "path traversal"
    ]

    # 🔥 SSRF
    ssrf_patterns = [
        "ssrf",
        "169.254.169.254",
        "metadata",
        "internal service",
        "localhost access"
    ]

    # 🔥 AUTH ATTACKS
    auth_attack_patterns = [
        "brute force",
        "too many login attempts",
        "credential stuffing",
        "password spraying",
        "account locked"
    ]

    # 🔥 TOKEN / JWT ATTACK
    token_patterns = [
        "jwt tampering",
        "invalid signature",
        "token replay",
        "token manipulation"
    ]

    # 🔥 DOS / FLOOD
    dos_patterns = [
        "request flood",
        "ddos",
        "rate limit exceeded",
        "too many requests",
        "connection flood"
    ]

    # 🔥 SECURITY MISCONFIG
    misconfig_patterns = [
        "debug mode enabled",
        "stack trace exposed",
        "information disclosure",
        "default credentials",
        "directory listing"
    ]

    # 🔥 DATA EXPOSURE
    data_patterns = [
        "pii exposed",
        "sensitive data",
        "password in log",
        "api key exposed",
        "token leaked"
    ]

    # 🔥 MALWARE / PAYLOAD
    malware_patterns = [
        "malware detected",
        "trojan",
        "backdoor",
        "web shell",
        "suspicious payload"
    ]

    # 🔥 NETWORK ATTACKS
    network_patterns = [
        "port scan",
        "arp spoofing",
        "dns spoofing",
        "syn flood",
        "icmp flood"
    ]

    # 🔹 matcher
    def match(patterns, weight, label):
        nonlocal score, category
        for p in patterns:
            if p in log_lower:
                score += weight
                category = label

    match(sql_patterns, 4, "SQL_INJECTION")
    match(xss_patterns, 4, "XSS_ATTACK")
    match(command_patterns, 4, "COMMAND_INJECTION")
    match(path_patterns, 4, "PATH_TRAVERSAL")
    match(ssrf_patterns, 4, "SSRF_ATTACK")
    match(auth_attack_patterns, 3, "AUTH_ATTACK")
    match(token_patterns, 3, "TOKEN_ATTACK")
    match(dos_patterns, 3, "DOS_ATTACK")
    match(misconfig_patterns, 2, "SECURITY_MISCONFIG")
    match(data_patterns, 4, "DATA_EXPOSURE")
    match(malware_patterns, 4, "MALWARE_DETECTED")
    match(network_patterns, 3, "NETWORK_ATTACK")

    # 🔥 STRUCTURAL DETECTION (VERY POWERFUL)
    
    # SQL injection pattern
    if re.search(r"(union\s+select|or\s+1=1|--)", log_lower):
        score += 4
        category = "SQL_INJECTION"

    # XSS pattern
    if re.search(r"<script.*?>", log_lower):
        score += 4
        category = "XSS_ATTACK"

    # Path traversal pattern
    if re.search(r"\.\./", log):
        score += 4
        category = "PATH_TRAVERSAL"

    # Base64 + eval (RCE attempt)
    if re.search(r"eval\(.*base64", log_lower):
        score += 5
        category = "REMOTE_CODE_EXECUTION"

    # Internal metadata access (SSRF strong signal)
    if "169.254.169.254" in log:
        score += 5
        category = "SSRF_ATTACK"

    # WAF / IDS keywords
    if any(x in log_lower for x in ["waf", "ids", "ips", "security alert"]):
        score += 2

    # 🔥 FINAL DECISION
    if score >= 3:
        return {
            "is_security_error": True,
            "category": category,
            "confidence": score
        }

    return {
        "is_security_error": False,
        "category": None,
        "confidence": score
    }