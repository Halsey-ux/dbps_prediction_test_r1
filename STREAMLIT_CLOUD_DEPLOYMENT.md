# 🚀 Streamlit Cloud 部署指南

## 消毒副产物预测系统云端部署

### 📋 部署概览

- **应用URL**: https://dbpspredictiontestr1-vjsdv9wdme5qfrqnqcwdqq.streamlit.app/
- **GitHub仓库**: https://github.com/Halsey-ux/dbps_prediction_test_r1
- **Python版本**: 3.9.18
- **PyTorch版本**: 2.0.1 (CPU版本)

### 🛠️ 部署配置

#### 1. 依赖管理
```bash
# requirements.txt 已优化为Streamlit Cloud版本
torch==2.0.1              # 稳定的CPU版本
torchvision==0.15.2       # 配套版本
numpy==1.24.3             # 兼容版本
pandas==2.0.3             # 稳定版本
streamlit==1.28.1         # 推荐版本
plotly==5.15.0            # 可视化
scikit-learn==1.3.0       # 机器学习工具
```

#### 2. Python运行时
```bash
# runtime.txt
python-3.9.18
```

#### 3. Streamlit配置
```toml
# .streamlit/config.toml
[global]
developmentMode = false
dataFrameSerialization = "legacy"

[server]
port = 8501
enableCORS = false
maxUploadSize = 200
fileWatcherType = "none"
headless = true
runOnSave = false
```

### 🚀 部署步骤

#### 步骤1: 准备GitHub仓库
```bash
# 确保所有文件已推送到GitHub
git add .
git commit -m "🚀 Streamlit Cloud部署优化"
git push origin main
```

#### 步骤2: 访问Streamlit Cloud
1. 打开 [Streamlit Cloud](https://share.streamlit.io/)
2. 使用GitHub账户登录
3. 点击 "New app"

#### 步骤3: 配置应用
- **Repository**: `Halsey-ux/dbps_prediction_test_r1`
- **Branch**: `main`
- **Main file path**: `app.py`
- **App URL**: `dbpspredictiontestr1-vjsdv9wdme5qfrqnqcwdqq`

#### 步骤4: 部署设置
- 确保Python版本设置为3.9.18
- 检查requirements.txt文件路径
- 验证模型文件大小（29MB < 200MB限制）

### 📊 文件检查清单

#### 必需文件
- [ ] `app.py` - 主应用文件
- [ ] `requirements.txt` - 依赖配置
- [ ] `runtime.txt` - Python版本
- [ ] `.streamlit/config.toml` - Streamlit配置

#### 模型文件
- [ ] `transformer_model.pth` (29MB) - 预训练模型
- [ ] `vocabulary.json` (590B) - 词汇表
- [ ] `model.py` - 模型定义
- [ ] `predict.py` - 预测引擎
- [ ] `utils.py` - 工具函数

#### 数据文件
- [ ] `data/sample_data.json` - 示例数据

### 🔧 兼容性优化

#### PyTorch版本兼容性
```python
# 在app.py中添加版本检查
import torch
print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")
```

#### 内存优化
```python
# 模型加载优化
@st.cache_resource
def load_model():
    return ReactionPredictor(
        model_path="transformer_model.pth",
        vocab_path="vocabulary.json",
        device="cpu"  # 强制使用CPU
    )
```

### 🐛 故障排除

#### 常见问题及解决方案

**问题1: 模块导入错误**
```bash
# 解决方案：确保所有依赖在requirements.txt中
pip freeze > requirements.txt
```

**问题2: PyTorch版本冲突**
```bash
# 解决方案：使用CPU版本
torch==2.0.1
torchvision==0.15.2
```

**问题3: 内存不足**
```python
# 解决方案：优化模型加载
torch.set_num_threads(1)  # 限制线程数
```

**问题4: 模型文件加载失败**
```python
# 解决方案：检查文件路径
import os
print("当前工作目录:", os.getcwd())
print("模型文件存在:", os.path.exists("transformer_model.pth"))
```

### 📈 性能优化

#### 1. 缓存策略
```python
# 使用Streamlit缓存
@st.cache_resource
def load_model():
    return ReactionPredictor(...)

@st.cache_data
def predict_product(smiles, ph, disinfectant):
    return predictor.predict_product(smiles, ph, disinfectant)
```

#### 2. 内存管理
```python
# 限制内存使用
import gc
gc.collect()  # 强制垃圾回收
```

#### 3. 异步处理
```python
# 使用进度条显示处理状态
with st.spinner('正在预测...'):
    result = predict_product(smiles, ph, disinfectant)
```

### 🔄 更新部署

#### 自动部署
```bash
# 推送更改到GitHub，Streamlit Cloud会自动重新部署
git add .
git commit -m "更新模型或代码"
git push origin main
```

#### 手动重启
1. 访问 https://share.streamlit.io/
2. 找到你的应用
3. 点击 "Reboot" 按钮

### 📊 监控和日志

#### 应用状态监控
- 访问Streamlit Cloud控制面板
- 查看应用运行状态
- 检查错误日志

#### 性能监控
```python
# 在app.py中添加性能监控
import time
start_time = time.time()
# ... 预测代码 ...
end_time = time.time()
st.info(f"预测耗时: {end_time - start_time:.2f}秒")
```

### 🌟 最佳实践

1. **版本锁定**: 使用精确版本号避免冲突
2. **错误处理**: 添加完整的异常处理
3. **用户反馈**: 显示加载状态和错误信息
4. **资源管理**: 优化内存和CPU使用
5. **日志记录**: 记录关键操作和错误

### 🔗 相关链接

- [Streamlit Cloud文档](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit部署指南](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)
- [PyTorch CPU版本](https://pytorch.org/get-started/locally/)

---

### 🎯 部署完成后验证

1. **访问应用**: https://dbpspredictiontestr1-vjsdv9wdme5qfrqnqcwdqq.streamlit.app/
2. **功能测试**: 尝试预测几个示例
3. **性能检查**: 确认响应时间在合理范围内
4. **错误处理**: 测试无效输入的处理

### 🚨 重要提醒

- 确保模型文件已推送到GitHub
- 检查所有依赖版本兼容性
- 监控应用内存使用情况
- 定期更新安全补丁

部署完成后，你的消毒副产物预测系统将在云端24/7运行，为用户提供专业的化学反应预测服务！🎉 