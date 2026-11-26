# Docker Multi-Stage Build Experiment

## 1. Objective

Evaluate whether a multi-stage Docker build can improve the security,
maintainability, and image size of the Backend API container.

The experiment focuses on separating dependency installation from
the runtime environment and removing unnecessary package-management
tools from the application environment.

---

## 2. Hypothesis

A multi-stage Docker build will:

- Separate dependency installation from the runtime stage.
- Reduce unnecessary tooling in the application environment.
- Improve build isolation and Dockerfile organization.
- Potentially reduce the final container image size.

---

## 3. Baseline

The original Backend API Docker image used a single-stage build.

| Metric | Baseline |
|---|---|
| Build strategy | Single-stage |
| Base image | python:3.12-slim |
| Image disk usage | 209 MB |
| Content size | 51.1 MB |
| Application port | 5002 |
| Runtime user | Non-root |
| Python dependencies | Flask, PyJWT, Psycopg, Gunicorn |

---

## 4. Implementation

The Dockerfile was redesigned using a multi-stage build.

### Builder stage

Responsibilities:

- Use Python 3.12 slim.
- Create a Python virtual environment.
- Install application dependencies.
- Remove pip from the virtual environment.

### Runtime stage

Responsibilities:

- Use Python 3.12 slim.
- Apply operating-system package updates.
- Copy the virtual environment from the builder stage.
- Copy application code.
- Create a dedicated non-root user.
- Run the application using Gunicorn.

### Security controls

- Application runs as UID 10001.
- Application runs as GID 10001.
- Pip is removed from the application's virtual environment.
- Dependencies are installed in an isolated virtual environment.
- Application runs through Gunicorn.
- Docker build context is minimized using `.dockerignore`.

---

## 5. Build Architecture

### Stage 1: Builder

The builder stage creates the virtual environment and installs
the Python application dependencies.

### Stage 2: Runtime

The runtime stage receives the virtual environment and application
code without needing to perform dependency installation.

This separates dependency installation from application execution.

---

## 6. Image Size Comparison

| Build | Disk Usage | Content Size |
|---|---:|---:|
| Original single-stage build | 209 MB | 51.1 MB |
| Pip-removal experiment | 209 MB | 51.1 MB |
| Multi-stage build | 212 MB | 51.9 MB |

### Result

The multi-stage build increased the measured image size slightly.

- Disk usage increased from 209 MB to 212 MB.
- Content size increased from 51.1 MB to 51.9 MB.

Therefore, the experiment did not achieve image-size reduction.

---

## 7. Functional Validation

The resulting image was tested before deployment to the Docker Compose
environment.

### Python runtime

```text
Python 3.12.16
