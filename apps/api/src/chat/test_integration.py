# Chat 模块基本结构测试
# 验证重构后的模块是否正确构建

import pytest
import os


def test_module_files_exist():
    """测试模块文件是否存在"""
    current_dir = os.path.dirname(__file__)
    required_files = [
        'chat_service.py',
        'service.py',
        'router.py',
        'schemas.py',
        'models.py',
        'exceptions.py',
        'utils.py',
        '__init__.py'
    ]

    for file_name in required_files:
        file_path = os.path.join(current_dir, file_name)
        assert os.path.exists(file_path), f"Required file {file_name} does not exist"


def test_python_syntax():
    """测试Python文件语法正确性"""
    current_dir = os.path.dirname(__file__)
    python_files = [
        'chat_service.py',
        'service.py',
        'router.py',
        'schemas.py',
        'models.py',
        'exceptions.py',
        'utils.py'
    ]

    for file_name in python_files:
        file_path = os.path.join(current_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        # 简单的语法检查
        try:
            compile(code, file_path, 'exec')
        except SyntaxError as e:
            pytest.fail(f"Syntax error in {file_name}: {e}")


def test_class_definitions():
    """测试关键类定义是否存在"""
    current_dir = os.path.dirname(__file__)

    # 检查异常类
    exceptions_path = os.path.join(current_dir, 'exceptions.py')
    with open(exceptions_path, 'r', encoding='utf-8') as f:
        exceptions_content = f.read()

    assert 'class ChatException' in exceptions_content
    assert 'class DifyServiceException' in exceptions_content
    assert 'class ValidationError' in exceptions_content

    # 检查服务类
    service_path = os.path.join(current_dir, 'chat_service.py')
    with open(service_path, 'r', encoding='utf-8') as f:
        service_content = f.read()

    assert 'class DifyService' in service_content

    # 检查业务逻辑类
    chat_service_path = os.path.join(current_dir, 'service.py')
    with open(chat_service_path, 'r', encoding='utf-8') as f:
        chat_service_content = f.read()

    assert 'class ChatService' in chat_service_content


if __name__ == "__main__":
    # 直接运行测试
    test_module_files_exist()
    test_python_syntax()
    test_class_definitions()
    print("✅ All basic tests passed!")
