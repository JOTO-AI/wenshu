from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Database
    database_url: str
    database_url_sync: str
    
    # Redis
    redis_url: str
    
    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # Admin
    admin_email: str
    admin_password: str
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Casbin
    casbin_model_path: str = "./config/rbac_model.conf"
    casbin_policy_path: str = "./config/rbac_policy.csv"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
