# Multi-Service Application – Dockerized

## Overview
This project demonstrates containerization of a multi-service application
consisting of a frontend, backend, and database, following Docker best practices.

The goal of this assignment was to design a production-ready containerized
setup with optimized images, service isolation, and clear validation steps.

---

## Architecture
- Frontend: React (served via Nginx)
- Backend: FastAPI (Python)
- Database: PostgreSQL

Communication flow:
Browser → Frontend → Backend → Database

---

## Docker Best Practices Applied
- Separate Dockerfile per service
- Multi-stage builds for frontend
- Slim / Alpine base images
- No secrets baked into images
- `.dockerignore` for reduced build context
- Environment-based configuration

---

## Running the Project (Docker Compose)

```bash
docker compose up --build
