# Chat 模块异常定义
# 定义聊天相关的自定义异常类型

class ChatException(Exception):
    """聊天模块基础异常"""
    def __init__(self, message: str, code: str = "CHAT_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class DifyServiceException(ChatException):
    """Dify 服务异常"""
    def __init__(self, message: str, status_code: int = None):
        self.status_code = status_code
        super().__init__(message, "DIFY_ERROR")


class ConfigurationError(ChatException):
    """配置错误异常"""
    def __init__(self, message: str):
        super().__init__(message, "CONFIG_ERROR")


class ValidationError(ChatException):
    """数据验证错误"""
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class RateLimitError(DifyServiceException):
    """API 请求频率限制异常"""
    def __init__(self, message: str = "API rate limit exceeded"):
        super().__init__(message, 429)


class AuthenticationError(DifyServiceException):
    """认证错误异常"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)
