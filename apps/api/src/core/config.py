# 配置管理
# 用于管理应用配置、环境变量等

from pydantic_settings import BaseSettings
from pydantic import SecretStr, ConfigDict
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    model_config = ConfigDict(env_file=".env")

    # 应用基础配置
    app_name: str = "智能问数 API"
    debug: bool = False

    # CORS 配置
    cors_origins: str = "http://localhost:3000"

    # 日志配置
    log_level: str = "INFO"

    # Dify 服务配置
    dify_base_url: str = "https://api.dify.ai/v1"
    dify_api_key: Optional[SecretStr] = None
    dify_analysis_api_key: Optional[SecretStr] = None

    # Chat 功能配置
    chat_max_history: int = 100
    chat_request_timeout: int = 30

    # 数据库配置（可选）
    database_url: Optional[str] = None

    # 安全配置（可选）
    secret_key: Optional[SecretStr] = None


settings = Settings()
