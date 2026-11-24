# Enterprise Application Migration Lab

## Project Overview

This project simulates the migration of a traditional enterprise application environment from an on-premises infrastructure to AWS.

The objective is to demonstrate enterprise cloud migration, infrastructure automation, containerization, application modernization, security, monitoring, and deployment practices.

## Source Environment

The initial environment will run locally using Docker Compose.

### Application Components

1. Customer Portal - Python Flask
2. Authentication Service - Python Flask
3. Backend API - Python Flask
4. Database - PostgreSQL
5. Document Storage - Python Flask

## Application Architecture

Customer Portal
    |
    +---- Authentication Service
    |
    +---- Backend API
              |
              +---- PostgreSQL
              |
              +---- Document Storage

## Target AWS Architecture

| Source Component | AWS Target |
|---|---|
| Flask applications | Amazon ECS Fargate |
| PostgreSQL | Amazon RDS |
| Document Storage | Amazon S3 |
| Container Images | Amazon ECR |
| Load Balancing | Application Load Balancer |
| Networking | Amazon VPC |
| Secrets | AWS Secrets Manager |
| Encryption | AWS KMS |
| Monitoring | Amazon CloudWatch |
| Infrastructure | Terraform |
| Configuration Management | Ansible |
| CI/CD | GitHub Actions |

## Migration Strategy

The project will follow these stages:

1. Build the simulated on-premises environment.
2. Containerize the application components.
3. Establish application communication and dependencies.
4. Document the existing infrastructure.
5. Develop the AWS target architecture.
6. Provision AWS infrastructure using Terraform.
7. Migrate the database to Amazon RDS.
8. Migrate documents to Amazon S3.
9. Deploy applications using ECS Fargate.
10. Configure security, monitoring, and backups.
11. Implement CI/CD automation.
12. Perform migration validation and cutover testing.

## Key Learning Objectives

- Enterprise application migration
- AWS networking and security
- Docker and Docker Compose
- Amazon ECS and Fargate
- Amazon RDS and S3
- Terraform and Ansible
- CI/CD automation
- Application monitoring
- Migration validation and rollback

## Project Status

Phase 1: Project structure and environment setup - Completed.

Phase 2: Source application development - In progress.
