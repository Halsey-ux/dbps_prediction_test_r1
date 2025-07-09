#!/usr/bin/env python3
"""
Web应用测试脚本
验证app.py的基本功能和导入
"""

import sys
import os

def test_imports():
    """测试所有必要的导入"""
    print("🔍 测试Python包导入...")
    
    try:
        import streamlit as st
        print("✅ Streamlit导入成功")
    except ImportError as e:
        print(f"❌ Streamlit导入失败: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        print("✅ Plotly导入成功")
    except ImportError as e:
        print(f"❌ Plotly导入失败: {e}")
        return False
    
    try:
        import torch
        print(f"✅ PyTorch导入成功 (版本: {torch.__version__})")
    except ImportError as e:
        print(f"❌ PyTorch导入失败: {e}")
        return False
    
    try:
        import pandas as pd
        import numpy as np
        print("✅ 数据处理包导入成功")
    except ImportError as e:
        print(f"❌ 数据处理包导入失败: {e}")
        return False
    
    return True

def test_project_modules():
    """测试项目模块导入"""
    print("\n🔍 测试项目模块导入...")
    
    try:
        from model import ReactionTransformer
        print("✅ 模型模块导入成功")
    except ImportError as e:
        print(f"❌ 模型模块导入失败: {e}")
        return False
    
    try:
        from utils import SMILESVocabulary, encode_conditions
        print("✅ 工具模块导入成功")
    except ImportError as e:
        print(f"❌ 工具模块导入失败: {e}")
        return False
    
    try:
        from predict import ReactionPredictor
        print("✅ 预测模块导入成功")
    except ImportError as e:
        print(f"❌ 预测模块导入失败: {e}")
        return False
    
    return True

def test_app_structure():
    """测试app.py文件结构"""
    print("\n🔍 测试应用文件结构...")
    
    if not os.path.exists("app.py"):
        print("❌ app.py文件不存在")
        return False
    
    print("✅ app.py文件存在")
    
    # 检查关键配置文件
    config_files = [
        ".streamlit/config.toml",
        "requirements.txt",
        "run_app.py",
        "DEPLOYMENT.md"
    ]
    
    for file_path in config_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在")
        else:
            print(f"❌ {file_path} 不存在")
    
    return True

def test_model_files():
    """检查模型文件状态"""
    print("\n🔍 检查模型文件...")
    
    model_files = ["transformer_model.pth", "vocabulary.json"]
    model_exists = True
    
    for file_path in model_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在")
        else:
            print(f"⚠️  {file_path} 不存在 (需要先训练模型)")
            model_exists = False
    
    if not model_exists:
        print("\n📝 要使用完整功能，请运行以下命令:")
        print("   python train.py")
    
    return True

def test_app_syntax():
    """测试app.py语法"""
    print("\n🔍 测试app.py语法...")
    
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            app_code = f.read()
        
        # 尝试编译代码
        compile(app_code, "app.py", "exec")
        print("✅ app.py语法检查通过")
        return True
    except SyntaxError as e:
        print(f"❌ app.py语法错误: {e}")
        return False
    except Exception as e:
        print(f"❌ app.py检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 消毒副产物预测系统 - Web应用测试")
    print("=" * 60)
    
    tests = [
        ("Python包导入", test_imports),
        ("项目模块导入", test_project_modules),
        ("应用文件结构", test_app_structure),
        ("模型文件状态", test_model_files),
        ("应用语法检查", test_app_syntax)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ 测试 '{test_name}' 异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过! Web应用已准备就绪!")
        print("\n🚀 启动应用:")
        print("   方法1: python run_app.py")
        print("   方法2: streamlit run app.py")
        print("\n🌐 访问地址: http://localhost:8501")
    else:
        print("⚠️  部分测试未通过，请检查问题后重试")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 