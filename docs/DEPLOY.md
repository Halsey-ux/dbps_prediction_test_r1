# 🚀 消毒副产物预测系统 - 本地部署指南

本指南详细介绍如何在本地环境中部署和运行消毒副产物预测系统。

## 📋 目录

- [🎯 快速开始](#🎯-快速开始)
- [🔧 详细安装步骤](#🔧-详细安装步骤)
- [🐍 环境管理](#🐍-环境管理)
- [🤖 模型训练](#🤖-模型训练)
- [🌐 应用启动](#🌐-应用启动)
- [🛠️ 高级配置](#🛠️-高级配置)
- [🔍 故障排除](#🔍-故障排除)
- [📊 性能优化](#📊-性能优化)

## 🎯 快速开始

### 🚀 一键部署（推荐新手）

```bash
# 1. 获取项目
git clone https://github.com/Halsey-ux/dbps_prediction_test_r1.git
cd dbps_prediction_test_r1

# 2. 一键安装
python setup_local.py

# 3. 启动应用
python run_app.py
```

### ⚡ 专家模式（熟悉Python环境）

```bash
# 快速安装和启动
git clone https://github.com/Halsey-ux/dbps_prediction_test_r1.git
cd dbps_prediction_test_r1
conda create -n test_r1_env python=3.12 -y && conda activate test_r1_env
pip install -r requirements.txt
python train.py  # 训练模型（首次运行）
python run_app.py
```

## 🔧 详细安装步骤

### 步骤1：系统要求检查

#### 🖥️ 操作系统
- **Windows**: Windows 10/11 (64位)
- **macOS**: macOS 10.14+ (Intel/Apple Silicon)
- **Linux**: Ubuntu 18.04+, CentOS 7+, 或其他主流发行版

#### 🐍 Python环境
```bash
# 检查Python版本（需要3.8+）
python --version
# 或
python3 --version

# 检查pip
pip --version
```

**最低要求**: Python 3.8
**推荐版本**: Python 3.12
**不支持**: Python 2.x, Python 3.7及以下

#### 💾 硬件要求
- **RAM**: 最少4GB，推荐8GB+
- **存储**: 至少2GB可用空间
- **CPU**: 任意现代CPU（多核心推荐）
- **GPU**: 可选，NVIDIA GPU支持CUDA加速

### 步骤2：获取项目代码

#### 方法A：Git克隆（推荐）
```bash
# 克隆完整项目
git clone https://github.com/Halsey-ux/dbps_prediction_test_r1.git
cd dbps_prediction_test_r1

# 检查项目完整性
ls -la  # 应该看到app.py, model.py等文件
```

#### 方法B：下载ZIP包
1. 访问 [项目GitHub页面](https://github.com/Halsey-ux/dbps_prediction_test_r1)
2. 点击绿色"Code"按钮
3. 选择"Download ZIP"
4. 解压到本地目录

### 步骤3：创建虚拟环境

#### 🐍 Conda环境（强烈推荐）

**安装Conda（如果没有）**:
```bash
# Windows/macOS: 下载Anaconda
# https://www.anaconda.com/download

# Linux: 下载Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

**创建项目环境**:
```bash
# 创建专用环境
conda create -n test_r1_env python=3.12 -y

# 激活环境
conda activate test_r1_env

# 验证环境
python --version  # 应显示Python 3.12.x
which python      # 应显示conda环境路径
```

#### 🔧 venv环境（备选方案）

```bash
# 创建虚拟环境
python -m venv test_r1_env

# 激活环境
# Windows:
test_r1_env\Scripts\activate
# macOS/Linux:
source test_r1_env/bin/activate

# 验证激活
echo $VIRTUAL_ENV  # 应显示环境路径
```

### 步骤4：安装依赖包

#### 🔄 自动安装（推荐）
```bash
# 确保在正确环境中
conda activate test_r1_env  # 或激活你的venv

# 升级基础工具
pip install --upgrade pip setuptools wheel

# 安装项目依赖
pip install -r requirements.txt

# 验证关键包
python -c "import torch; print(f'PyTorch版本: {torch.__version__}')"
python -c "import streamlit; print(f'Streamlit版本: {streamlit.__version__}')"
```

#### 🎯 手动安装（故障排除）
如果自动安装失败，可以逐个安装：

```bash
# 深度学习框架
pip install torch>=2.0.0

# Web框架
pip install streamlit>=1.28.0

# 数据处理
pip install numpy>=1.24.0 pandas>=2.0.0

# 可视化
pip install plotly>=5.15.0

# 机器学习
pip install scikit-learn>=1.3.0

# 工具包
pip install tqdm>=4.65.0

# 开发工具（可选）
pip install jupyter>=1.0.0 matplotlib>=3.7.0
```

## 🐍 环境管理

### 🔄 环境切换

```bash
# 列出所有conda环境
conda env list

# 激活项目环境
conda activate test_r1_env

# 退出环境
conda deactivate

# 删除环境（清理时使用）
conda env remove -n test_r1_env
```

### 📦 依赖管理

```bash
# 查看已安装包
pip list

# 导出环境（用于共享）
pip freeze > my_requirements.txt

# 更新包
pip install --upgrade torch streamlit

# 检查包兼容性
pip check
```

### 🔍 环境诊断

```bash
# 检查Python环境
python -c "
import sys
print(f'Python版本: {sys.version}')
print(f'执行路径: {sys.executable}')
print(f'模块搜索路径: {sys.path[:3]}...')
"

# 检查关键依赖
python -c "
try:
    import torch, streamlit, numpy, pandas
    print('✅ 所有关键依赖已安装')
except ImportError as e:
    print(f'❌ 缺少依赖: {e}')
"
```

## 🤖 模型训练

### 📊 数据准备

#### 检查训练数据
```bash
# 验证数据文件
ls -la data/
cat data/sample_data.json | head -n 5  # 查看数据格式
```

#### 数据格式要求
训练数据应为JSON格式：
```json
[
    {
        "reactant_smiles": "CCO",
        "conditions": {
            "pH": 7.0,
            "disinfectant": "chlorine"
        },
        "product_smiles": "CCO.Cl"
    }
]
```

### 🚀 开始训练

#### 🎯 快速训练
```bash
# 使用默认参数训练
python train.py
```

#### 🔧 自定义训练
```bash
# 查看训练选项
python train.py --help

# 自定义训练参数
python train.py \
    --epochs 50 \
    --batch_size 16 \
    --learning_rate 0.001 \
    --model_dim 256
```

#### 📊 训练监控

训练过程中会显示：
- **损失值**: 每个epoch的训练损失
- **学习率**: 当前学习率状态
- **进度条**: 训练进度和预计完成时间
- **GPU使用**: GPU利用率（如果使用GPU）

```bash
# 实时监控训练
# 训练会显示类似输出:
# Epoch 1/30: 100%|██████████| 45/45 [00:23<00:00, 1.95it/s, loss=2.45]
# Epoch 2/30: 100%|██████████| 45/45 [00:22<00:00, 2.04it/s, loss=2.12]
```

#### 🎯 训练输出
成功训练后会生成：
- `transformer_model.pth`: 训练好的模型权重
- `vocabulary.json`: SMILES词汇表
- 训练日志和损失图表

## 🌐 应用启动

### 🚀 基础启动

#### 方法1：智能启动脚本（推荐）
```bash
# 启动应用（自动检测环境和端口）
python run_app.py

# 开发模式（支持热重载）
python run_app.py --dev
```

启动脚本功能：
- ✅ 自动检测Python环境
- ✅ 验证依赖安装
- ✅ 检查模型文件
- ✅ 自动选择可用端口
- ✅ 自动打开浏览器

#### 方法2：直接启动
```bash
# 直接使用Streamlit
streamlit run app.py

# 指定端口和地址
streamlit run app.py --server.port=8501 --server.address=localhost
```

#### 方法3：便捷脚本
```bash
# Windows用户
start_app.bat

# macOS/Linux用户
./start_app.sh
```

### 🔧 启动选项

#### 端口配置
```bash
# 使用特定端口
streamlit run app.py --server.port=8502

# 允许外部访问（局域网）
streamlit run app.py --server.address=0.0.0.0

# 禁用统计收集
streamlit run app.py --browser.gatherUsageStats=false
```

#### 开发选项
```bash
# 启用文件监视（自动重载）
streamlit run app.py --server.runOnSave=true

# 启用错误详情显示
streamlit run app.py --client.showErrorDetails=true
```

### 🌐 访问应用

启动成功后：
1. **本地访问**: http://localhost:8501
2. **局域网访问**: http://[你的IP]:8501
3. **浏览器会自动打开**（使用run_app.py时）

## 🛠️ 高级配置

### ⚡ 性能优化

#### GPU加速配置
```bash
# 检查CUDA支持
python -c "
import torch
print(f'CUDA可用: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU数量: {torch.cuda.device_count()}')
    print(f'GPU名称: {torch.cuda.get_device_name(0)}')
"

# 强制使用CPU（如果GPU有问题）
export CUDA_VISIBLE_DEVICES=""
python run_app.py
```

#### 内存优化
```python
# 在model.py中调整批处理大小
BATCH_SIZE = 8  # 从16减少到8以节省内存

# 在train.py中启用梯度累积
accumulation_steps = 4  # 累积4步再更新
```

### 🔐 安全配置

#### 本地网络访问
```bash
# 仅本地访问（默认，最安全）
streamlit run app.py --server.address=localhost

# 局域网访问（需要时使用）
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

#### 数据保护
- 训练数据和模型文件保存在本地
- 不会上传任何数据到云端
- 预测结果仅在本地计算

### 📊 监控和日志

#### 应用监控
```bash
# 查看Streamlit日志
streamlit run app.py 2>&1 | tee streamlit.log

# 监控系统资源
# Windows: 任务管理器
# macOS: 活动监视器
# Linux: htop 或 top
```

#### 错误日志
日志文件位置：
- **Windows**: `%USERPROFILE%\.streamlit\logs\`
- **macOS/Linux**: `~/.streamlit/logs/`

## 🔍 故障排除

### 🚨 常见问题及解决方案

#### 问题1：Python版本错误
**错误**: `Python version 3.7 is not supported`
```bash
# 解决方案：升级Python
# 1. 卸载旧版本Python
# 2. 安装Python 3.8+
# 3. 重新创建虚拟环境
conda create -n test_r1_env python=3.12 -y
```

#### 问题2：依赖安装失败
**错误**: `Failed to build torch` 或 `No matching distribution found`
```bash
# 解决方案1：升级pip
pip install --upgrade pip setuptools wheel

# 解决方案2：使用conda安装
conda install pytorch torchvision torchaudio -c pytorch

# 解决方案3：使用清华镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 问题3：端口被占用
**错误**: `Port 8501 is already in use`
```bash
# 解决方案1：使用run_app.py（自动选择端口）
python run_app.py

# 解决方案2：手动指定端口
streamlit run app.py --server.port=8502

# 解决方案3：杀死占用端口的进程
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8501 | xargs kill -9
```

#### 问题4：模型文件缺失
**错误**: `FileNotFoundError: transformer_model.pth`
```bash
# 解决方案：训练模型
python train.py

# 或检查数据文件
ls -la data/sample_data.json
```

#### 问题5：内存不足
**错误**: `CUDA out of memory` 或应用崩溃
```bash
# 解决方案1：使用CPU
export CUDA_VISIBLE_DEVICES=""

# 解决方案2：减少批处理大小
# 编辑train.py，设置batch_size=4

# 解决方案3：关闭其他应用
# 释放更多内存
```

#### 问题6：导入错误
**错误**: `ModuleNotFoundError: No module named 'torch'`
```bash
# 解决方案1：检查环境激活
conda activate test_r1_env
which python  # 确认使用正确的Python

# 解决方案2：重新安装
pip uninstall torch
pip install torch>=2.0.0
```

### 🔧 诊断工具

#### 环境诊断脚本
```bash
# 创建诊断脚本
cat > diagnose.py << 'EOF'
import sys
import subprocess
import importlib

def check_environment():
    print("🔍 环境诊断报告")
    print("=" * 50)
    
    # Python版本
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    
    # 关键包检查
    packages = ['torch', 'streamlit', 'numpy', 'pandas', 'plotly']
    for pkg in packages:
        try:
            module = importlib.import_module(pkg)
            version = getattr(module, '__version__', 'Unknown')
            print(f"✅ {pkg}: {version}")
        except ImportError:
            print(f"❌ {pkg}: 未安装")
    
    # CUDA检查
    try:
        import torch
        print(f"CUDA可用: {torch.cuda.is_available()}")
    except:
        print("CUDA检查失败")
    
    # 文件检查
    import os
    files = ['app.py', 'model.py', 'train.py', 'data/sample_data.json']
    for file in files:
        status = "✅" if os.path.exists(file) else "❌"
        print(f"{status} {file}")

if __name__ == "__main__":
    check_environment()
EOF

# 运行诊断
python diagnose.py
```

### 📞 获取帮助

如果问题仍然存在：

1. **检查日志**: 查看详细错误信息
2. **搜索Issue**: 在GitHub项目中搜索类似问题
3. **创建Issue**: 提供详细的错误信息和环境描述
4. **社区求助**: 在相关技术社区提问

**提Bug时请包含**:
- 操作系统版本
- Python版本
- 完整错误信息
- 重现步骤
- 诊断脚本输出

## 📊 性能优化

### ⚡ 启动优化

#### 快速启动技巧
```bash
# 预热模型（首次运行后更快）
python -c "from predict import ReactionPredictor; print('模型预热完成')"

# 使用SSD存储项目文件
# 确保项目在SSD而不是HDD上

# 关闭不必要的后台程序
# 释放更多CPU和内存资源
```

#### 缓存配置
```python
# 在app.py中启用Streamlit缓存
@st.cache_data
def load_model():
    return ReactionPredictor("transformer_model.pth", "vocabulary.json")

# 缓存预测结果
@st.cache_data
def predict_reaction(smiles, ph, disinfectant):
    return predictor.predict(smiles, ph, disinfectant)
```

### 🔧 运行时优化

#### CPU优化
```bash
# 设置OpenMP线程数
export OMP_NUM_THREADS=4

# PyTorch线程数
export MKL_NUM_THREADS=4
```

#### 内存优化
```python
# 在predict.py中启用内存清理
import gc
import torch

def cleanup_memory():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
```

### 📈 监控性能

#### 资源监控
```bash
# 安装监控工具
pip install psutil

# 创建监控脚本
cat > monitor.py << 'EOF'
import psutil
import time

def monitor_resources():
    while True:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        print(f"CPU: {cpu:5.1f}% | 内存: {memory:5.1f}%")
        time.sleep(5)

if __name__ == "__main__":
    monitor_resources()
EOF

# 运行监控
python monitor.py
```

## 🎯 最佳实践

### 🛡️ 开发最佳实践

1. **使用虚拟环境**: 始终在独立环境中开发
2. **定期备份**: 备份训练好的模型和重要数据
3. **版本控制**: 使用git跟踪代码变更
4. **测试优先**: 修改代码前先运行测试
5. **文档更新**: 保持文档与代码同步

### 🚀 部署最佳实践

1. **环境一致性**: 开发和生产使用相同的Python版本
2. **依赖固定**: 使用具体版本号而不是范围
3. **资源监控**: 定期检查系统资源使用
4. **安全配置**: 仅在需要时开放网络访问
5. **备份策略**: 定期备份模型和配置文件

### 🔄 维护最佳实践

1. **定期更新**: 保持依赖包为最新稳定版
2. **性能监控**: 关注应用性能变化
3. **日志分析**: 定期查看错误日志
4. **用户反馈**: 收集和处理用户问题
5. **持续改进**: 根据使用情况优化配置

---

## 🎉 部署完成

恭喜！您已经成功在本地部署了消毒副产物预测系统。

### 📋 快速检查清单

- ✅ Python 3.8+ 已安装
- ✅ 虚拟环境已创建并激活
- ✅ 项目依赖已安装
- ✅ 模型已训练（或使用预训练模型）
- ✅ 应用成功启动
- ✅ 可以通过浏览器访问

### 🔗 常用命令

```bash
# 激活环境
conda activate test_r1_env

# 启动应用
python run_app.py

# 开发模式
python run_app.py --dev

# 训练模型
python train.py

# 运行测试
python test_app.py
```

### 📚 下一步

- 🧪 尝试预测不同的化学反应
- 🔧 自定义模型参数以适应您的数据
- 📊 分析预测结果和性能指标
- 🌐 考虑与其他系统集成
- 📖 阅读详细的技术文档

**祝您使用愉快！** 🎉

---

**📞 需要帮助？**
- 📖 查看 [README.md](../README.md) 了解基础使用
- 🐛 在 [GitHub Issues](https://github.com/Halsey-ux/dbps_prediction_test_r1/issues) 报告问题
- 💬 参与社区讨论获取支持 