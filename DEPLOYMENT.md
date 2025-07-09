# 🚀 消毒副产物预测系统 - 部署指南

## 📋 目录
- [本地部署](#本地部署)
- [云端部署](#云端部署)
- [故障排除](#故障排除)

## 🏠 本地部署

### 1. 环境要求
- **Python**: 3.8 或更高版本
- **内存**: 最少 4GB RAM（推荐 8GB）
- **存储**: 至少 2GB 可用空间
- **操作系统**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

### 2. 快速开始

#### 方法一：自动启动（推荐）
```bash
# 1. 激活conda环境
conda activate test_r1_env

# 2. 运行自动启动脚本
python run_app.py
```

#### 方法二：手动安装
```bash
# 1. 激活conda环境
conda activate test_r1_env

# 2. 安装Web应用依赖
pip install streamlit plotly

# 3. 启动应用
streamlit run app.py
```

### 3. 访问应用
- 🌐 **本地地址**: http://localhost:8501
- 📱 **移动端**: 同网络下其他设备可通过您的IP地址访问

## ☁️ 云端部署

### 1. Streamlit Cloud 部署

#### 步骤：
1. **准备GitHub仓库**
   ```bash
   # 确保代码已推送到GitHub
   git push origin main
   ```

2. **访问 Streamlit Cloud**
   - 前往 [share.streamlit.io](https://share.streamlit.io)
   - 使用GitHub账号登录

3. **创建应用**
   - 点击 "New app"
   - 选择您的GitHub仓库
   - 设置以下参数：
     - **Repository**: `your-username/dbps_prediction_test_r1`
     - **Branch**: `main`
     - **Main file path**: `app.py`

4. **配置环境**
   - Streamlit Cloud会自动识别 `requirements.txt`
   - 应用将自动构建和部署

#### 注意事项：
- ⚠️ **模型文件**: 需要先训练模型并提交 `.pth` 和 `.json` 文件
- 📁 **文件大小**: GitHub有100MB文件大小限制
- 🔧 **依赖管理**: 确保 `requirements.txt` 包含所有依赖

### 2. Heroku 部署

#### 准备文件：
1. **创建 Procfile**
   ```bash
   echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   ```

2. **创建 runtime.txt**
   ```bash
   echo "python-3.9.18" > runtime.txt
   ```

#### 部署步骤：
```bash
# 1. 安装Heroku CLI
# 访问: https://devcenter.heroku.com/articles/heroku-cli

# 2. 登录Heroku
heroku login

# 3. 创建应用
heroku create your-app-name

# 4. 推送代码
git push heroku main

# 5. 打开应用
heroku open
```

### 3. Docker 部署

#### 创建 Dockerfile：
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 复制文件
COPY requirements.txt .
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8501

# 健康检查
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 启动命令
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### 构建和运行：
```bash
# 构建镜像
docker build -t dbps-prediction .

# 运行容器
docker run -p 8501:8501 dbps-prediction
```

## 🔧 故障排除

### 常见问题

#### 1. 模型文件缺失
**问题**: `模型文件不存在，请先训练模型`

**解决方案**:
```bash
# 训练模型
python train.py

# 检查生成的文件
ls -la *.pth *.json
```

#### 2. 依赖安装失败
**问题**: `Import "torch" could not be resolved`

**解决方案**:
```bash
# 重新安装PyTorch
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cpu

# 重新安装其他依赖
pip install -r requirements.txt
```

#### 3. 端口被占用
**问题**: `Port 8501 is already in use`

**解决方案**:
```bash
# 方法1: 使用其他端口
streamlit run app.py --server.port=8502

# 方法2: 关闭占用端口的进程
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8501 | xargs kill
```

#### 4. 内存不足
**问题**: 模型加载时内存不足

**解决方案**:
- 关闭其他应用程序
- 使用更小的模型配置
- 增加系统虚拟内存

#### 5. 网络访问问题
**问题**: 局域网内其他设备无法访问

**解决方案**:
```bash
# 允许外部访问
streamlit run app.py --server.address=0.0.0.0

# 检查防火墙设置
# 允许8501端口通过防火墙
```

### 性能优化

#### 1. 模型加载优化
```python
# 在app.py中使用缓存
@st.cache_resource
def load_model():
    return ReactionPredictor(model_path, vocab_path)
```

#### 2. 内存优化
```python
# 清理GPU内存（如果使用GPU）
import torch
torch.cuda.empty_cache()
```

#### 3. 并发处理
```toml
# .streamlit/config.toml
[server]
maxUploadSize = 200
enableWebsocketCompression = true
```

## 📊 监控和日志

### 启用日志记录
```bash
# 详细日志
streamlit run app.py --logger.level=debug

# 保存日志到文件
streamlit run app.py > app.log 2>&1
```

### 性能监控
- 使用 `streamlit run app.py --server.enableStaticServing=true` 提高静态文件服务性能
- 监控内存使用情况
- 记录预测响应时间

## 🔐 安全配置

### 生产环境设置
```toml
# .streamlit/config.toml
[server]
enableCORS = false
enableXsrfProtection = true

[global]
developmentMode = false
```

### 环境变量管理
```bash
# 设置环境变量
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=localhost
```

## 📞 技术支持

如果遇到问题，请：
1. 检查本文档的故障排除部分
2. 查看应用日志文件
3. 确认所有依赖已正确安装
4. 验证模型文件完整性

**联系方式**: 创建GitHub Issue或提交PR

---

🎉 **恭喜！您的消毒副产物预测系统已成功部署！** 