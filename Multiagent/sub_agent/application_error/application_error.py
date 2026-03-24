class ApplicationErrorClassifier:

    def __init__(self):
        self.error_map = {
            "APP-001": ["business rule violation", "insufficient balance", "limit exceeded"],
            "APP-002": ["invalid state transition", "status change not allowed"],
            "APP-003": ["not found", "does not exist"],
            "APP-004": ["duplicate", "already exists"],
            "APP-005": ["quota exceeded", "usage limit"],
            "APP-006": ["feature not enabled"],
            "APP-007": ["validation failed", "invalid input", "invalid form"],
            "APP-008": ["timeout", "operation exceeded time"],
            "APP-009": ["dependency failed", "external service error"],
            "APP-010": ["configuration error", "misconfigured"]
        }

    def classify_error(self, log_line: str) -> str:
        log_line = log_line.lower()

        for code, keywords in self.error_map.items():
            for keyword in keywords:
                if keyword in log_line:
                    return code

        return "APP-000"  # Unknown error

    def get_error_response(self, code: str, message: str):
        return {
            "status": 422,
            "error": "application_error",
            "code": code,
            "message": message
        }

    def process_log(self, log_line: str):
        code = self.classify_error(log_line)
        return self.get_error_response(code, log_line)