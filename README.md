# SRE Auto-Remediation Agent

## Overview
This project aims to build an autonomous SRE Agent designed to reduce human intervention in production environments. It acts as a "Digital SRE" that pairs with human engineers to handle repetitive incident responses, perform real-time diagnostics, and execute remediation runbooks safely.

## Core Philosophy 
1.  **Safety First**: The agent operates with strict "Safety Valves" (e.g., max retries, impact blast radius limits).
2.  **Observability**: Every action is logged, audited, and traceable.
3.  **Idempotency**: Remediation actions can be repeated without side effects.
4.  **Feedback Loops**: The agent verifies if a fix actually worked.

## Architecture
The agent consists of three main loops:
1.  **Detection (The Eyes)**: Connects to observability platforms (Prometheus, CloudWatch, Datadog) to detect anomalies.
2.  **Decision (The Brain)**: Matches alerts to "Runbooks". Can be rule-based or AI-assisted.
3.  **Execution (The Hands)**: Executes safe, pre-approved scripts (restart pods, clear cache, rollback deployments).

## Quick Start

### Prerequisites
- Python 3.10+
- `pip install -r requirements.txt`

### Running the Demo
This demo proves the **Safety Circuit Breaker**. It simulates a critical incident and shows the agent attempting to fix it, but eventually stopping itself to prevent a cascading failure (simulated infinite loop).
```bash
python demo.py
```

### Running the Agent (Live Mode)
This runs the agent against your **local system** (checking CPU/Memory).
```bash
python src/main.py
```

## Technology Stack
- **Language**: Python 3.10+
- **Configuration**: YAML-based Remediation Policies
- **Observability**: Prometheus (for metrics), Structured Logging
- **Integration**: Webhooks / API

## Roadmap
- [ ] **Phase 1: Foundation**: Basic framework to listen for alerts and log them.
- [ ] **Phase 2: Deterministic Runbooks**: Implement simple "If CPU > 90% -> Scale Up" logic.
- [ ] **Phase 3: Safety Guardrails**: Implement "Do Not Harm" logic (e.g., don't restart more than 10% of fleet).
- [ ] **Phase 4: AI Analysis**: (Optional) Use LLM to analyze complex root causes.
