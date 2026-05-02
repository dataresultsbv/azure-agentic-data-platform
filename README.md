# Agentic IoT Platform on Azure

## Overview

This project simulates an end-to-end IoT data platform on Azure, evolving towards an agentic AI-driven system capable of autonomous decision-making.

The first version of the platform will have synthetic telemetry data ingestion and then incrementally expands into intelligent processing, scalable infrastructure, and AI agent orchestration in future versions.

## Why This Project

I am a Data Platform Lead with over 15 years of experience in business intelligence and data engineering. From the start of my career, I have worked extensively with on-premise data platforms and have been part of the transition towards modern cloud-based architectures. Currently, we are entering a new wave of innovation in the data landscape: the rise of Agentic AI systems. Unlike traditional data platforms that focus primarily on ingestion, transformation, and reporting, these systems introduce autonomous decision-making, reasoning, and action-taking capabilities. This shift requires a fundamentally different approach to system design.

Personally I am also riding the wave from Data Platform Lead towards a Agentic AI Platform Architect. This project is a hands-on exploration from myself in achieving my goals. See it as a portfolio to demonstrate the things I learn in my path towards multiple new Azure certifications. 

The first version starts with a solid, cloud-native data engineering foundation: simulating IoT telemetry, building ingestion pipelines, and applying infrastructure-as-code principles. From there, it incrementally evolves into a more advanced architecture that incorporates AI agents, intelligent processing, and eventually multi-agent orchestration.

The goal is not just to build a working system, but to demonstrate architectural thinking across multiple stages of maturity:

From batch-based ingestion to intelligent, metadata driven data processing.
From static pipelines to adaptive, agent-driven workflows.
From infrastructure-focused design to end-to-end intelligent systems.

By continuously expanding this project with new capabilities (AI agents, Kubernetes, MLOps, and orchestration), it becomes a living representation of how modern data platforms are evolving towards intelligent, autonomous systems.

## Goals

* Simulate large-scale IoT telemetry data
* Build a cloud-native ingestion pipeline
* Apply infrastructure-as-code principles
* Evolve towards agent-based AI systems
* Demonstrate real-world Azure architecture patterns

## Architecture (Current version: V1)

* Python-based IoT simulator
* Containerized using Docker
* Deployed via Azure Container Instances
* Data stored in Azure Blob Storage (partitioned)

## Tech Stack (Current version: V1)

* Azure (Blob Storage, Container Instances)
* Terraform (Infrastructure as Code)
* Docker (Containerization)
* Python (Data simulation)
* GitHub Actions (Orchestration)

## Data Structure

/raw/year=YYYY/month=MM/day=DD/sensor_data.json

## Roadmap

### V1 – Data Ingestion

* IoT simulation
* Blob storage ingestion
* Terraform deployment

### V2 – AI Agents

* Anomaly detection agent
* AI-based summarization (Azure OpenAI)

### V3 – Scalable Platform

* Migration to Kubernetes (AKS)
* Distributed workloads

### V4 – MLOps Integration

* Model training pipelines
* Model versioning and deployment

### V5 – Agentic Architecture

* Multi-agent orchestration
* Autonomous decision workflows
