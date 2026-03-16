import logging
import json
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "request_info"):
            log_record["request"] = record.request_info
        return json.dumps(log_record)

audit_logger = logging.getLogger("api_audit")
audit_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/api_audit.log")
file_handler.setFormatter(JSONLogFormatter())
audit_logger.addHandler(file_handler)

def log_audit(message: str, request_info: dict = None):
    extra = {"request_info": request_info} if request_info else {}
    audit_logger.info(message, extra=extra)