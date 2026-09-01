#!/bin/bash
# scripts/deploy_ec2.sh
#
# WHY: Documents/automates exactly what a Junior DevOps Engineer does
# to manually deploy this app onto a fresh AWS EC2 Linux instance.
# In real companies, this logic eventually gets absorbed into
# Jenkins/Terraform/Ansible — but you MUST understand the manual
# steps first.
#
# USAGE: Run this ON the EC2 instance after SSH-ing in.
#   scp -i key.pem -r task-manager ubuntu@<EC2_IP>:~/
#   ssh -i key.pem ubuntu@<EC2_IP>
#   bash deploy_ec2.sh

set -e  # Exit immediately if any command fails

echo ">>> Updating system packages..."
sudo apt-get update -y

echo ">>> Installing Docker..."
sudo apt-get install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

echo ">>> Installing Docker Compose plugin..."
sudo apt-get install -y docker-compose-plugin

echo ">>> Building and starting containers..."
cd ~/task-manager
sudo docker compose up -d --build

echo ">>> Verifying app health..."
sleep 5
curl -f http://localhost:8080/health || (echo "Health check failed!" && exit 1)

echo ">>> Deployment complete. App is running behind Nginx on port 8080."
