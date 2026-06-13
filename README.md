# Autonomous Cloud Remediation Agent (ACRA)

ACRA is an intelligent, event-driven, serverless backend system that uses LLMs to autonomously investigate cloud alerts, diagnose root causes, and take precise remediation actions.

## Core Capabilities

1. **Storage Layer (Storage Optimization & Lifecycle Guard)**
   - *Disk-Full Automation & Log Rotation:* Monitors EC2 storage volumes. If disk space hits 95% due to runaway application logs, the AI analyzes which log folders are the largest, archives old logs to an S3 bucket, clears local cache, and restarts the log service.
2. **Security Layer (Real-time Compliance & Governance Guard)**
   - *Automated IAM & Drift Remediation:* Watches AWS CloudTrail for security misconfigurations. If someone makes an S3 bucket public or opens an EC2 port (like port 22/SSH) to the entire internet (0.0.0.0/0), the AI immediately intercepts the event, evaluates the security risk, rewrites the security group/policy back to private, and flags the user who did it.
3. **Database & Messaging Layer (Deadlock & Queue Resolution)**
   - *Connection-Pool Clearance & DLQ Triage:* If a database connection hangs or an AWS SQS queue builds up with corrupted messages, the AI examines the stuck messages, determines why they are failing processing, logs the payload analysis, and flushes the queue safely.

## Phase 1: Local LLM Test

This phase demonstrates the agent's ability to reason through an alert and call mock tools.

### Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`.
   - Add your Gemini API Key to `.env`.

### Run

```bash
python src/agent.py
```
