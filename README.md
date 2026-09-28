# MemoryDesk AI

> **HackwithHyderabad 3.0 — persistent-memory customer support agent**

MemoryDesk is a focused AI support workflow: it remembers customer history, previous troubleshooting attempts, successful fixes and preferences, then uses that context in later conversations.

## Why this fits the challenge

The product makes persistent memory visible and central:
- **Retain** meaningful support interactions in Hindsight.
- **Recall** relevant history before responding.
- Use recalled context to personalize the next response.
- Show the recalled memories in the UI so a judge can see why the response changed.
- A one-click demo seed makes the memory progression reproducible.

Hindsight provides the core Retain, Recall and Reflect operations; this MVP uses Retain + Recall directly and an LLM for response generation.

## Demo story

1. Open **Rahul Sharma**.
2. Click **Seed demo memory**.
3. Ask: **“It happened again.”**
4. Point to the memory panel.
5. Explain that Hindsight recalled the previous Wi-Fi issue and the successful driver-reinstall fix.
6. Ask a second related question and show that the agent avoids starting from generic troubleshooting.

## Architecture

```
React UI
  │
  ▼
FastAPI Support Agent
  ├── Hindsight Retain  ──► persistent memory bank
  ├── Hindsight Recall  ◄── relevant customer history
  └── LLM              ──► personalized response
```

## Run locally

### 1. Backend

```bash
cd backend
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set:
- `HINDSIGHT_BASE_URL`
- `HINDSIGHT_API_KEY`
- `HINDSIGHT_BANK_ID`
- `LLM_API_KEY`
- `LLM_MODEL`

Hindsight's current Python client is installed as `hindsight-client`; the official quickstart uses `Hindsight(base_url=...)` with `retain`, `recall`, and `reflect`.

Start:

```bash
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL, normally `http://localhost:5173`.

## Repository layout

```
backend/
  app/
    agent.py
    hindsight.py
    main.py
    models.py
    demo_data.py
frontend/
  src/
    main.jsx
    styles.css
docs/
  ARCHITECTURE.md
  DEMO_SCRIPT.md
  SUBMISSION.md
```

## Environment and security

Never commit API keys. Use `.env`, which is ignored by Git.

## Scope

One workflow, one persona, one clear value proposition: **support that remembers**. The prototype intentionally avoids unrelated features so the memory behavior is easy to demonstrate.
