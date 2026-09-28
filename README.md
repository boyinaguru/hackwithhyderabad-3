# MemoryDesk AI

A hackathon MVP for HackwithHyderabad 3.0: a customer-support AI agent that uses persistent Hindsight memory to remember customer history, previous fixes, preferences, and unresolved issues.

## Core demo
1. Start with a customer who has no useful remembered context.
2. Record one or more support interactions.
3. Retain important facts into Hindsight.
4. Ask a related question later.
5. Recall relevant memory.
6. Produce a more personalized response.
7. Show the memory timeline in the UI.

## Architecture

Frontend (React/Vite) -> FastAPI backend -> Agent orchestration -> Hindsight memory + LLM

## Tech
- Python / FastAPI
- React + Vite
- Hindsight
- OpenAI-compatible LLM API (Groq or another provider)
- In-memory demo data for customer profiles

## Environment
Copy `.env.example` to `.env` and configure your Hindsight and LLM settings.

## Run backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Run frontend
```bash
cd frontend
npm install
npm run dev
```

## Hackathon alignment
The project is intentionally narrow: one persona, one workflow, one clear value proposition, with memory central to the product experience.

## Important
Never commit API keys. Use `.env`.
