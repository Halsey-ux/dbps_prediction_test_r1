# 🧪 消毒副产物预测系统 (本地版)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-green.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

基于深度学习Transformer架构的化学反应路径预测系统，专门用于预测消毒副产物的形成。**专为本地部署优化**。

## 🌟 项目特点

- 🤖 **深度学习架构**: 基于Transformer编码器-解码器模型
- 🧬 **化学专业**: 专门针对消毒反应和副产物预测
- 🌐 **本地Web界面**: 现代化的Streamlit Web应用
- ⚡ **快速预测**: 秒级响应时间
- 🔧 **简易部署**: 一键本地安装和启动
- 🛠️ **开发友好**: 支持开发模式和热重载

## 🚀 快速开始

### 🎯 **方法一：一键安装（推荐）**

```bash
# 1. 克隆项目
git clone https://github.com/Halsey-ux/dbps_prediction_test_r1.git
cd dbps_prediction_test_r1

# 2. 运行一键安装脚本
python setup_local.py

# 3. 启动应用
python run_app.py
```

### 🛠️ **方法二：手动安装**

#### 1. 环境准备

```bash
# 推荐使用Conda创建环境
conda create -n test_r1_env python=3.12 -y
conda activate test_r1_env

# 或使用venv
python -m venv test_r1_env
# Windows:
test_r1_env\Scripts\activate
# macOS/Linux:
source test_r1_env/bin/activate
```

#### 2. 安装依赖

```bash
# 升级pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

#### 3. 训练模型

```bash
# 训练ReactionTransformer模型
python train.py
```

#### 4. 启动应用

```bash
# 普通模式
python run_app.py

# 开发模式（自动重载）
python run_app.py --dev

# 或使用便捷脚本
# Windows: 双击 start_app.bat
# macOS/Linux: ./start_app.sh
```

#### 5. 访问应用
🔗 打开浏览器访问: http://localhost:8501

## 📁 项目结构

```
dbps_prediction_test_r1/
├── 🧬 核心AI模块
│   ├── model.py              # ReactionTransformer模型定义
│   ├── train.py              # 模型训练脚本
│   ├── predict.py            # 模型预测脚本
│   └── utils.py              # 工具函数库
├── 🌐 Web应用模块
│   ├── app.py                # Streamlit Web应用
│   ├── run_app.py            # 本地启动脚本
│   └── test_app.py           # 应用测试脚本
├── 📊 数据与模型
│   ├── data/
│   │   └── sample_data.json  # 示例训练数据
│   ├── transformer_model.pth # 训练好的模型权重
│   └── vocabulary.json       # SMILES词汇表
├── ⚙️ 环境配置
│   ├── requirements.txt      # Python依赖
│   ├── setup_local.py        # 本地环境安装脚本
│   ├── start_app.bat         # Windows启动脚本
│   └── start_app.sh          # macOS/Linux启动脚本
└── 📖 文档
    ├── README.md             # 项目说明（本文件）
    └── docs/                 # 详细文档
```

## 💻 使用指南

### 🎮 Web界面操作

1. **输入反应条件**
   - **反应物SMILES**: 分子的SMILES表示法
     - 示例: `CCO` (乙醇), `c1ccc(cc1)O` (苯酚)
   - **pH值**: 反应溶液的酸碱度 (5.0-9.0)
   - **消毒剂类型**: 
     - `chlorine`: 氯气 (Cl₂) - 强氧化性，快速反应
     - `chloramine`: 氯胺 (NH₂Cl) - 中等氧化性，持续性强
     - `ozone`: 臭氧 (O₃) - 最强氧化性，无残留

2. **查看预测结果**
   - 预测的副产物SMILES
   - 反应条件分析图表
   - 置信度评估

3. **导出结果**
   - 下载预测报告
   - 保存参数配置

### 🔧 开发模式

```bash
# 启用开发模式（文件变更自动重载）
python run_app.py --dev
```

开发模式特性：
- 📝 代码修改自动重载
- 🔍 详细错误信息
- 🚀 快速开发迭代

### 🧪 模型训练与测试

```bash
# 训练新模型
python train.py

# 测试模型性能
python predict.py

# 测试Web应用
python test_app.py
```

## 🏗️ 技术架构

### 🤖 AI模型架构
- **类型**: Transformer编码器-解码器
- **输入**: 反应物SMILES + 反应条件 (pH + 消毒剂类型)
- **输出**: 产物SMILES序列
- **特殊处理**: 条件向量融合，位置编码优化

### 🌐 Web应用架构
- **框架**: Streamlit (本地优化)
- **端口管理**: 自动检测可用端口
- **浏览器集成**: 自动打开浏览器
- **热重载**: 开发模式支持

### 📊 核心技术栈
- **🧠 AI框架**: PyTorch 2.0+
- **🌐 Web框架**: Streamlit 1.28+  
- **📊 数据处理**: NumPy, Pandas
- **📈 可视化**: Plotly
- **🔧 环境**: Python 3.8+, Conda推荐

## 🛠️ 高级功能

### 📊 性能监控
- **内存使用**: ~2-4GB (取决于模型大小)
- **预测速度**: < 3秒
- **并发支持**: 单用户本地模式

### 🎯 自定义配置
- **模型参数**: 修改 `model.py` 中的架构参数
- **训练配置**: 调整 `train.py` 中的超参数
- **界面设置**: 自定义 `app.py` 中的UI组件

### 🧪 批量预测
```python
from predict import ReactionPredictor

# 加载预测器
predictor = ReactionPredictor("transformer_model.pth", "vocabulary.json")

# 批量预测
inputs = [
    ("CCO", 7.0, "chlorine"),
    ("c1ccccc1", 6.5, "ozone")
]
results = predictor.predict_batch(inputs)
```

## 🛠️ 故障排除

### 常见问题

**Q: 端口8501被占用**
```bash
# 脚本会自动选择其他可用端口
# 或手动指定端口
streamlit run app.py --server.port=8502
```

**Q: 模型加载失败**
```bash
# 重新训练模型
python train.py

# 检查文件完整性
python test_app.py
```

**Q: 依赖安装失败**
```bash
# 更新pip和setuptools
pip install --upgrade pip setuptools

# 重新安装依赖
pip install -r requirements.txt
```

**Q: 内存不足**
- 关闭其他应用程序
- 减少模型批处理大小
- 使用CPU模式而非GPU

## 🎯 开发与贡献

### 🔧 开发环境搭建
```bash
# 1. 克隆项目
git clone https://github.com/Halsey-ux/dbps_prediction_test_r1.git
cd dbps_prediction_test_r1

# 2. 安装开发环境
python setup_local.py

# 3. 启动开发模式
python run_app.py --dev
```

### 🧪 测试
```bash
# 运行所有测试
python test_app.py

# 测试模型推理
python predict.py

# 验证模型导入
python -c "from model import ReactionTransformer; print('✅ 模型导入成功')"
```

### 📝 贡献指南
1. Fork项目
2. 创建功能分支: `git checkout -b feature/new-feature`
3. 提交更改: `git commit -am 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 创建Pull Request

## 📚 更多信息

### 🔗 相关链接
- **PyTorch**: https://pytorch.org/
- **Streamlit**: https://streamlit.io/
- **RDKit**: https://www.rdkit.org/
- **化学信息学**: https://en.wikipedia.org/wiki/Cheminformatics

### 📖 学术参考
- Transformer架构: "Attention Is All You Need"
- SMILES表示法: Simplified molecular-input line-entry system
- 消毒副产物: Disinfection byproduct formation

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 致谢

- PyTorch团队提供的深度学习框架
- Streamlit团队提供的Web应用框架
- RDKit团队提供的化学计算工具
- 开源社区的贡献和支持

## 📞 联系方式

- **GitHub**: [Halsey-ux](https://github.com/Halsey-ux)
- **项目地址**: https://github.com/Halsey-ux/dbps_prediction_test_r1
- **问题反馈**: [创建Issue](https://github.com/Halsey-ux/dbps_prediction_test_r1/issues)

---

<div align="center">

**🧪 本地AI助力化学研究，预测更安全的未来 🌍**

[快速开始](#🚀-快速开始) • [使用指南](#💻-使用指南) • [技术架构](#🏗️-技术架构) • [开发贡献](#🎯-开发与贡献)

</div> 