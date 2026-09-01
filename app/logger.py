# app/logger.py
#
# WHY THIS FILE EXISTS:
# In production, you cannot "print()" debug statements and hope to find
# them later. Companies use structured logging so that tools like the
# ELK Stack (Elasticsearch, Logstash, Kibana), Loki, or CloudWatch can
# collect, search, and alert on logs automatically.
#
# WHERE THIS IS USED IN COMPANIES:
# Every production service logs: startup events, errors, and request info.
# When something breaks in production at 2 AM, logs are the FIRST place
# a DevOps/SRE engineer looks.

import logging
import sys
from app.config import Config


def setup_logger(name: str) -> logging.Logger:
    """
    Creates and configures a logger instance.
    Logs are written to stdout (standard output) — NOT to a file.
    WHY stdout? Because in Docker/Kubernetes, anything printed to
    stdout is automatically captured by the container runtime and
    can be shipped to a centralized logging system. Writing to a
    local file inside a container is an anti-pattern.
    """
    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL)

    # Avoid adding duplicate handlers if this function is called twice
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
