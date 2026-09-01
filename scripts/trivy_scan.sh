#!/bin/bash
# scripts/trivy_scan.sh
#
# WHY: Lets you run the exact same security scan locally that Jenkins/
# GitHub Actions run in CI — so you catch vulnerabilities BEFORE pushing.

set -e

IMAGE_NAME="task-manager:local"

echo ">>> Building image for scanning..."
docker build -t $IMAGE_NAME .

echo ">>> Running Trivy scan (HIGH and CRITICAL only)..."
trivy image --severity HIGH,CRITICAL $IMAGE_NAME

echo ">>> Scan complete."
