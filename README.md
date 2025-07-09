# ReactionTransformer 消毒副产物路径预测项目

一个基于Transformer架构的化学反应路径预测模型，专门用于预测消毒副产物（DBPs）的生成。本项目基于《TP-Transformer: An Interpretable Model for Predicting the Transformation Pathways of Organic Pollutants in Chemical Oxidation Processes》论文思想构建。

## 🎯 项目目标

- 使用**PyTorch**实现Transformer编码-解码模型
- 输入：`反应物SMILES + pH + 消毒剂类型`
- 输出：`产物SMILES`
- 提供完整的训练和预测流程
- 使用字符级SMILES编码，支持动态词汇表构建

## 📁 项目结构

```
.
├── data/
│   └── sample_data.json      # 示例训练数据（18条反应对）
├── model.py                  # ReactionTransformer 模型定义
├── train.py                  # 训练脚本
├── predict.py                # 推理脚本
├── utils.py                  # 工具函数（词汇表、掩码生成等）
├── requirements.txt          # Python依赖列表
└── README.md                 # 项目说明文档
```

## ⚙️ 模型架构

### ReactionTransformer 主要组件：

1. **词嵌入层**: 将SMILES字符转换为向量表示
2. **位置编码**: 为序列添加位置信息
3. **条件编码器**: 编码pH和消毒剂类型信息
4. **Transformer编码器**: 处理输入的反应物SMILES和条件信息
5. **Transformer解码器**: 自回归生成产物SMILES
6. **输出投影层**: 将隐藏状态映射到词汇表概率分布

### 特色功能：

- **条件注入**: 将pH和消毒剂信息融入编码器
- **字符级编码**: 支持任意SMILES结构，具有良好泛化性
- **因果掩码**: 确保解码器只能看到当前位置之前的信息
- **贪心解码**: 实现快速的序列生成

## 🚀 快速开始

### 1. 环境准备

确保已安装Python 3.8+，然后安装依赖：

```bash
# 安装依赖
pip install -r requirements.txt
```

### 2. 训练模型

```bash
# 训练模型（约2-5分钟，取决于硬件）
python train.py
```

训练完成后会生成：
- `transformer_model.pth`: 训练好的模型权重
- `vocabulary.json`: 字符级词汇表文件

### 3. 进行预测

```bash
# 运行预测脚本
python predict.py
```

预测脚本包含：
- **自动示例预测**: 在几个测试样本上展示模型效果
- **交互式预测**: 用户可以输入自定义的反应条件进行预测

### 4. 示例输入输出

```
反应物: CCO
pH: 7.0
消毒剂: chlorine
预测产物: CCOCl

反应物: c1ccc(cc1)O
pH: 6.5
消毒剂: chlorine
预测产物: c1cc(c(cc1)O)Cl
```

## 🧪 数据格式

训练数据采用JSON格式，每个反应记录包含：

```json
{
  "reactant_smiles": "CCO",
  "pH": 7.0,
  "disinfectant": "chlorine",
  "product_smiles": "CCOCl"
}
```

### 支持的消毒剂类型：
- `chlorine`: 氯气
- `chloramine`: 氯胺
- `ozone`: 臭氧

### pH范围：
- 建议范围：5.0 - 9.0
- 模型会自动标准化到 [0, 1] 区间

## 🔧 模型配置

可以在 `train.py` 中调整模型超参数：

```python
model = ReactionTransformer(
    vocab_size=vocab.vocab_size,
    d_model=256,              # 模型维度
    nhead=8,                  # 注意力头数
    num_encoder_layers=4,     # 编码器层数
    num_decoder_layers=4,     # 解码器层数
    dim_feedforward=1024,     # 前馈网络维度
    dropout=0.1,              # Dropout率
    condition_dim=4,          # 条件向量维度
    max_len=200              # 最大序列长度
)
```

## 📊 训练参数

当前配置针对小数据集优化：

- **批量大小**: 2（适应小数据集）
- **学习率**: 0.0005（使用Adam优化器）
- **训练轮数**: 50
- **学习率调度**: StepLR（每30个epoch衰减0.5倍）
- **梯度裁剪**: 最大范数1.0

## 🔄 扩展指南

### 1. 使用真实数据

替换 `data/sample_data.json` 为你的真实DBP数据：

```python
# 确保数据格式一致
data = [
    {
        "reactant_smiles": "实际反应物SMILES",
        "pH": 实际pH值,
        "disinfectant": "实际消毒剂类型",
        "product_smiles": "实际产物SMILES"
    },
    # ... 更多数据
]
```

### 2. 多步路径预测

当前模型预测单步反应，扩展为多步路径：

```python
def predict_pathway(predictor, initial_smiles, conditions, max_steps=3):
    """预测多步反应路径"""
    pathway = [initial_smiles]
    current_smiles = initial_smiles
    
    for step in range(max_steps):
        next_product = predictor.predict_product(
            current_smiles, conditions['pH'], conditions['disinfectant']
        )
        if next_product == current_smiles:  # 达到稳定状态
            break
        pathway.append(next_product)
        current_smiles = next_product
    
    return pathway
```

### 3. 添加新的条件因子

在 `utils.py` 中扩展条件编码：

```python
def encode_conditions(pH, disinfectant, temperature=None, concentration=None):
    """扩展条件编码，支持温度和浓度"""
    # 现有pH和消毒剂编码
    conditions = [normalized_pH] + disinfectant_encoded
    
    # 添加新条件
    if temperature is not None:
        normalized_temp = (temperature - 273.15) / 100  # 标准化温度
        conditions.append(normalized_temp)
    
    if concentration is not None:
        log_conc = math.log10(concentration + 1e-6)  # 对数变换
        conditions.append(log_conc)
    
    return conditions
```

### 4. 改进采样策略

在 `predict.py` 中实现更好的解码策略：

```python
def beam_search_decode(self, src, conditions, beam_size=5, max_length=100):
    """束搜索解码（比贪心搜索效果更好）"""
    # 实现束搜索算法
    pass

def nucleus_sampling(self, logits, p=0.9):
    """核采样（生成更多样的结果）"""
    # 实现nucleus sampling
    pass
```

## 🔍 模型评估

评估指标建议：

1. **SMILES有效性**: 生成的SMILES是否能被RDKit解析
2. **化学合理性**: 产物结构是否符合化学常识
3. **BLEU分数**: 与真实产物的序列相似度
4. **分子指纹相似性**: 使用Tanimoto系数比较分子结构

```python
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def evaluate_predictions(true_smiles, pred_smiles):
    """评估预测结果"""
    valid_count = 0
    total_count = len(pred_smiles)
    
    for pred in pred_smiles:
        try:
            mol = Chem.MolFromSmiles(pred)
            if mol is not None:
                valid_count += 1
        except:
            pass
    
    validity = valid_count / total_count
    return {'validity': validity}
```

## ⚠️ 注意事项

1. **数据质量**: 确保训练数据中的SMILES格式正确
2. **计算资源**: 模型参数约2.5M，训练需要少量GPU/CPU资源
3. **过拟合**: 当前示例数据较小，实际应用需要更大数据集
4. **化学验证**: 建议结合领域专家知识验证预测结果

## 📚 参考文献

1. TP-Transformer: An Interpretable Model for Predicting the Transformation Pathways of Organic Pollutants in Chemical Oxidation Processes
2. Attention Is All You Need (Transformer原始论文)
3. SMILES: a chemical language and information system

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目：

- 报告bug和问题
- 建议新功能
- 提供更好的数据集
- 改进模型架构

## 📄 许可证

本项目采用MIT许可证。详情请参阅LICENSE文件。

---

🧬 **Happy Chemical Modeling!** 🧬 