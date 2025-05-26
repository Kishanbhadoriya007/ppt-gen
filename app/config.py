# app/config.py
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    SECRET_KEY: str = "your_super_secret_key" # Default if not in .env

    GEMINI_API_KEY: str | None = None
    GPT_API_KEY: str | None = None
    DEEPSEEK_API_KEY: str | None = None
    MISTRAL_API_KEY: str | None = None

    MONGO_DATABASE_URL: str | None = None
    MONGO_DATABASE_NAME: str | None = None

    DEFAULT_SLIDES: int = 5
    MAX_SLIDES: int = 10
    DEFAULT_TOKENS_PER_SLIDE: int = 250
    MAX_TOKENS_PER_SLIDE: int = 500 # Max tokens for content on a single slide
    MAX_TOTAL_TOKENS_GEMINI: int = 8000 # Max total tokens for a request to Gemini

    GENERATED_PPT_TTL_SECONDS: int = 60
    
    # Directories
    TEMPLATES_DIR: Path = BASE_DIR / "app" / "templates"
    STATIC_DIR: Path = BASE_DIR / "app" / "static"
    SERVER_TEMPLATES_DIR: Path = BASE_DIR / "app" / "server_templates"
    GENERATED_PPTS_DIR: Path = BASE_DIR / "app" / "generated_ppts"


    class Config:
        env_file = BASE_DIR.parent / ".env" # Correct path to .env if it's in project root
        env_file_encoding = 'utf-8'

settings = Settings()

# Ensure necessary directories exist
settings.SERVER_TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
settings.GENERATED_PPTS_DIR.mkdir(parents=True, exist_ok=True)