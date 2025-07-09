#!/usr/bin/env python3
"""
消毒副产物预测系统启动脚本
自动检查环境和依赖，启动Streamlit应用
"""

import os
import sys
import subprocess
import importlib.util

def check_package(package_name):
    """检查包是否已安装"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_requirements():
    """安装所需依赖"""
    print("📦 正在检查和安装依赖...")
    
    # 检查关键包
    required_packages = {
        'streamlit': 'streamlit>=1.28.0',
        'torch': 'torch',
        'plotly': 'plotly>=5.17.0',
        'pandas': 'pandas>=1.3.0',
        'numpy': 'numpy>=1.21.0'
    }
    
    missing_packages = []
    for package, pip_name in required_packages.items():
        if not check_package(package):
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"⚠️  缺少以下依赖: {', '.join(missing_packages)}")
        print("🔄 正在自动安装...")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'] + missing_packages
            )
            print("✅ 依赖安装完成!")
        except subprocess.CalledProcessError:
            print("❌ 依赖安装失败，请手动运行：")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    else:
        print("✅ 所有依赖已满足!")
    
    return True

def check_model_files():
    """检查模型文件是否存在"""
    model_files = ['transformer_model.pth', 'vocabulary.json']
    missing_files = [f for f in model_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"\n⚠️  缺少模型文件: {', '.join(missing_files)}")
        print("📝 请按以下步骤训练模型：")
        print("   1. 确保数据文件存在: data/sample_data.json")
        print("   2. 运行训练脚本: python train.py")
        print("   3. 等待训练完成")
        print("   4. 重新启动Web应用")
        return False
    
    print("✅ 模型文件检查通过!")
    return True

def start_streamlit():
    """启动Streamlit应用"""
    print("\n🚀 启动消毒副产物预测系统...")
    print("📱 Web应用将在浏览器中自动打开")
    print("🔗 访问地址: http://localhost:8501")
    print("🛑 按 Ctrl+C 停止应用\n")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port=8501',
            '--server.address=localhost',
            '--browser.gatherUsageStats=false'
        ])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except FileNotFoundError:
        print("❌ 找不到Streamlit，请确保已正确安装")

def main():
    """主函数"""
    print("="*60)
    print("🧪 消毒副产物预测系统 - 启动程序")
    print("="*60)
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        sys.exit(1)
    
    print(f"✅ Python版本: {sys.version.split()[0]}")
    
    # 检查并安装依赖
    if not install_requirements():
        sys.exit(1)
    
    # 检查模型文件
    model_ready = check_model_files()
    
    if not model_ready:
        choice = input("\n❓ 模型文件不存在，是否继续启动应用？(y/N): ").lower()
        if choice not in ['y', 'yes']:
            print("👋 请先训练模型，然后重新启动应用")
            sys.exit(0)
        print("⚠️  应用将启动，但预测功能需要先训练模型")
    
    # 启动应用
    start_streamlit()

if __name__ == "__main__":
    main() 