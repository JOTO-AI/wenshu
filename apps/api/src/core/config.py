# 配置管理
# 用于管理应用配置、环境变量等

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    app_name: str = "智能问数 API"
    debug: bool = False
    
    class Config:
        env_file = ".env"


settings = Settings()