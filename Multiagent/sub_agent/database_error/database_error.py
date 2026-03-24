import re

def detect_database_error(log: str):
    log_lower = log.lower()

    score = 0
    category = None

    # 🔥 CONNECTION ERRORS
    connection_patterns = [
        "database connection failed",
        "cannot connect to database",
        "connection to db failed",
        "too many connections",
        "connection pool exhausted",
        "max connections reached",
        "connection refused",
        "db unreachable"
    ]

    # 🔥 AUTH ERRORS
    auth_patterns = [
        "access denied",
        "authentication failed",
        "invalid credentials",
        "login failed",
        "password incorrect",
        "user not found"
    ]

    # 🔥 QUERY / SYNTAX
    query_patterns = [
        "sql syntax error",
        "syntax error at or near",
        "invalid query",
        "malformed query",
        "query failed",
        "unknown column",
        "unknown table",
        "table does not exist",
        "column not found"
    ]

    # 🔥 CONSTRAINT ERRORS
    constraint_patterns = [
        "duplicate entry",
        "duplicate key",
        "unique constraint",
        "primary key violation",
        "foreign key constraint",
        "constraint violation",
        "cannot insert null"
    ]

    # 🔥 TRANSACTION / LOCK
    transaction_patterns = [
        "deadlock detected",
        "lock wait timeout",
        "transaction aborted",
        "transaction rollback",
        "could not serialize",
        "lock timeout"
    ]

    # 🔥 TIMEOUT / PERFORMANCE
    performance_patterns = [
        "query timeout",
        "statement timeout",
        "execution timeout",
        "slow query",
        "long running query"
    ]

    # 🔥 STORAGE / RESOURCE
    storage_patterns = [
        "tablespace full",
        "disk full",
        "no space left",
        "database full",
        "log file full"
    ]

    # 🔥 REPLICATION / CLUSTER
    replication_patterns = [
        "replication failed",
        "replica lag",
        "node not synced",
        "cluster down",
        "failover failed"
    ]

    # 🔥 NOSQL / GENERIC
    nosql_patterns = [
        "document not found",
        "key not found",
        "collection not found",
        "index not found",
        "cursor error"
    ]

    # 🔥 DB-SPECIFIC SIGNATURES (VERY IMPORTANT)
    db_signatures = [
        "sqlstate",
        "ora-",
        "psql:",
        "mysql",
        "postgres",
        "mongodb",
        "redis",
        "cassandra"
    ]

    # 🔹 Matcher
    def match(patterns, weight, label):
        nonlocal score, category
        for p in patterns:
            if p in log_lower:
                score += weight
                category = label

    match(connection_patterns, 3, "DB_CONNECTION_ERROR")
    match(auth_patterns, 3, "DB_AUTH_ERROR")
    match(query_patterns, 3, "DB_QUERY_ERROR")
    match(constraint_patterns, 3, "DB_CONSTRAINT_ERROR")
    match(transaction_patterns, 3, "DB_TRANSACTION_ERROR")
    match(performance_patterns, 2, "DB_TIMEOUT_PERFORMANCE")
    match(storage_patterns, 3, "DB_STORAGE_ERROR")
    match(replication_patterns, 2, "DB_REPLICATION_ERROR")
    match(nosql_patterns, 2, "DB_NOSQL_ERROR")
    match(db_signatures, 1, "DB_GENERIC_ERROR")

    # 🔥 SQL error codes (universal)
    if re.search(r'\b\d{4,5}\b', log):  # e.g., 1062, 23505
        score += 1

    # 🔥 SQLSTATE pattern
    if re.search(r'sqlstate\s*\[?\w+\]?', log_lower):
        score += 2
        category = "DB_SQLSTATE_ERROR"

    # 🔥 JSON DB error (API responses)
    if '"sql"' in log_lower or '"query"' in log_lower:
        score += 1

    # 🔥 Final decision
    if score >= 2:
        return {
            "is_database_error": True,
            "category": category,
            "confidence": score
        }

    return {
        "is_database_error": False,
        "category": None,
        "confidence": score
    }