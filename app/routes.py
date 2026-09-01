# app/routes.py
#
# WHY THIS FILE EXISTS:
# Separating routes (URL endpoints) from app setup (main.py) and
# database logic (models.py) is called "separation of concerns."
# It makes the codebase easier to test, read, and maintain — exactly
# what a real engineering team expects in a code review.
#
# WHERE THIS IS USED IN COMPANIES:
# This is a standard Flask "Blueprint" pattern used in real production
# microservices to keep route definitions organized as the app grows.

from flask import Blueprint, jsonify, request
from app import models
from app.logger import setup_logger

logger = setup_logger(__name__)

# A Blueprint lets us group related routes together and register
# them on the main app later (see main.py)
bp = Blueprint("routes", __name__)


@bp.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.
    Kubernetes 'liveness' and 'readiness' probes call this constantly
    (e.g., every 10 seconds) to decide whether to keep sending traffic
    to this pod, or restart it if it's unhealthy.
    """
    return jsonify({"status": "ok"}), 200


@bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = models.get_all_tasks()
    return jsonify({"tasks": tasks}), 200


@bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = models.get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "task not found"}), 404
    return jsonify(task), 200


@bp.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True)

    if not data or "title" not in data or not str(data["title"]).strip():
        logger.warning("Rejected task creation: missing/invalid title")
        return jsonify({"error": "title is required"}), 400

    task = models.create_task(data["title"].strip())
    logger.info(f"Task created: {task}")
    return jsonify(task), 201


@bp.route("/tasks/<int:task_id>", methods=["PUT"])
def mark_task_done(task_id):
    existing = models.get_task_by_id(task_id)
    if not existing:
        return jsonify({"error": "task not found"}), 404

    data = request.get_json(silent=True) or {}
    done = bool(data.get("done", True))
    task = models.update_task(task_id, done)
    logger.info(f"Task updated: {task}")
    return jsonify(task), 200


@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    existing = models.get_task_by_id(task_id)
    if not existing:
        return jsonify({"error": "task not found"}), 404

    models.delete_task(task_id)
    logger.info(f"Task deleted: id={task_id}")
    return jsonify({"message": "task deleted"}), 200
