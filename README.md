# 🧪 消毒副产物预测系统

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.7.1-red.svg)](https://pytorch.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.46.1-green.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

基于深度学习Transformer架构的化学反应路径预测系统，专门用于预测消毒副产物的形成。

## 🌟 项目特点

- 🤖 **深度学习架构**: 基于Transformer编码器-解码器模型
- 🧬 **化学专业**: 专门针对消毒反应和副产物预测
- 🌐 **Web界面**: 现代化的Streamlit Web应用
- ⚡ **快速预测**: 秒级响应时间
- 🔧 **易于部署**: 支持本地和云端部署

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/Halsey-ux/dbps_prediction_test_r1.git
cd dbps_prediction_test_r1

# 创建conda环境
conda create -n test_r1_env python=3.9 -y
conda activate test_r1_env

# 安装依赖
pip install -r requirements.txt
```

### 2. 训练模型

```bash
# 训练ReactionTransformer模型
python train.py
```

### 3. 启动Web应用

#### 方法一：自动启动（推荐）
```bash
python run_app.py
```

#### 方法二：直接启动
```bash
streamlit run app.py
```

### 4. 访问应用
打开浏览器访问: http://localhost:8501

## 📁 项目结构

```
dbps_prediction_test_r1/
├── 🧬 核心模型
│   ├── model.py              # ReactionTransformer模型定义
│   ├── train.py              # 模型训练脚本
│   ├── predict.py            # 模型预测脚本
│   └── utils.py              # 工具函数
├── 🌐 Web应用
│   ├── app.py                # Streamlit Web应用
│   ├── run_app.py            # 自动启动脚本
│   └── .streamlit/           # Streamlit配置
├── 📊 数据
│   └── data/
│       └── sample_data.json  # 示例训练数据
├── 📖 文档
│   ├── README.md             # 项目说明
│   ├── DEPLOYMENT.md         # 详细部署指南
│   └── requirements.txt      # 依赖列表
├── ⚙️ 配置
│   ├── .vscode/              # VS Code配置
│   ├── pyrightconfig.json    # Python类型检查
│   └── .gitignore           # Git忽略文件
└── 🧪 测试
    └── test_app.py           # Web应用测试脚本
```

## 💻 使用指南

### 输入参数

1. **反应物SMILES**: 分子的SMILES表示法
   - 示例: `CCO` (乙醇), `c1ccc(cc1)O` (苯酚)

2. **pH值**: 反应溶液的酸碱度 (5.0-9.0)
   - 影响反应路径和产物分布

3. **消毒剂类型**: 选择消毒剂
   - `chlorine`: 氯气 (Cl₂) - 强氧化性，快速反应
   - `chloramine`: 氯胺 (NH₂Cl) - 中等氧化性，持续性强
   - `ozone`: 臭氧 (O₃) - 最强氧化性，无残留

### 输出结果

- **预测产物**: 生成的副产物SMILES
- **反应条件分析**: 消毒剂特性雷达图
- **结果导出**: 可下载预测报告

## 🏗️ 技术架构

### 模型架构
- **类型**: Transformer编码器-解码器
- **输入**: 反应物SMILES + 反应条件 (pH + 消毒剂类型)
- **输出**: 产物SMILES序列
- **特殊处理**: 条件向量融合，位置编码优化

### Web应用
- **框架**: Streamlit
- **可视化**: Plotly交互图表
- **响应式设计**: 支持桌面和移动端
- **实时预测**: 异步处理，加载动画

## 🌐 部署选项

### 本地部署
```bash
# 开发环境
streamlit run app.py

# 生产环境  
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

### 云端部署

#### Streamlit Cloud
1. 将代码推送到GitHub
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 连接GitHub仓库并部署

#### Docker部署
```bash
# 构建镜像
docker build -t dbps-prediction .

# 运行容器
docker run -p 8501:8501 dbps-prediction
```

详细部署指南请参考: [DEPLOYMENT.md](DEPLOYMENT.md)

## 🔧 开发与贡献

### 环境测试
```bash
# 运行应用测试
python test_app.py

# 验证模型导入
python -c "from model import ReactionTransformer; print('✅ 模型导入成功')"
```

### 代码贡献
1. Fork项目
2. 创建功能分支: `git checkout -b feature/new-feature`
3. 提交更改: `git commit -am 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 创建Pull Request

## 📊 性能指标

- **预测速度**: < 5秒
- **内存使用**: ~4GB (CPU模式)
- **模型大小**: ~50MB
- **并发支持**: 多用户同时访问

## 🛠️ 故障排除

### 常见问题

**Q: 模型文件不存在**
```bash
# 解决方案: 训练模型
python train.py
```

**Q: 依赖安装失败**
```bash
# 解决方案: 重新安装
pip install --upgrade -r requirements.txt
```

**Q: 端口被占用**
```bash
# 解决方案: 使用其他端口
streamlit run app.py --server.port=8502
```

更多问题请查看: [DEPLOYMENT.md](DEPLOYMENT.md#故障排除)

## 📚 技术文档

### 核心依赖
- **PyTorch**: 深度学习框架
- **Streamlit**: Web应用框架
- **RDKit**: 化学分子处理
- **Plotly**: 交互式可视化
- **Pandas/NumPy**: 数据处理

### API文档
- `ReactionTransformer`: 主模型类
- `ReactionPredictor`: 预测接口
- `SMILESVocabulary`: 词汇表管理

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 致谢

- PyTorch团队提供的深度学习框架
- Streamlit团队提供的Web应用框架
- RDKit团队提供的化学计算工具

## 📞 联系方式

- **GitHub**: [Halsey-ux](https://github.com/Halsey-ux)
- **项目地址**: https://github.com/Halsey-ux/dbps_prediction_test_r1
- **问题反馈**: [创建Issue](https://github.com/Halsey-ux/dbps_prediction_test_r1/issues)

---

<div align="center">

**🧪 让AI助力化学研究，预测更安全的未来 🌍**

[开始使用](#🚀-快速开始) • [查看演示](#💻-使用指南) • [部署指南](DEPLOYMENT.md) • [贡献代码](#🔧-开发与贡献)

</div> 