# Smart Campus – DevOps Automation & Cloud Deployment

A demo campus student-registration service built with Flask and SQLite and packaged using Docker. The repository demonstrates CI checks, automated testing, static security scanning, Docker Compose, Jenkins, GitHub Actions, Terraform, Ansible, basic monitoring endpoints, logging, and example Kubernetes manifests.

## Architecture

GitHub → Jenkins pipeline / GitHub Actions → Pytest → Bandit → Docker image → Docker Compose deployment → AWS EC2 (manual deployment guide below).

## Features

- Responsive student registration UI
- REST API: `GET/POST /api/students`
- Health endpoint: `/health`
- Prometheus-style metrics: `/metrics`
- SQLite persistence via Docker volume
- Duplicate email validation and input validation

## Run locally

Prerequisites: Docker Desktop with Docker Compose.

```bash
docker compose up --build -d
```

Open http://localhost:5000 . Health check: http://localhost:5000/health . Metrics: http://localhost:5000/metrics .

Stop:

```bash
docker compose down
```

Persisted data is in the `campus_data` volume. To remove data too: `docker compose down -v`.

## Tests and security scan

With Python 3.11+:

```bash
python -m pip install -r backend/requirements.txt
python -m pytest backend/tests -v
python -m bandit -r backend -ll
```

## GitHub

Create a repository, then from this directory:

```bash
git init
git add .
git commit -m "Initial Smart Campus DevOps project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/smart-campus-devops.git
git push -u origin main
```

GitHub Actions is defined in `.github/workflows/ci.yml`. It runs tests, Bandit and Docker build on push/PR to `main`.

## Jenkins pipeline

The `Jenkinsfile` assumes a Linux Jenkins agent with Python 3, Docker, Docker Compose plugin, and permission to run Docker commands. Configure a Jenkins Pipeline job using **Pipeline script from SCM**, point it to this repository, branch `main`, script path `Jenkinsfile`. The pipeline tests, scans, builds, deploys using Compose, and checks the health endpoint. If Jenkins is installed on Windows, use a Linux agent or adapt shell (`sh`) steps to PowerShell; this included Jenkinsfile is Linux-oriented.

## AWS EC2 demo deployment (manual)

1. Launch Ubuntu EC2 in your account. For a short demo, use an eligible small instance. Restrict SSH (22) to your IP. For the demo, allow TCP 5000 to your IP or intended audience only.
2. Connect to the instance and install Docker:

```bash
sudo apt update
sudo apt install -y docker.io git
sudo systemctl enable --now docker
```

3. Clone your GitHub repo, enter the directory and build/run:

```bash
git clone https://github.com/YOUR_USERNAME/smart-campus-devops.git
cd smart-campus-devops
sudo docker build -t smart-campus .
sudo docker run -d --name smart-campus -p 5000:5000 -v campus_data:/data smart-campus
```

4. Open `http://EC2_PUBLIC_IP:5000`. Check `http://EC2_PUBLIC_IP:5000/health`.
5. Clean up the instance and security group when done to avoid ongoing charges.

This manual deployment is a demonstration, not an automated Jenkins-to-EC2 deployment. The included Jenkins pipeline deploys on its own Docker host. Remote deployment can be added using protected Jenkins credentials and a restricted SSH deployment workflow.

## Terraform (example)

`terraform/main.tf` creates a demo EC2 instance and security group. Review the security rules, provide a region-valid Ubuntu AMI ID, an existing key-pair name, and your IP CIDR in `terraform.tfvars` before use. Do not commit credentials or state files. Run:

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# edit values
terraform init
terraform plan
terraform apply
```

Destroy demo resources after use: `terraform destroy`. Terraform may incur AWS costs.

## Ansible

`ansible/deploy.yml` is a starter playbook. It expects a configured inventory and the project files to be staged on the target; review/edit paths before executing.

## Monitoring and logging

- `/health` provides a simple health status.
- `/metrics` exposes registered-student count in Prometheus text format.
- `monitoring/prometheus.yml` is a starter scrape configuration; adapt target address to your network.
- Application logs are emitted to stdout, suitable for Docker log collection.

## Kubernetes (starter manifests)

`kubernetes/deployment.yaml` and `service.yaml` are illustrative starter manifests. Build/load or push an image accessible to your Kubernetes cluster before applying them. They are not part of the tested Docker Compose workflow.

## Project limitations

This is a learning/demo application: no authentication, authorization, email verification, production database, TLS configuration, rate limiting, or hardened production deployment is included. Do not use it to collect real personal information. Review the infrastructure files and replace demo settings before deploying publicly.
