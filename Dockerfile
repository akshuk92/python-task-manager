# Dockerfile
#
# Packages the Python Flask application and its dependencies
# into a portable Docker image.

FROM python:3.12-slim

# Prevent Python from creating .pyc files
# and make Python logs appear immediately.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non-root user for security.
RUN addgroup --system app && \
    adduser --system --ingroup app app

# Application working directory.
WORKDIR /app

# Copy requirements first.
# Docker can cache this layer if requirements.txt doesn't change.
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code.
COPY app/ ./app/

# Give the app user ownership of the application files.
# This fixes the PermissionError when Gunicorn imports the Flask app.
RUN chown -R app:app /app

# Run the application as the non-root user.
USER app

# Flask/Gunicorn listens on port 5000.
EXPOSE 5000

# Docker health check.
# Checks whether the Flask application's /health endpoint is responding.
HEALTHCHECK --interval=30s --timeout=3s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Start the Flask application using Gunicorn.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app.main:app"]
