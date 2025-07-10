#!/usr/bin/env python3
"""
消毒副产物预测系统本地启动脚本
自动检查环境和依赖，启动Streamlit应用（本地优化版）
"""

import os
import sys
import subprocess
import importlib.util
import socket
import webbrowser
import time
from threading import Timer

def check_package(package_name):
    """检查包是否已安装"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def get_available_port(start_port=8501):
    """获取可用端口"""
    for port in range(start_port, start_port + 100):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def check_conda_environment():
    """检查是否在conda环境中"""
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    if conda_env:
        print(f"🐍 当前Conda环境: {conda_env}")
        return True
    return False

def install_requirements():
    """安装所需依赖"""
    print("📦 正在检查和安装依赖...")
    
    # 检查关键包
    required_packages = [
        ('streamlit', 'streamlit>=1.28.0'),
        ('torch', 'torch>=2.0.0'),
        ('plotly', 'plotly>=5.15.0'),
        ('pandas', 'pandas>=2.0.0'),
        ('numpy', 'numpy>=1.24.0'),
        ('sklearn', 'scikit-learn>=1.3.0'),
        ('tqdm', 'tqdm>=4.65.0')
    ]
    
    missing_packages = []
    for package, pip_name in required_packages:
        if not check_package(package):
            missing_packages.append(pip_name)
            print(f"  ❌ 缺少: {package}")
        else:
            print(f"  ✅ 已安装: {package}")
    
    if missing_packages:
        print(f"\n⚠️  需要安装 {len(missing_packages)} 个依赖包")
        
        # 询问用户是否自动安装
        auto_install = input("🤖 是否自动安装缺失的依赖？(Y/n): ").lower()
        if auto_install in ['', 'y', 'yes']:
            print("🔄 正在自动安装...")
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '--upgrade'
                ] + missing_packages)
                print("✅ 依赖安装完成!")
            except subprocess.CalledProcessError:
                print("❌ 依赖安装失败，请手动运行：")
                print(f"pip install {' '.join(missing_packages)}")
                return False
        else:
            print("📝 请手动安装依赖：")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    else:
        print("✅ 所有依赖已满足!")
    
    return True

def check_model_files():
    """检查模型文件是否存在"""
    model_files = ['transformer_model.pth', 'vocabulary.json']
    data_files = ['data/sample_data.json']
    
    missing_model = [f for f in model_files if not os.path.exists(f)]
    missing_data = [f for f in data_files if not os.path.exists(f)]
    
    if missing_data:
        print(f"\n❌ 缺少训练数据: {', '.join(missing_data)}")
        return False
    
    if missing_model:
        print(f"\n⚠️  缺少模型文件: {', '.join(missing_model)}")
        print("📝 检测到训练数据，可以开始训练模型：")
        print("   🔄 运行: python train.py")
        
        train_now = input("🤖 是否现在开始训练模型？(y/N): ").lower()
        if train_now in ['y', 'yes']:
            print("🚀 开始训练模型...")
            try:
                subprocess.run([sys.executable, 'train.py'], check=True)
                print("✅ 模型训练完成!")
                return True
            except subprocess.CalledProcessError:
                print("❌ 模型训练失败")
                return False
        else:
            return False
    
    print("✅ 模型文件检查通过!")
    return True

def open_browser(port):
    """延迟打开浏览器"""
    def _open():
        time.sleep(2)  # 等待2秒让服务器启动
        webbrowser.open(f'http://localhost:{port}')
    
    Timer(0, _open).start()

def start_streamlit(dev_mode=False):
    """启动Streamlit应用"""
    # 获取可用端口
    port = get_available_port()
    if not port:
        print("❌ 无法找到可用端口")
        return
    
    print(f"\n🚀 启动消毒副产物预测系统...")
    print(f"📱 应用端口: {port}")
    print(f"🔗 访问地址: http://localhost:{port}")
    
    if not dev_mode:
        print("🌐 浏览器将自动打开...")
        open_browser(port)
    
    print("🛑 按 Ctrl+C 停止应用\n")
    
    # 构建启动命令
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'app.py',
        f'--server.port={port}',
        '--server.address=localhost'
    ]
    
    if not dev_mode:
        cmd.extend([
            '--browser.gatherUsageStats=false',
            '--client.showErrorDetails=false'
        ])
    else:
        cmd.extend([
            '--server.runOnSave=true',
            '--server.fileWatcherType=auto'
        ])
        print("🔧 开发模式已启用（自动重载）")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except FileNotFoundError:
        print("❌ 找不到Streamlit，请确保已正确安装")

def main():
    """主函数"""
    print("="*60)
    print("🧪 消毒副产物预测系统 - 本地启动程序")
    print("="*60)
    
    # 解析命令行参数
    dev_mode = '--dev' in sys.argv or '-d' in sys.argv
    if dev_mode:
        print("🔧 开发模式启用")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        print(f"当前版本: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python版本: {sys.version.split()[0]}")
    
    # 检查conda环境
    check_conda_environment()
    
    # 检查当前目录
    if not os.path.exists('app.py'):
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)
    
    print("✅ 项目目录检查通过")
    
    # 检查并安装依赖
    if not install_requirements():
        sys.exit(1)
    
    # 检查模型文件
    model_ready = check_model_files()
    
    if not model_ready:
        choice = input("\n❓ 模型未就绪，是否继续启动应用？(y/N): ").lower()
        if choice not in ['y', 'yes']:
            print("👋 请先准备模型文件，然后重新启动应用")
            sys.exit(0)
        print("⚠️  应用将启动，但预测功能可能不可用")
    
    # 启动应用
    start_streamlit(dev_mode)

if __name__ == "__main__":
    main() 