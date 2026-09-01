# Task Manager API — End-to-End DevOps Project

A real-world Python Flask REST API, built to practice the **full DevOps
lifecycle**: coding, version control, containerization, CI/CD, security
scanning, orchestration, and monitoring.

---

## 1. What This App Does

A simple task-tracking REST API backed by SQLite.

| Method | Endpoint          | Description          |
|--------|-------------------|-----------------------|
| GET    | `/health`         | Health check          |
| GET    | `/tasks`          | List all tasks        |
| GET    | `/tasks/<id>`     | Get one task          |
| POST   | `/tasks`          | Create a task         |
| PUT    | `/tasks/<id>`     | Mark task done/undone |
| DELETE | `/tasks/<id>`     | Delete a task         |

---

## 2. Folder Structure

```
task-manager/
├── app/                      # Application source code
│   ├── __init__.py
│   ├── main.py                # App factory / entry point (Gunicorn target)
│   ├── routes.py               # API endpoints
│   ├── models.py               # SQLite database layer
│   ├── config.py               # Environment-based configuration
│   └── logger.py               # Structured logging setup
├── tests/
│   └── test_app.py             # Pytest automated tests
├── k8s/                        # Raw Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── helm/task-manager/          # Helm chart (templated K8s manifests)
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── nginx/
│   └── nginx.conf              # Reverse proxy config
├── monitoring/
│   └── prometheus.yml          # Metrics scrape config
├── scripts/
│   ├── deploy_ec2.sh           # Manual AWS EC2 deployment script
│   └── trivy_scan.sh           # Local security scan helper
├── .github/workflows/ci-cd.yml # GitHub Actions pipeline
├── Jenkinsfile                 # Jenkins pipeline (Sonar/Trivy/Nexus/K8s)
├── sonar-project.properties    # SonarQube code-quality config
├── Dockerfile                  # Production container image
├── docker-compose.yml          # Local multi-container stack
├── requirements.txt            # Production Python dependencies
├── requirements-dev.txt        # + testing/linting dependencies
└── .gitignore / .dockerignore
```

---

## 3. Running Locally (No Docker)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

# Run the app
python -m app.main

# In another terminal, run tests
pytest -v tests/
```

Test it:
```bash
curl http://localhost:5000/health
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"title":"Learn Kubernetes"}'
curl http://localhost:5000/tasks
```

---

## 4. Running With Docker

```bash
docker build -t task-manager:local .
docker run -p 5000:5000 -e APP_ENV=production task-manager:local
```

## 5. Running the Full Stack (App + Nginx + Prometheus + Grafana)

```bash
docker compose up -d --build
```
- App (via Nginx):  http://localhost:8080
- Prometheus:        http://localhost:9090
- Grafana:           http://localhost:3000 (login: admin/admin)

---

## 6. CI/CD Pipeline Flow

```
Push code to GitHub
      │
      ▼
Checkout ─▶ Install deps ─▶ Lint ─▶ Unit tests ─▶ SonarQube scan
      │                                                 │
      ▼                                          Quality Gate (pass/fail)
Build Docker image
      │
      ▼
Trivy security scan (blocks on HIGH/CRITICAL CVEs)
      │
      ▼
Push image to Nexus (private Docker registry)
      │
      ▼
kubectl apply → Kubernetes Deployment / Service / Ingress
```

Both `Jenkinsfile` and `.github/workflows/ci-cd.yml` implement this —
Jenkins is common in large/legacy enterprises, GitHub Actions in modern
cloud-native teams. Knowing both matters for interviews.

---

## 7. Kubernetes / Helm

```bash
# Raw manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/

# OR using Helm (recommended — parameterized per environment)
helm install task-manager ./helm/task-manager \
  --set image.tag=1.0.0 \
  --set replicaCount=5
```

---

## 8. AWS EC2 Manual Deployment

```bash
scp -i key.pem -r task-manager ubuntu@<EC2_PUBLIC_IP>:~/
ssh -i key.pem ubuntu@<EC2_PUBLIC_IP>
bash ~/task-manager/scripts/deploy_ec2.sh
```

---

## 9. Full DevOps Toolchain Covered

| Tool | Purpose in this project |
|---|---|
| Git/GitHub | Version control, collaboration, triggers CI |
| Docker | Packages app into a portable container |
| Docker Compose | Runs app + Nginx + Prometheus + Grafana locally |
| Jenkins | Enterprise CI/CD orchestration |
| GitHub Actions | Cloud-native CI/CD alternative |
| SonarQube | Static code quality & security analysis |
| Trivy | Container image vulnerability scanning |
| Nexus | Private Docker image / artifact registry |
| Kubernetes | Container orchestration, self-healing, scaling |
| Helm | Templated, environment-aware K8s deployments |
| AWS EC2 | Cloud virtual machine hosting |
| Nginx | Reverse proxy / load balancer |
| Prometheus + Grafana | Monitoring and dashboards |
| Python logging | Centralized, structured application logs |

---

## 10. Next Steps (Learning Path)

1. Push this to a real GitHub repo, connect a Jenkins job to it.
2. Spin up a real SonarQube + Nexus server (Docker Compose is fine for practice).
3. Get a free-tier AWS EC2 instance and run `scripts/deploy_ec2.sh`.
4. Install `minikube` or `kind` locally and `kubectl apply -f k8s/`.
5. Install Helm and deploy via the chart instead.
6. Add Prometheus + Grafana dashboards for real request metrics.
