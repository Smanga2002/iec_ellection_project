# IEC Election Project

A containerised environment and Python-based toolkit for connecting to and working with a PostgreSQL database used for the IEC election project. This README documents how to set up the local and containerised environment, verify connectivity, and manage the repository.

> Note: Sensitive credentials must never be committed — use a `.env` file (added to `.gitignore`) for secrets.

## Table of contents
- Overview
- Prerequisites
- Local installation (Windows)
- Containerised setup (Docker + docker-compose)
- Environment variables (`.env`)
- Running and verifying the system
- Testing database connectivity from Python
- Git and repository instructions
- Project structure (example)
- Troubleshooting
- Contact / Next steps

## Overview
This repository contains the environment scaffolding (Dockerfile, docker-compose.yml, notebooks, and scripts) used to run Python notebooks and scripts that connect to a PostgreSQL instance. The intention is to be able to run everything locally (Windows + WSL) or fully containerised with Docker.

## Prerequisites
- Git (install for Windows)
- VS Code (recommended editor; set as default terminal if preferred)
- Docker Desktop for Windows (enable WSL 2 backend)
- WSL2 (Windows Subsystem for Linux) — run `wsl --install` or `wsl --update` as needed
- PostgreSQL (optional locally; for containerised runs we use the official Postgres image)
- Python 3.14.x (3.14.2 recommended per notes)
- pip (comes with Python)

## Local installation (Windows)
1. Install Git and set up your GitHub profile.
2. Install VS Code and configure it as your terminal/editor.
3. Install WSL2 if you plan to use Linux tooling with Docker:
   - From an elevated PowerShell: `wsl --install` or `wsl --update`
4. Install Docker Desktop for Windows and sign in with your work email if required. Restart the machine if Docker requests it.
5. (Optional) Install PostgreSQL locally:
   - Download the Windows installer from PostgreSQL site and follow the installer steps.
   - During install set your PostgreSQL password and note port (default 5432).

Verify:
- Git: `git --version`
- Docker: `docker run hello-world`
- Python: `python --version` (or `python3 --version`)

## Containerised setup (recommended)
This project is designed to run with Docker and docker-compose.

1. Pull the required Postgres image (use same major version you want to test with, e.g., 18):
   - `docker pull postgres:18`
2. Ensure your repo contains:
   - `docker-compose.yml`
   - `Dockerfile` (for the Python/notebook container)
   - `requirements.txt`
   - `scripts/connection_test.py` (or equivalent) for verifying DB connectivity
3. Build and start containers:
   - `docker-compose build`
   - `docker-compose up -d` (or `docker-compose up` to see logs)
4. List running containers:
   - `docker ps`

Example minimal docker run for quick check:
- `docker run -d ubuntu sleep 5`
- `docker ps` to confirm it ran

## Environment variables (`.env`)
Create a `.env` file in the project root (do not commit). Example:

DB_HOST=iec_postgres
DB_PORT=5432
DB_NAME=iec_db
DB_USER=postgres
DB_PASSWORD=your_password
POSTGRES_IMAGE=postgres:18

Ensure `.env` is listed in `.gitignore`.

## requirements.txt (core packages)
Ensure your `requirements.txt` contains at least:
- pandas
- SQLAlchemy
- psycopg2-binary
- jupyter

These packages enable DataFrame handling, ORM/connection engine, Postgres driver, and notebooks respectively.

## Dockerfile
Your Dockerfile for the Python/notebook container should:
- Use a Python base image (matching your Python version)
- Copy `requirements.txt` and run `pip install -r requirements.txt`
- Copy project files
- Expose ports for Jupyter (if you run it)
- Provide an entrypoint or CMD that starts a notebook or keeps the container up for debugging

## Running and verifying connectivity
After `docker-compose up`:
- Verify PostgreSQL container is ready by connecting with psql or a client (pgAdmin).
- Example: `docker exec -it <postgres-container-name> psql -U postgres` and enter your password.
- Verify Python container can reach Postgres:
  - Example test command (from notes):  
    `docker exec iec_test_notebook python ~/scripts/connection_test.py`
  - Or open a Jupyter notebook and run a small SQLAlchemy/psycopg2 script to connect and run `SELECT 1;`.

Typical commands:
- Build: `docker-compose build`
- Start (foreground): `docker-compose up`
- Start (detached): `docker-compose up -d`
- Stop: `docker-compose down`

## Testing DB connection from Python (example)
A small Python snippet (connection_test.py) should:
- Read DB params from environment variables
- Create an SQLAlchemy engine:
  - `engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")`
- Try a basic query:
  - `with engine.connect() as conn: result = conn.execute(text("SELECT 1")); print(result.scalar())`

Run inside notebook container:
`docker exec iec_test_notebook python ~/scripts/connection_test.py`

## Git & repository management
Initialize repo and push:
```bash
git init
git remote add origin <Your_GitHub_URL>
git add .
git commit -m "Initial environment structure and Docker setup for Sprint 3"
git push -u origin main
```

Branch workflow (example):
```bash
git checkout -b sprint3-setup
git add .
git commit -m "Descriptive message about changes"
git push origin sprint3-setup
```

Add collaborators in the GitHub repository settings to allow team members to pull and push.

## Recommended .gitignore entries
Add (at minimum):
```
.env
__pycache__/
*.pyc
.ipynb_checkpoints/
data/
*.sqlite
```

## Example project structure
(Adapt to your project; this is a suggested layout)
```
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env           # NOT checked into git
├── .gitignore
├── README.md
├── notebooks/
│   └── analysis.ipynb
├── scripts/
│   └── connection_test.py
└── src/
    └── app_code.py
```

## Troubleshooting tips
- Docker Desktop errors on Windows:
  - Ensure WSL2 is installed and set as backend.
  - Restart Docker and reboot the machine if prompted.
- Postgres connection refused:
  - Confirm container is running: `docker ps`
  - Check `DB_HOST` (in docker-compose networks the service name is typically the host)
  - Check ports mapping and `.env` variables
- Python packages missing:
  - Rebuild container: `docker-compose build --no-cache`
  - Check `requirements.txt` for correct package names
