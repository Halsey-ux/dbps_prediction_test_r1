# 部署说明 (DEPLOY.md)

## Python 版本兼容性说明

### 为什么使用 Python 3.12.4 而不是最新版本？

我们选择使用 Python 3.12.4 而不是 Python 3.13.x 的原因如下：

#### 1. **PyTorch 兼容性问题**
- **问题**: PyTorch 2.0.1 在 Python 3.13.5 环境下没有预编译的轮子 (wheels)
- **表现**: 部署时出现错误 `torch==2.0.1 has no wheels with a matching Python ABI tag`
- **解决方案**: 升级到 PyTorch 2.6.0 + Python 3.12.4 的稳定组合

#### 2. **依赖包生态系统成熟度**
- Python 3.12.x 拥有更成熟的科学计算包生态系统
- 大多数 ML/DL 包都对 Python 3.12 有完整的支持和测试
- Python 3.13 作为较新版本，许多包还在适配阶段

#### 3. **Streamlit Cloud 环境优化**
- Streamlit Cloud 对 Python 3.12.x 有更好的支持
- 避免了新版本 Python 可能带来的兼容性风险
- 确保部署环境的稳定性和可预测性

### 当前配置

```txt
# runtime.txt
python-3.12.4

# requirements.txt  
torch==2.6.0  # 升级以支持 Python 3.12+
numpy==1.24.3
pandas==2.0.3
tqdm==4.65.0
streamlit==1.28.1
plotly==5.17.0
```

### 部署验证

经过测试，Python 3.12.4 + PyTorch 2.6.0 的组合能够：
- ✅ 在 Streamlit Cloud 上成功安装所有依赖
- ✅ 正常运行 ReactionTransformer 模型
- ✅ 提供稳定的 Web 应用服务

### 未来升级计划

当 PyTorch 和相关依赖包对 Python 3.13+ 提供完整支持后，我们会考虑升级到最新的 Python 版本。目前的配置优先考虑稳定性和兼容性。

## ⚠️ Streamlit Cloud 部署重要说明

### Python 版本配置限制

**重要提醒**: Streamlit Cloud **不会自动读取 `runtime.txt` 文件**来确定 Python 版本。

#### 如何正确设置 Python 版本：

1. **在 Streamlit Cloud 管理界面手动选择**
   - 登录 [Streamlit Cloud](https://share.streamlit.io/)
   - 进入应用设置页面
   - 在 "Advanced settings" 中手动选择 Python 版本
   - 推荐选择：**Python 3.12.x**

2. **当前部署问题的根本原因**
   - Streamlit Cloud 默认使用 Python 3.13.5
   - `runtime.txt` 中的 `python-3.12.4` 配置被忽略
   - 导致 PyTorch 2.6.0 安装失败（Python 3.13 ABI 不兼容）

#### 解决步骤：

1. ✅ **确保 requirements.txt 正确**: `torch==2.6.0`
2. ⚠️ **在 Streamlit Cloud UI 中手动选择 Python 3.12.x**
3. 🔄 **重新部署 (Rebuild) 应用**

### 依赖管理最佳实践

- 只维护一个 `requirements.txt` 文件
- 避免使用 `uv.lock`, `Pipfile`, `environment.yml` 等可能冲突的锁定文件
- 使用固定版本号 (`==`) 而非版本范围 (`>=`, `<`) 确保可重现性 