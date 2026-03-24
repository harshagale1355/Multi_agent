from Multiagent.find_files.find_files import workspace_scanner_agent
from Multiagent.log_filter.log_filter import log_filter_agent

state = {}

state.update(workspace_scanner_agent(state))
state.update(log_filter_agent(state))

record = state["errors"]
log = record[0]["content"]

def detect_network_error(log):
    log = log.lower()

    patterns = {
        "NETWORK_TIMEOUT": [
            "timeout", "timed out", "etimedout"
        ],
        "CONNECTION_ERROR": [
            "connection refused", "connection reset", "econnrefused", "econnreset"
        ],
        "DNS_ERROR": [
            "dns", "name resolution", "enotfound", "eai_again",
            "host not found", "failed to resolve", "resolve host",
            "no address record"
        ],
        "SERVER_ERROR": [
            "502", "503", "504", "bad gateway", "service unavailable"
        ],
        "SSL_ERROR": [
            "ssl", "tls", "certificate"
        ],
        "NETWORK_UNREACHABLE": [
            "network unreachable", "no route to host"
        ]
    }

    for category, keywords in patterns.items():
        for keyword in keywords:
            if keyword in log:
                return category

    return None


print(detect_network_error(log))