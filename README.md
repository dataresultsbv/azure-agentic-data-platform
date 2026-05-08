# Agentic IoT Platform on Azure

## Overview

This project simulates an end-to-end IoT data platform on Azure, evolving towards an agentic AI-driven system capable of autonomous decision-making.

The first version of the platform will have synthetic telemetry data ingestion and then incrementally expands into intelligent processing, scalable infrastructure, and AI agent orchestration in future versions.

## Background

With over 15 years of experience in BI and data platforms, I have worked across the evolution from on-premise systems to modern cloud architectures on Azure. Currently, a new shift is emerging. The shift from data platforms that process information to systems that can reason, decide, and act.

This project captures that transition.

The first version starts with a solid data engineering foundation with simulated IoT ingestion, cloud-native pipelines, and infrastructure-as-code and evolves into an agentic AI platform with autonomous decision-making capabilities in later versions.

The focus is not just on building components, but on designing systems that scale from data processing to intelligent, agent-driven architectures. This aligns with the next generation of Azure solutions and the path towards Agentic AI architecture.

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

## Roadmap

### V1 – Data Ingestion

* IoT simulation
* Blob storage ingestion
* Terraform deployment
* Docker containerization 
* Github Actions CICD

### V2 – AI Agents

* Anomaly detection agent
* AI-based summarization

### V3 – Scalable Platform

* Migration to Kubernetes (AKS)
* Distributed workloads

### V4 – MLOps Integration

* Model training pipelines
* Model versioning and deployment

### V5 – Agentic Architecture

* Multi-agent orchestration
* Autonomous decision workflows
