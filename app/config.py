# app/config.py
#
# WHY THIS FILE EXISTS:
# Real applications should NEVER hardcode values like database paths,
# debug flags, or ports directly in the code. Instead, they read them
# from environment variables. This is called "The Twelve-Factor App"
# methodology (a famous set of best practices for cloud-native apps).
#
# WHERE THIS IS USED IN COMPANIES:
# When Docker, Kubernetes, or Jenkins deploy this app, they inject
# environment variables like APP_ENV=production, DB_PATH=/data/tasks.db
# WITHOUT touching a single line of code. That's the whole point of
# separating config from code.

import os


class Config:
    # os.environ.get(key, default) reads an environment variable.
    # If it doesn't exist, it falls back to the default value.
    APP_ENV = os.environ.get("APP_ENV", "development")
    DEBUG = APP_ENV == "development"
    DB_PATH = os.environ.get("DB_PATH", "tasks.db")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    PORT = int(os.environ.get("PORT", 5000))
