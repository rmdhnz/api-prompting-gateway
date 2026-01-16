from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

def find_project_root() -> Path : 
  current = Path(__file__).resolve()
  for parent in current.parents : 
    if (parent / ".env").exists() : 
      return parent
    raise RuntimeError("Fucking .env not found")

base_dir = find_project_root()
env_path = base_dir / ".env"
load_dotenv()


class Config(BaseSettings) : 
  model_config = SettingsConfigDict(
    env_file=str(env_path),
    env_file_encoding="utf-8",
    extra="ignore",
    case_sensitive=False,
  )

  APP_ENV: str = "local"
  MYSQL_HOST: str = "127.0.0.1"
  MYSQL_PORT: int = 3306
  MYSQL_DB: str
  MYSQL_USER: str
  MYSQL_PASSWORD: str
  BAUS_API_KEY: str



config = Config()

