pipeline {
    agent any
    options { timestamps() }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Python Tests') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/pip install -r backend/requirements.txt'
                sh '.venv/bin/python -m pytest backend/tests -v'
            }
        }
        stage('Security Scan') { steps { sh '.venv/bin/bandit -r backend -ll' } }
        stage('Docker Build') { steps { sh 'docker build -t smart-campus:${BUILD_NUMBER} .' } }
        stage('Deploy on Jenkins host') {
            steps {
                sh 'docker compose up -d --build'
                sh 'sleep 5'
                sh 'curl --fail http://localhost:5000/health'
            }
        }
    }
    post {
        success { echo 'Pipeline completed: image built and application deployed via Docker Compose.' }
        failure { echo 'Pipeline failed. Review stage logs to identify the issue.' }
    }
}
