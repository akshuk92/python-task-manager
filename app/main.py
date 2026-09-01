# app/main.py
#
# WHY THIS FILE EXISTS:
# This uses the "Application Factory" pattern (create_app function)
# instead of a single global `app = Flask(__name__)`.
# WHY? Because it allows:
#   1. Creating multiple app instances for testing (each with a fresh DB)
#   2. Loading different configs for dev/test/production
# This is the pattern used by real production Flask codebases.
#
# WHERE THIS IS USED IN COMPANIES:
# This exact file is what Gunicorn (a production WSGI server) will
# import and run in our Docker container — NOT `python app.py`.
# Flask's built-in server (used in Step 1) is only for local development;
# it is single-threaded and NOT safe for production traffic.

from flask import Flask
from app.config import Config
from app.routes import bp
from app.models import init_db
from app.logger import setup_logger

logger = setup_logger(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database (creates the table if missing)
    init_db()
    logger.info(f"Database initialized at {Config.DB_PATH}")

    # Register all routes defined in routes.py
    app.register_blueprint(bp)

    logger.info(f"App starting in '{Config.APP_ENV}' mode")
    return app


# This creates the app object that Gunicorn will look for
# when we run: gunicorn "app.main:app"
app = create_app()

if __name__ == "__main__":
    # Only used for local development (python -m app.main)
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
