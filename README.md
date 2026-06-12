# Autonomous Cloud Remediation Agent (ACRA)

ACRA is an intelligent, event-driven, serverless backend system that uses LLMs to autonomously investigate cloud alerts, diagnose root causes, and take precise remediation actions.

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
