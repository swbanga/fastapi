# Enterprise FastAPI DevSecOps Architecture

[![CI/CD Pipeline](https://github.com/swbanga1/fastapi/actions/workflows/deploy.yml/badge.svg)](https://github.com/swbanga1/fastapi/actions/workflows/deploy.yml)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg?logo=docker)](https://www.docker.com/)

## 🏗️ Architectural Overview

This repository houses a high-performance RESTful API engineered with Python and FastAPI, wrapped in a strict DevSecOps deployment architecture. 

The primary objective of this project is not just application logic, but **infrastructure as code (IaC) and deployment immutability**. It demonstrates a transition from legacy host-based deployments to a fully containerized, automated, and secure cloud environment targeting bare-metal execution.

### The Engineering Stack

| Layer | Technology | Execution Reality |
| :--- | :--- | :--- |
| **Application Kernel** | Python 3.12 / FastAPI | Asynchronous, high-throughput routing with Pydantic schema validation. |
| **Data Persistence** | PostgreSQL 16 / SQLAlchemy | Relational data mapping executed strictly within an isolated Docker bridge network. |
| **Orchestration** | Docker & Docker Compose | Sterile execution environment. Zero dependencies installed on the host OS. |
| **Security & Routing** | Nginx Reverse Proxy | Handles SSL termination and securely filters traffic into the container perimeter. |
| **Continuous Integration** | GitHub Actions | Automated `pytest` matrix executed against an isolated PostgreSQL service container. |
| **Continuous Deployment** | GitHub Actions | Automated Docker Hub registry push and SSH-driven bare-metal Azure container rotation. |

---

## 🔒 Security & Deployment Protocol

This architecture employs strict DevSecOps methodologies to mathematically eliminate configuration drift and credential exposure:

1. **The Immutable Hard Reset:** The CI/CD pipeline does not perform standard Git merges on the production server. It executes `git fetch --all` followed by `git reset --hard origin/main`. The Azure VM's file system is forced to perfectly mirror the repository, destroying any unauthorized manual tampering.
2. **Cryptographic Vault Injection:** No database passwords or JWT secrets exist in version control. All credentials are dynamically injected into the production `.env` perimeter via GitHub Actions Secrets during the deployment sequence.
3. **Network Sterilization:** The PostgreSQL database does not expose port `5432` to the host machine in production. It is completely isolated from the public internet, accessible only by the API container via internal Docker DNS.

---

## 🚀 Local Development Environment

To replicate this environment locally for development or security auditing, execute the following protocol.

### 1. Clone the Blueprint
```bash
git clone [https://github.com/swbanga/fastapi.git](https://github.com/swbanga/fastapi.git)
cd fastapi
