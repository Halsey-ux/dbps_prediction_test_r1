#!/usr/bin/env python3
"""
消毒副产物预测系统 - 本地环境安装脚本
自动设置完整的本地开发环境
"""

import os
import sys
import subprocess
import platform
import shutil

def print_header():
    """打印安装程序头部"""
    print("=" * 70)
    print("🧪 消毒副产物预测系统 - 本地环境安装程序")
    print("=" * 70)
    print("📦 此脚本将帮助您设置完整的本地开发环境")
    print()

def check_system():
    """检查系统环境"""
    print("🔍 检查系统环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print(f"❌ Python版本过低: {sys.version}")
        print("   需要Python 3.8或更高版本")
        return False
    
    print(f"✅ Python版本: {sys.version.split()[0]}")
    print(f"✅ 操作系统: {platform.system()} {platform.release()}")
    
    # 检查pip
    try:
        subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                      capture_output=True, check=True)
        print("✅ pip 已安装")
    except subprocess.CalledProcessError:
        print("❌ pip 未找到，请先安装pip")
        return False
    
    return True

def check_conda():
    """检查和推荐Conda环境"""
    print("\n🐍 检查Conda环境...")
    
    # 检查是否有conda
    conda_cmd = shutil.which('conda')
    if conda_cmd:
        print("✅ 检测到Conda")
        
        # 检查当前环境
        current_env = os.environ.get('CONDA_DEFAULT_ENV', 'base')
        print(f"📍 当前环境: {current_env}")
        
        if current_env == 'base':
            print("⚠️  建议创建专用的conda环境")
            create_env = input("🤖 是否创建专用环境 'test_r1_env'? (Y/n): ").lower()
            
            if create_env in ['', 'y', 'yes']:
                return create_conda_environment()
            else:
                print("📝 您可以稍后手动创建环境：")
                print("   conda create -n test_r1_env python=3.12 -y")
                print("   conda activate test_r1_env")
        else:
            print("✅ 已在专用环境中")
    else:
        print("❓ 未检测到Conda")
        print("💡 推荐安装Anaconda或Miniconda以获得更好的环境管理")
        print("   下载地址: https://www.anaconda.com/download")
    
    return True

def create_conda_environment():
    """创建Conda环境"""
    print("\n🔨 创建Conda环境...")
    
    try:
        # 创建环境
        print("📦 创建环境 'test_r1_env' (Python 3.12)...")
        subprocess.run([
            'conda', 'create', '-n', 'test_r1_env', 
            'python=3.12', '-y'
        ], check=True)
        
        print("✅ Conda环境创建成功!")
        print("📝 请运行以下命令激活环境：")
        print("   conda activate test_r1_env")
        print("   python setup_local.py  # 重新运行此脚本")
        
        return False  # 需要用户手动激活环境后重新运行
        
    except subprocess.CalledProcessError:
        print("❌ Conda环境创建失败")
        return True  # 继续安装

def install_dependencies():
    """安装项目依赖"""
    print("\n📦 安装项目依赖...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ 找不到requirements.txt文件")
        return False
    
    try:
        print("🔄 更新pip...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'
        ], check=True)
        
        print("🔄 安装项目依赖...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], check=True)
        
        print("✅ 依赖安装完成!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        print("💡 尝试手动安装：")
        print("   pip install -r requirements.txt")
        return False

def setup_data():
    """检查和设置数据文件"""
    print("\n📊 检查数据文件...")
    
    # 检查数据目录
    if not os.path.exists('data'):
        print("📁 创建data目录...")
        os.makedirs('data')
    
    # 检查训练数据
    if os.path.exists('data/sample_data.json'):
        print("✅ 训练数据已存在")
    else:
        print("⚠️  训练数据不存在")
        print("📝 请确保在data/目录下放置sample_data.json文件")
    
    return True

def check_model_status():
    """检查模型状态"""
    print("\n🤖 检查模型状态...")
    
    model_files = ['transformer_model.pth', 'vocabulary.json']
    missing_files = [f for f in model_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"⚠️  缺少模型文件: {', '.join(missing_files)}")
        print("📝 您需要训练模型：")
        print("   python train.py")
        
        if os.path.exists('data/sample_data.json'):
            train_now = input("🤖 是否现在开始训练模型？(y/N): ").lower()
            if train_now in ['y', 'yes']:
                print("🚀 开始训练模型...")
                try:
                    subprocess.run([sys.executable, 'train.py'], check=True)
                    print("✅ 模型训练完成!")
                except subprocess.CalledProcessError:
                    print("❌ 模型训练失败，请手动运行: python train.py")
    else:
        print("✅ 模型文件已存在")

def create_launch_script():
    """创建便捷启动脚本"""
    print("\n🚀 创建启动脚本...")
    
    if platform.system() == "Windows":
        # Windows批处理文件
        script_content = """@echo off
echo 🧪 启动消毒副产物预测系统...
python run_app.py
pause
"""
        with open('start_app.bat', 'w', encoding='utf-8') as f:
            f.write(script_content)
        print("✅ 创建了Windows启动脚本: start_app.bat")
        
    else:
        # Unix shell脚本
        script_content = """#!/bin/bash
echo "🧪 启动消毒副产物预测系统..."
python3 run_app.py
"""
        with open('start_app.sh', 'w') as f:
            f.write(script_content)
        os.chmod('start_app.sh', 0o755)
        print("✅ 创建了Shell启动脚本: start_app.sh")

def print_usage_guide():
    """打印使用指南"""
    print("\n" + "=" * 70)
    print("🎉 本地环境安装完成!")
    print("=" * 70)
    print("📝 使用指南：")
    print()
    print("1️⃣  启动应用:")
    print("   方式一: python run_app.py")
    if platform.system() == "Windows":
        print("   方式二: 双击 start_app.bat")
    else:
        print("   方式二: ./start_app.sh")
    print()
    print("2️⃣  开发模式（自动重载）:")
    print("   python run_app.py --dev")
    print()
    print("3️⃣  训练模型:")
    print("   python train.py")
    print()
    print("4️⃣  测试应用:")
    print("   python test_app.py")
    print()
    print("🔗 应用访问地址: http://localhost:8501")
    print("📚 详细文档: README.md")
    print("=" * 70)

def main():
    """主函数"""
    print_header()
    
    # 检查当前目录
    if not os.path.exists('app.py'):
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 检查系统环境
    if not check_system():
        sys.exit(1)
    
    # 检查Conda环境
    if not check_conda():
        sys.exit(0)  # 需要用户激活环境
    
    # 安装依赖
    if not install_dependencies():
        sys.exit(1)
    
    # 设置数据
    setup_data()
    
    # 检查模型
    check_model_status()
    
    # 创建启动脚本
    create_launch_script()
    
    # 打印使用指南
    print_usage_guide()

if __name__ == "__main__":
    main() 