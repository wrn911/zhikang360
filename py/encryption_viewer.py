#!/usr/bin/env python3
"""
加密文件查看工具
用于查看、测试和验证加密后的文件内容
"""

import os
import sys
from pathlib import Path

# 添加项目路径，以便导入自定义模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.encryption import encrypt_content, decrypt_content
except ImportError:
    print("❌ 无法导入加密模块，请确保 utils/encryption.py 存在")
    sys.exit(1)


def create_test_file():
    """创建一个测试文件并加密"""
    print("📝 创建测试文件...")

    # 测试内容
    test_content = """这是一个测试文档
包含中文内容：用户健康信息
血压：120/80 mmHg
血糖：5.6 mmol/L
过敏史：海鲜过敏
慢性病：高血压

This is test content in English.
Personal information: John Doe
Age: 35
Medical history: Diabetes"""

    # 保存原始文件
    original_file = "test_original.txt"
    with open(original_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    print(f"✅ 原始文件已保存：{original_file}")

    # 加密并保存
    user_id = 123  # 测试用户ID
    encrypted_content = encrypt_content(test_content, user_id)
    encrypted_file = "test_encrypted.txt.enc"

    with open(encrypted_file, 'w', encoding='utf-8') as f:
        f.write(encrypted_content)
    print(f"🔒 加密文件已保存：{encrypted_file}")

    return original_file, encrypted_file, user_id, test_content


def view_files(original_file, encrypted_file, user_id, original_content):
    """查看原始文件和加密文件的内容"""
    print("\n" + "=" * 50)
    print("📄 原始文件内容:")
    print("=" * 50)

    with open(original_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)

    print("\n" + "=" * 50)
    print("🔒 加密文件内容 (原始):")
    print("=" * 50)

    with open(encrypted_file, 'r', encoding='utf-8') as f:
        encrypted_content = f.read()
        print(f"文件大小: {len(encrypted_content)} 字符")
        print(f"前100字符: {encrypted_content[:100]}...")
        print(f"是否包含明文关键词 '血压': {'血压' in encrypted_content}")
        print(f"是否包含明文关键词 'John': {'John' in encrypted_content}")

    print("\n" + "=" * 50)
    print("🔓 解密后的内容:")
    print("=" * 50)

    try:
        decrypted_content = decrypt_content(encrypted_content, user_id)
        print(decrypted_content)

        # 验证解密是否正确
        if decrypted_content == original_content:
            print("\n✅ 解密成功！内容完全匹配")
        else:
            print("\n❌ 解密失败！内容不匹配")

    except Exception as e:
        print(f"\n❌ 解密失败: {str(e)}")


def test_different_users():
    """测试不同用户ID的加密效果"""
    print("\n" + "=" * 50)
    print("🧪 测试不同用户的加密效果:")
    print("=" * 50)

    test_text = "这是敏感的用户数据"

    for user_id in [1, 2, 123]:
        encrypted = encrypt_content(test_text, user_id)
        print(f"用户 {user_id}: {encrypted[:50]}...")

        # 尝试用错误的用户ID解密
        if user_id == 123:
            try:
                wrong_decrypt = decrypt_content(encrypted, 456)  # 错误的用户ID
                print(f"  ❌ 用错误用户ID解密成功: {wrong_decrypt}")
            except:
                print(f"  ✅ 用错误用户ID解密失败 (符合预期)")


def view_real_encrypted_file(file_path, user_id=None):
    """查看真实的加密文件"""
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return

    print(f"\n📂 查看文件: {file_path}")
    print("=" * 50)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"文件大小: {len(content)} 字符")
    print(f"文件内容预览: {content[:200]}...")

    if user_id and file_path.endswith('.enc'):
        print(f"\n🔓 尝试用用户ID {user_id} 解密:")
        try:
            decrypted = decrypt_content(content, user_id)
            print(f"解密成功! 内容预览: {decrypted[:200]}...")
        except Exception as e:
            print(f"解密失败: {str(e)}")


def main():
    """主函数"""
    print("🔐 加密文件查看工具")
    print("=" * 50)

    # 设置测试环境的密钥
    os.environ['MASTER_KEY'] = 'TEST_KEY_32_CHARS_FOR_DEMO_ONLY12'

    while True:
        print("""
选择操作:
1. 创建测试文件并查看加密效果
2. 测试不同用户ID的加密效果  
3. 查看指定的加密文件
4. 查看项目中的加密文件
5. 退出

请选择 (1-5): """, end="")

        choice = input().strip()

        if choice == '1':
            original_file, encrypted_file, user_id, original_content = create_test_file()
            view_files(original_file, encrypted_file, user_id, original_content)

        elif choice == '2':
            test_different_users()

        elif choice == '3':
            file_path = input("请输入文件路径: ").strip()
            user_id_input = input("请输入用户ID (可选): ").strip()
            user_id = int(user_id_input) if user_id_input else None
            view_real_encrypted_file(file_path, user_id)

        elif choice == '4':
            print("\n🔍 搜索项目中的加密文件:")

            # 搜索加密文件
            encrypted_files = []
            search_dirs = ['uploads', 'user_profiles']

            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    for root, dirs, files in os.walk(search_dir):
                        for file in files:
                            if file.endswith('.enc'):
                                encrypted_files.append(os.path.join(root, file))

            if encrypted_files:
                print(f"找到 {len(encrypted_files)} 个加密文件:")
                for i, file_path in enumerate(encrypted_files, 1):
                    print(f"{i}. {file_path}")

                try:
                    file_choice = int(input("选择文件编号查看: ")) - 1
                    if 0 <= file_choice < len(encrypted_files):
                        user_id_input = input("请输入用户ID: ").strip()
                        user_id = int(user_id_input) if user_id_input else None
                        view_real_encrypted_file(encrypted_files[file_choice], user_id)
                except (ValueError, IndexError):
                    print("❌ 无效选择")
            else:
                print("未找到加密文件")

        elif choice == '5':
            print("👋 再见!")
            break

        else:
            print("❌ 无效选择，请重试")


if __name__ == "__main__":
    main()