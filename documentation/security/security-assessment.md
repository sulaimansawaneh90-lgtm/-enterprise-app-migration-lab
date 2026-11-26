# Enterprise Application Migration Lab — Security Assessment

## 1. Overview

Security scanning was incorporated into the Enterprise Application Migration Lab
to identify exposed secrets, insecure Python code patterns, vulnerable
dependencies, container image vulnerabilities, and Dockerfile configuration
issues.

The objective is to integrate security checks into the application development
and containerization workflow.

## 2. Security Tools

| Tool | Purpose | Result |
|------|---------|--------|
| Gitleaks | Detect secrets and credentials | Passed |
| Bandit | Analyze Python code for security issues | Passed |
| pip-audit | Identify vulnerable Python dependencies | Passed |
| Trivy | Scan container images for vulnerabilities | Findings identified |
| Hadolint | Lint Dockerfiles for best practices | Passed |

## 3. Application Security Scanning

### Gitleaks

Scanned application source code and Docker Compose configuration for
potentially exposed secrets.

**Result:** No leaks found.

### Bandit

Analyzed Python application code for common security issues.

An initial finding related to binding the development Flask server to
all network interfaces was addressed.

**Result:** No issues identified in the subsequent scan.

### pip-audit

Audited Python dependencies for known vulnerabilities.

**Result:** No known vulnerabilities found in the audited Python dependencies.

### Hadolint

Analyzed Dockerfiles for Docker best practices and potential configuration
issues.

An initial warning regarding the container user configuration was addressed
by using a numeric non-root UID/GID.

**Result:** No warnings or errors.

## 4. Container Image Vulnerability Assessment

Trivy was used to scan the Authentication Service and Backend API Docker images.

### Images Scanned

- Authentication Service
- Backend API

Both images use Debian 13.8 as their base operating system.

### Scan Results

| Severity | Findings |
|----------|----------|
| Critical | 0 |
| High | 53 |
| Medium | 81 |
| Low | 78 |
| Total vulnerability records per image | 229 |

The scan identified vulnerabilities primarily within the operating system
packages included in the container images.

At the time of the assessment, the identified unique High-severity
vulnerabilities did not have fixes listed in the Trivy reports.

## 5. Docker Security Improvements

The following security improvements were implemented:

- Applications run as a non-root user.
- Container images use Python slim base images.
- Dependencies are explicitly version-pinned.
- Docker build contexts are restricted using `.dockerignore`.
- Sensitive environment files are excluded from Git.
- Private keys and certificate files are excluded from Git.
- Application containers are bound to localhost on the host.
- JWT authentication protects backend API access.
- Passwords are stored using password hashing.
- Database access is restricted to the Docker network for application services.
- PostgreSQL data is persisted using a named Docker volume.

## 6. Docker Image Optimization Experiment

A multi-stage Docker build was implemented and evaluated.

The experiment separated dependency installation from the runtime image.

The resulting image was approximately 212 MB, compared with the
approximately 209 MB baseline.

Although the experiment did not reduce image size, it demonstrated:

- Multi-stage Docker build implementation.
- Separation of build and runtime stages.
- Dependency transfer between stages.
- Removal of pip from the application virtual environment.
- Runtime dependency validation.
- Image size measurement and comparison.

The experiment was documented separately.

## 7. Findings and Remediation Strategy

The container scans identified High, Medium, and Low severity vulnerabilities
in the operating system packages.

The remediation strategy includes:

1. Monitor upstream Debian security updates.
2. Rebuild images regularly to incorporate updated base images.
3. Re-run Trivy scans after image rebuilds.
4. Evaluate vulnerability severity and exploitability.
5. Prioritize Critical and High vulnerabilities when fixes become available.
6. Avoid introducing unnecessary packages into container images.
7. Maintain dependency version control.
8. Integrate security scanning into CI/CD pipelines.

## 8. Security Scanning Limitations

Security scan results represent a point-in-time assessment.

Vulnerability databases are continuously updated, and new vulnerabilities
may be identified after the scans.

The scan results should therefore be revalidated before production deployment.

## 9. Conclusion

Security testing was incorporated throughout the development of the lab.

The project demonstrates secret scanning, static application security
analysis, dependency auditing, container vulnerability scanning,
Dockerfile linting, secure container configuration, and vulnerability
assessment documentation.

The identified container vulnerabilities provide opportunities for
continued remediation and integration of security gates into the CI/CD pipeline.
