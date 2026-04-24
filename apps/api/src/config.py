from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env", override=False)


class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file=ROOT_DIR / ".env",
    env_file_encoding="utf-8",
    extra="ignore",
  )

  app_name: str = "MiroWorld API"
  app_env: str = "development"
  app_debug: bool = True
  host: str = "127.0.0.1"
  port: int = 8000
  frontend_origin: str = "http://127.0.0.1:4173"
  data_dir: Path = Field(default=ROOT_DIR / "data" / "runtime")
  fixtures_dir: Path = Field(default=ROOT_DIR / "fixtures")
  contracts_dir: Path = Field(default=ROOT_DIR / "contracts")
  llm_api_key: str | None = None
  llm_base_url: HttpUrl = "https://api.minimaxi.com/v1"
  llm_model_name: str = "MiniMax-M2.7-highspeed"
  llm_request_timeout: int = 120


@lru_cache(maxsize=1)
def get_settings() -> Settings:
  settings = Settings()
  settings.data_dir.mkdir(parents=True, exist_ok=True)
  (settings.data_dir / "projects").mkdir(parents=True, exist_ok=True)
  (settings.data_dir / "cache").mkdir(parents=True, exist_ok=True)
  (settings.data_dir / "process").mkdir(parents=True, exist_ok=True)
  return settings
