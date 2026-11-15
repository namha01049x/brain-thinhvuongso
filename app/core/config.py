import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Brain Thịnh Vượng Số - AI OS"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    VAULT_DIR: Path = BASE_DIR / "vault_data"
    DATA_DIR: Path = BASE_DIR / ".data"
    DB_PATH: Path = DATA_DIR / "system.sqlite3"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Token Pruning & Budget Limits
    LIGHT_LANE_TOKEN_LIMIT: int = 2000
    HEAVY_LANE_TOKEN_LIMIT: int = 16000
    AUTO_COMMIT_GIT: bool = True
    
    # Default Provider
    DEFAULT_PROVIDER: str = "claude-code"
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure directories exist
settings.VAULT_DIR.mkdir(parents=True, exist_ok=True)
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
