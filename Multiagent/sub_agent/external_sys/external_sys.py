import re

class IntegrationErrorDetector:

    def __init__(self):
        self.patterns = {
            "API_ERRORS": [
                r"endpoint unreachable",
                r"api timeout",
                r"response timeout",
                r"invalid api response",
                r"api version mismatch",
                r"rate limit exceeded",
                r"quota exceeded",
                r"api authentication failed",
                r"api authorization failed",
                r"method not allowed"
            ],

            "PAYMENT_ERRORS": [
                r"payment failed",
                r"transaction declined",
                r"insufficient funds",
                r"card declined",
                r"card expired",
                r"fraud detected",
                r"3d secure failed",
                r"refund failed"
            ],

            "EMAIL_SMS_ERRORS": [
                r"email delivery failed",
                r"smtp connection failed",
                r"sms delivery failed",
                r"invalid email",
                r"invalid phone",
                r"message too long"
            ],

            "CLOUD_ERRORS": [
                r"ec2 unavailable",
                r"s3 bucket not found",
                r"lambda timeout",
                r"rds failover",
                r"blob not found",
                r"cloud run timeout"
            ],

            "QUEUE_ERRORS": [
                r"kafka broker unavailable",
                r"topic not found",
                r"consumer rebalance failed",
                r"offset commit failed",
                r"producer buffer full",
                r"queue full",
                r"connection refused"
            ],

            "DATA_INTEGRATION_ERRORS": [
                r"etl failed",
                r"data conversion error",
                r"data truncation",
                r"duplicate key",
                r"foreign key constraint",
                r"schema mismatch",
                r"replication lag"
            ],

            "FILE_TRANSFER_ERRORS": [
                r"sftp connection failed",
                r"file upload failed",
                r"file download failed",
                r"permission denied",
                r"disk quota exceeded"
            ],

            "SSO_ERRORS": [
                r"idp unavailable",
                r"saml response invalid",
                r"saml assertion expired",
                r"oauth error",
                r"token exchange failed",
                r"ldap bind failed"
            ],

            "WEBHOOK_ERRORS": [
                r"webhook failed",
                r"webhook timeout",
                r"invalid webhook signature",
                r"callback failed",
                r"callback timeout"
            ],

            "DNS_ERRORS": [
                r"dns resolution failed",
                r"dns lookup timeout",
                r"nxdomain",
                r"service not found"
            ],

            "LOAD_BALANCER_ERRORS": [
                r"no healthy targets",
                r"502 bad gateway",
                r"504 gateway timeout",
                r"proxy timeout",
                r"backend connection failed"
            ],

            "RATE_LIMIT_ERRORS": [
                r"rate limit exceeded",
                r"too many requests",
                r"quota exhausted",
                r"retry-after"
            ]
        }

    def detect(self, log_line):
        log_line = log_line.lower()

        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, log_line):
                    return category

        return "UNKNOWN"