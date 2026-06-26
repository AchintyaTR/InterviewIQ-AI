# Deployment Guide

This document describes the instructions to deploy **InterviewIQ AI** using Docker containerization.

## Deployment Architecture

In a production environment, components are distributed as follows:

1. **Frontend:** Deployed to a CDN or server container (e.g., Vercel, AWS ECS, or Docker container behind Nginx).
2. **Backend:** Deployed as a scalable FastAPI task container inside a cluster (e.g., AWS ECS Fargate, Kubernetes, or DigitalOcean App Platform).
3. **Database:** Deployed as a managed cloud PostgreSQL instance (e.g., AWS RDS or Supabase).
4. **Vector Database:** Deployed as a containerized ChromaDB service or hosted Qdrant/Pinecone instance.

---

## Deploying with Docker Compose

For staging, demonstration, or single-instance local deployments, a standard Docker Compose stack maps the services.

### Prerequisite Setup
1. Clone the repository on the target server.
2. Initialize production settings in `.env`:
   ```bash
   cp .env.example .env
   nano .env # Set secure, high-entropy secrets and production API keys
   ```

### Command to Start Stack
Run the stack detached in background:
```bash
docker-compose -f docker-compose.yml up -d --build
```

### Verification and Health Checks
Check logs to verify startup:
```bash
docker-compose logs -f
```
Run ping requests to check API availability:
```bash
curl -f http://localhost:8000/api/v1/health
```

---

## GitHub Actions CI/CD Pipeline

The `.github/workflows/ci.yml` pipeline automates unit testing and builds checking on every pull request to `main`.

### Production Build Steps
1. **Lint Checks:** Checks backend code style with `flake8` and frontend layout with `npm run lint`.
2. **Unit Tests:** Executes test cases using `pytest`.
3. **Docker Multi-stage Builds:** Builds lightweight production Docker images for both backend and frontend layers.
4. **Container Registry Push:** Pushes built target containers to Docker Hub, GitHub Container Registry (GHCR), or AWS ECR.
5. **Auto-deploy (optional):** Triggers webhook updates or ECS task updates to roll out the new release.
