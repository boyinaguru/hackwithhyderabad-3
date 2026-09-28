import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    hindsight_base_url: str = os.getenv("HINDSIGHT_BASE_URL", "http://localhost:8888")
    hindsight_bank_id: str = os.getenv("HINDSIGHT_BANK_ID", "memorydesk-demo")
    hindsight_api_key: str = os.getenv("HINDSIGHT_API_KEY", "")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")

settings = Settings()
