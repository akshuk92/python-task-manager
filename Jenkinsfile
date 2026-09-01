// Jenkinsfile
//
// WHY: This is the heart of DevOps automation. Every code push should
// automatically flow through: build -> test -> code quality scan ->
// security scan -> package -> publish -> deploy — with ZERO manual steps.
//
// WHERE USED: Jenkins is one of the most widely used CI/CD tools in
// enterprises (banks, telecoms, large legacy companies). Understanding
// a Jenkinsfile is a core Junior DevOps Engineer interview expectation.

pipeline {
    agent any

    environment {
        IMAGE_NAME   = "task-manager"
        IMAGE_TAG    = "${env.BUILD_NUMBER}"
        DOCKER_REGISTRY = "your-nexus-registry.company.com:5000"
        SONAR_PROJECT_KEY = "task-manager"
    }

    stages {

        stage('Checkout') {
            steps {
                // Pulls the latest code from GitHub
                git branch: 'main', url: 'https://github.com/your-org/task-manager.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 app/ --max-line-length=100 || true
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --cov=app --cov-report=xml tests/
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                // Requires the SonarQube Jenkins plugin + a configured
                // SonarQube server named 'MySonarServer' in Jenkins config
                withSonarQubeEnv('MySonarServer') {
                    sh 'sonar-scanner -Dproject.settings=sonar-project.properties'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                // Pauses the pipeline and waits for SonarQube to report
                // pass/fail. If code quality fails, the pipeline STOPS here
                // — a bad-quality build never reaches Docker/production.
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Trivy Security Scan') {
            steps {
                // Scans the built image for known CVEs (vulnerabilities)
                // in OS packages and Python libraries. Fails the build
                // if HIGH/CRITICAL vulnerabilities are found.
                sh "trivy image --severity HIGH,CRITICAL --exit-code 1 ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Push to Nexus') {
            steps {
                sh '''
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                    docker login ${DOCKER_REGISTRY} -u $NEXUS_USER -p $NEXUS_PASS
                    docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    sed -i "s|IMAGE_PLACEHOLDER|${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}|g" k8s/deployment.yaml
                    kubectl apply -f k8s/namespace.yaml
                    kubectl apply -f k8s/configmap.yaml
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl apply -f k8s/ingress.yaml
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline succeeded — build ${IMAGE_TAG} deployed."
        }
        failure {
            echo "❌ Pipeline failed — check logs above for the failing stage."
        }
        always {
            cleanWs()
        }
    }
}
