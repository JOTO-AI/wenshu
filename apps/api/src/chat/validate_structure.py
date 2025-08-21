# 简单的模块结构验证
# 验证重构后的文件和类是否正确定义

import os
import importlib.util
import sys

def test_file_exists():
    """测试所有必需的文件是否存在"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
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

    print("📁 Checking file structure...")
    for file_name in required_files:
        file_path = os.path.join(current_dir, file_name)
        if os.path.exists(file_path):
            print(f"✅ {file_name} exists")
        else:
            print(f"❌ {file_name} missing")
            return False

    return True

def test_syntax():
    """测试Python文件的语法正确性"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    python_files = [
        'chat_service.py',
        'service.py',
        'router.py',
        'schemas.py',
        'models.py',
        'exceptions.py',
        'utils.py'
    ]

    print("\n🔍 Checking Python syntax...")
    for file_name in python_files:
        file_path = os.path.join(current_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()

            compile(code, file_path, 'exec')
            print(f"✅ {file_name} syntax OK")
        except SyntaxError as e:
            print(f"❌ {file_name} syntax error: {e}")
            return False
        except Exception as e:
            print(f"⚠️ {file_name} check failed: {e}")

    return True

def test_class_definitions():
    """测试关键类是否正确定义"""
    current_dir = os.path.dirname(os.path.abspath(__file__))

    print("\n🏗️ Checking class definitions...")

    # 检查异常类
    try:
        with open(os.path.join(current_dir, 'exceptions.py'), 'r') as f:
            content = f.read()
            if 'class ChatException' in content:
                print("✅ ChatException class defined")
            else:
                print("❌ ChatException class missing")
    except Exception as e:
        print(f"❌ Error checking exceptions.py: {e}")

    # 检查Schema类
    try:
        with open(os.path.join(current_dir, 'schemas.py'), 'r') as f:
            content = f.read()
            required_schemas = [
                'class ChatQueryRequest',
                'class ChatQueryResponse',
                'class FeedbackRequest',
                'class ChatHistoryRequest'
            ]

            for schema in required_schemas:
                if schema in content:
                    print(f"✅ {schema.replace('class ', '')} defined")
                else:
                    print(f"❌ {schema.replace('class ', '')} missing")
    except Exception as e:
        print(f"❌ Error checking schemas.py: {e}")

    # 检查服务类
    try:
        with open(os.path.join(current_dir, 'chat_service.py'), 'r') as f:
            content = f.read()
            if 'class DifyService' in content:
                print("✅ DifyService class defined")
            else:
                print("❌ DifyService class missing")
    except Exception as e:
        print(f"❌ Error checking chat_service.py: {e}")

    try:
        with open(os.path.join(current_dir, 'service.py'), 'r') as f:
            content = f.read()
            if 'class ChatService' in content:
                print("✅ ChatService class defined")
            else:
                print("❌ ChatService class missing")
    except Exception as e:
        print(f"❌ Error checking service.py: {e}")

def main():
    """运行所有检查"""
    print("🚀 Starting Chat Module Structure Validation\n")

    success = True

    # 文件存在性检查
    if not test_file_exists():
        success = False

    # 语法检查
    if not test_syntax():
        success = False

    # 类定义检查
    test_class_definitions()

    print(f"\n{'🎉 All checks passed!' if success else '💥 Some checks failed!'}")

    # 显示模块结构
    print("\n📋 Current module structure:")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for item in sorted(os.listdir(current_dir)):
        if item.endswith('.py'):
            print(f"   📄 {item}")
        elif os.path.isdir(os.path.join(current_dir, item)):
            print(f"   📁 {item}/")

    return success

if __name__ == "__main__":
    main()
