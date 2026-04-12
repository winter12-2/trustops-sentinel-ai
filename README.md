# trustops-sentinel-ai
TrustOps Sentinel AI is an agentic platform for enterprise IT/security that prevents unsafe actions before execution and enables post-incident analysis. It combines real-time policy enforcement, AI reasoning, vector memory, external intelligence, and blockchain audit logs to deliver proactive, explainable, and trustworthy decision-making.

Demo Video Link - https://drive.google.com/drive/folders/1cakyp9akn2yMJsRVkd3KRl-X1a7XZvAQ?usp=sharing

🚀 TrustOps Sentinel AI
Real-Time Policy Firewall for Agentic Enterprise Systems

📌 Overview
TrustOps Sentinel AI is a real-time AI governance platform that prevents unsafe actions before execution.
Unlike traditional monitoring systems, this platform:
intercepts actions pre-execution
evaluates risk using AI + rules + memory + live intelligence
enforces decisions:
ALLOW
ALLOW WITH REDACTION
REQUIRE APPROVAL
BLOCK
maps threat levels:
ALLOW
MONITOR
QUARANTINE
ESCALATE

🧠 System Architecture
User / UI (HTML + Bootstrap + JS)
        ↓
FastAPI Backend (Policy Engine)
        ↓
Redis (Streams + Memory)
        ↓
Tavily (Live Intelligence)
        ↓
MySQL (Persistent Storage)
        ↓
Watsonx Orchestrate (Agent Layer)
        ↓
(Next Phase) Blockchain Audit (PPoS)


🛠 Tech Stack
Backend
FastAPI
Python 3.13
Pydantic
Memory + Streaming
Redis (Docker)
Intelligence Layer
Tavily API
Database
MySQL
Frontend
HTML + Bootstrap
jQuery
Agent Layer
IBM watsonx Orchestrate (delegated)

📂 Project Structure
trustops-sentinel-ai/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models/
│   ├── services/
│   │   ├── policy_engine.py
│   │   ├── redis_service.py
│   │   ├── mysql_service.py
│   │   ├── tavily_service.py
│   │
│   └── static/
│       ├── index.html
│       ├── dashboard.html
│       ├── logs.html
│       ├── css/
│       └── js/
│
├── orchestrate/
│   ├── tools/
│   │   └── guarded_send_email.py
│   ├── agents/
│   │   └── risk_aware_ops.agent.yaml
│
├── requirements.txt
└── README.md


⚙️ Setup Instructions

🔹 STEP 1 — Clone & Setup Environment
git clone <repo-url>
cd trustops-sentinel-ai

Create virtual environment:
python -m venv .venv
.\.venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt


🔹 STEP 2 — Environment Variables
Create .env:
APP_NAME=TrustOps Sentinel AI
APP_ENV=development

REDIS_URL=redis://localhost:6379/0

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=trustops_db

TAVILY_API_KEY=your_api_key


🔹 STEP 3 — Start Redis (Docker)
docker run -d --name redis -p 6379:6379 redis:latest

Verify:
docker ps


🔹 STEP 4 — Setup MySQL
Create DB:
CREATE DATABASE trustops_db;

Tables will be auto-used by service layer.

🔹 STEP 5 — Run Backend
uvicorn app.main:app --reload

Check:
http://127.0.0.1:8000/health

Expected:
{"status":"ok"}


🔹 STEP 6 — Open Frontend
http://127.0.0.1:8000/

Pages:
/static/index.html
/static/dashboard.html
/static/logs.html

🎯 Dashboard Features
Manual input form
File attachment simulation
4 auto-fill scenarios
Live evaluation
Colored decision badges
Auto scroll to results

🧪 API Endpoints
Endpoint
Description
/evaluate-action
Core policy engine
/action-logs
Fetch logs
/redis-test
Redis check
/tavily-test
Live intelligence
/incidents
Incident storage


🧠 Policy Engine Logic
Layer 1 — Rules
External + attachment → risk
PII → high risk
Bulk send → high risk
Layer 2 — Memory
Redis vector-like retrieval
Layer 3 — Live Verification
Tavily checks claims
Layer 4 — Decision
Score
Decision
<30
ALLOW
30–59
REDACT
60–79
APPROVAL
80+
BLOCK


🤖 Watsonx Orchestrate (Delegated Task)
👩‍💻 Assigned To: Teammate

🔹 Goal
Integrate watsonx as:
👉 Agent runtime layer

🔹 What to do
1. Install
pip install ibm-watsonx-orchestrate


2. Get credentials
From watsonx UI:
Settings → API details
Copy:
Service URL
API Key

3. Configure environment
orchestrate env add cloudwo -u "<URL>" --type ibm_iam --activate


4. Import tool
orchestrate tools import -k python -f orchestrate/tools/guarded_send_email.py


5. Import agent
orchestrate agents import -f orchestrate/agents/risk_aware_ops.agent.yaml


🔹 Expected Flow
User → Watsonx Agent → guarded_send_email → FastAPI → Decision


⚠️ Important Notes
Backend must be running
Endpoint /evaluate-action must work
Tool uses localhost API

🔥 Demo Scenarios
Use Case 1 — Safe
→ Internal email → ALLOW
Use Case 2 — Medium Risk
→ External + attachment → APPROVAL
Use Case 3 — Verified Claim
→ External + claim → CONDITIONAL
Use Case 4 — High Risk
→ Bulk + PII → BLOCK

📊 Logs
Stored in MySQL
Streamed via Redis
Visualized in /logs

🚀 Future Work
Blockchain audit (PPoS)
Approval workflow UI
Multi-agent orchestration
Vector DB upgrade

🎯 Final Outcome
This system transforms enterprise AI from:
❌ Reactive monitoring
➡️ ✅ Proactive, explainable, real-time control

👨‍💻 Team Notes
Backend: complete ✅
Frontend: complete ✅
Watsonx: pending ✅
Blockchain: pending ✅

