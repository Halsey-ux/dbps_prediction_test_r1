# 消毒副产物预测系统

<div align="center">
  <h3>🧪 基于深度学习的化学反应预测平台</h3>
  <p>专为水处理中的消毒副产物预测而设计</p>
  
  ![PyTorch](https://img.shields.io/badge/PyTorch-2.5.1-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
  ![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![Streamlit](https://img.shields.io/badge/Streamlit-1.46.1-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
  ![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)
  
  [🌐 在线演示](https://yourusername.github.io/disinfection-byproduct-prediction/) | [📚 文档](docs/) | [🚀 快速开始](#快速开始)
</div>

## 📋 项目简介

消毒副产物预测系统是基于Transformer深度学习架构开发的化学反应路径预测平台。该系统专门用于预测水处理过程中不同消毒剂（氯气、氯胺、臭氧）与有机物反应产生的副产物，为水处理行业提供科学决策支持。

### ✨ 核心特性

- 🧠 **深度学习引擎**: 基于Transformer架构，包含7,484,046个参数
- 🧪 **多元素支持**: 支持氯气、氯胺、臭氧等多种消毒剂类型
- 📊 **可视化分析**: 提供交互式图表和结果展示
- 🌐 **Web应用**: 用户友好的Streamlit界面
- ⚡ **高效预测**: 2-5秒内完成单次预测
- 🔧 **本地部署**: 支持本地环境运行

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Conda (推荐)
- 2GB+ RAM
- 1GB+ 存储空间

### 方法一：Conda环境（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/disinfection-byproduct-prediction.git
cd disinfection-byproduct-prediction

# 2. 创建conda环境
conda env create -f environment.yml
conda activate test_r1_env

# 3. 启动应用
python run_app.py
```

### 方法二：pip安装

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/disinfection-byproduct-prediction.git
cd disinfection-byproduct-prediction

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动应用
streamlit run app.py
```

### 访问应用

打开浏览器访问 [http://localhost:8501](http://localhost:8501)

## 📊 系统架构

```
消毒副产物预测系统
├── 前端界面 (Streamlit)
│   ├── 输入参数设置
│   ├── 可视化展示
│   └── 结果导出
├── 预测引擎 (PyTorch)
│   ├── Transformer模型
│   ├── SMILES编码器
│   └── 反应条件编码
├── 数据处理
│   ├── 词汇表管理
│   ├── 数据预处理
│   └── 结果后处理
└── 模型训练
    ├── 数据加载
    ├── 模型训练
    └── 评估验证
```

## 🛠️ 技术栈

### 核心框架
- **PyTorch 2.5.1** - 深度学习框架
- **Streamlit 1.46.1** - Web应用框架
- **Plotly** - 数据可视化

### 数据处理
- **Pandas** - 数据处理
- **NumPy** - 数值计算
- **scikit-learn** - 机器学习工具

### 模型架构
- **Transformer** - 序列到序列模型
- **SMILES编码** - 化学分子表示
- **条件编码** - 反应条件向量化

## 📚 使用指南

### 1. 基本预测

```python
from predict import ReactionPredictor

# 初始化预测器
predictor = ReactionPredictor(
    model_path="transformer_model.pth",
    vocab_path="vocabulary.json"
)

# 进行预测
result = predictor.predict_product(
    reactant_smiles="CCO",      # 乙醇
    pH=7.0,                     # 中性pH
    disinfectant="chlorine"     # 氯气消毒
)

print(f"预测产物: {result}")
```

### 2. 批量预测

```python
# 批量预测
inputs = [
    ("CCO", 7.0, "chlorine"),
    ("c1ccc(cc1)O", 6.5, "chlorine"),
    ("CC(C)O", 7.5, "chloramine")
]

results = predictor.predict_batch(inputs)
```

### 3. Web界面使用

1. 启动应用：`python run_app.py`
2. 在浏览器中打开：`http://localhost:8501`
3. 输入反应物SMILES字符串
4. 设置pH值（5.0-9.0）
5. 选择消毒剂类型
6. 点击预测按钮获取结果

## 📁 项目结构

```
disinfection-byproduct-prediction/
├── app.py                    # Streamlit Web应用
├── model.py                  # Transformer模型定义
├── predict.py                # 预测引擎
├── train.py                  # 模型训练脚本
├── utils.py                  # 工具函数
├── run_app.py                # 应用启动脚本
├── test_app.py               # 测试脚本
├── requirements.txt          # pip依赖
├── environment.yml           # conda环境配置
├── data/                     # 数据文件夹
│   └── sample_data.json      # 示例数据
├── docs/                     # 文档和静态页面
│   ├── index.html            # GitHub Pages首页
│   └── DEPLOY.md             # 部署说明
├── transformer_model.pth     # 预训练模型
├── vocabulary.json           # 词汇表
└── README.md                 # 项目说明
```

## 🔧 模型训练

如果您需要重新训练模型：

```bash
# 1. 准备训练数据
# 确保 data/sample_data.json 包含训练数据

# 2. 开始训练
python train.py

# 3. 查看训练结果
# 训练完成后会生成 transformer_model.pth 和 vocabulary.json
```

## 🧪 测试

```bash
# 运行基本测试
python test_app.py

# 测试预测功能
python predict.py
```

## 📈 模型性能

- **参数数量**: 7,484,046
- **词汇表大小**: 14个化学字符
- **支持的消毒剂**: 氯气、氯胺、臭氧
- **pH范围**: 5.0-9.0
- **预测速度**: 2-5秒/样本（CPU）

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详细信息请参阅 [LICENSE](LICENSE) 文件。

## 🔗 相关链接

- [GitHub Pages演示](https://yourusername.github.io/disinfection-byproduct-prediction/)
- [部署文档](docs/DEPLOY.md)
- [问题反馈](https://github.com/yourusername/disinfection-byproduct-prediction/issues)

## 📧 联系方式

- 项目维护者: [Your Name](mailto:your.email@example.com)
- 项目主页: [https://github.com/yourusername/disinfection-byproduct-prediction](https://github.com/yourusername/disinfection-byproduct-prediction)

---

<div align="center">
  <p>🌟 如果这个项目对您有帮助，请给我们一个星标！</p>
  <p>Made with ❤️ by the Water Treatment AI Team</p>
</div> 