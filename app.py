"""
消毒副产物预测系统 - Web应用
基于ReactionTransformer的化学反应路径预测
"""

import streamlit as st
import torch
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import sys
from datetime import datetime
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入项目模块
try:
    from predict import ReactionPredictor
    from utils import SMILESVocabulary, load_vocab, encode_conditions
except ImportError as e:
    st.error(f"导入模块失败: {e}")
    st.stop()

# 页面配置
st.set_page_config(
    page_title="消毒副产物预测系统",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .prediction-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# 全局变量
@st.cache_resource
def load_model():
    """加载预训练模型"""
    model_path = "transformer_model.pth"
    vocab_path = "vocabulary.json"
    
    if not os.path.exists(model_path):
        return None, "模型文件不存在，请先训练模型"
    
    if not os.path.exists(vocab_path):
        return None, "词汇表文件不存在，请先训练模型"
    
    try:
        predictor = ReactionPredictor(model_path, vocab_path)
        return predictor, "模型加载成功"
    except Exception as e:
        return None, f"模型加载失败: {str(e)}"

# 主界面
def main():
    # 标题区域
    st.markdown("""
    <div class="main-header">
        <h1>🧪 消毒副产物预测系统</h1>
        <p>基于深度学习的化学反应路径预测平台</p>
        <p>Disinfection Byproduct Prediction System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 加载模型 (全局使用)
    predictor, status_msg = load_model()
    
    # 侧边栏
    with st.sidebar:
        st.markdown("## ⚙️ 模型设置")
        
        # 模型状态显示
        model_available = predictor is not None
        
        if predictor is None:
            st.error(status_msg)
            st.markdown("""
            ### 🚀 模型状态
            模型文件尚未加载。这通常发生在：
            - 首次部署时
            - 模型文件未正确上传
            
            ### 📋 系统功能
            - ✅ Web界面正常运行
            - ✅ 输入验证功能
            - ❌ 预测功能（需要模型文件）
            
            ### 🔧 解决方案
            1. 运行训练脚本生成模型文件
            2. 确保模型文件已正确上传
            3. 刷新页面重新加载
            """)
        else:
            st.success(status_msg)
        
        st.markdown("---")
        
        # 预测参数设置
        st.markdown("## 🎛️ 预测参数")
        
        temperature = st.slider(
            "生成温度",
            min_value=0.1,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="较低的温度产生更确定的预测，较高的温度增加随机性"
        )
        
        max_length = st.slider(
            "最大生成长度",
            min_value=50,
            max_value=200,
            value=100,
            step=10,
            help="生成序列的最大长度"
        )
        
        st.markdown("---")
        
        # 模型信息
        st.markdown("## 📊 模型信息")
        
        model_info = {
            "模型类型": "ReactionTransformer",
            "架构": "Transformer编码器-解码器",
            "输入": "反应物SMILES + 反应条件",
            "输出": "产物SMILES",
            "训练数据": "消毒反应数据集"
        }
        
        for key, value in model_info.items():
            st.markdown(f"**{key}:** {value}")
    
    # 主内容区域
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("## 📝 输入反应条件")
        
        # 示例选择（在表单外部）
        st.markdown("### 🧬 选择示例分子")
        examples = {
            "乙醇 (CCO)": "CCO",
            "苯酚 (c1ccc(cc1)O)": "c1ccc(cc1)O", 
            "异丙醇 (CC(C)O)": "CC(C)O",
            "苯胺 (Nc1ccccc1)": "Nc1ccccc1",
            "苯 (c1ccccc1)": "c1ccccc1",
            "自定义输入": ""
        }
        
        selected_example = st.selectbox(
            "选择示例分子或自定义输入",
            options=list(examples.keys()),
            index=0,
            help="选择预设的示例分子，或选择'自定义输入'来手动输入SMILES"
        )
        
        # 根据选择设置默认值
        default_smiles = examples[selected_example] if selected_example != "自定义输入" else "CCO"
        
        # 输入表单
        with st.form("prediction_form"):
            st.markdown("### 反应物信息")
            
            # SMILES输入
            reactant_smiles = st.text_input(
                "反应物SMILES",
                value=default_smiles,
                help="输入反应物的SMILES表示法，例如：CCO (乙醇)"
            )
            
            st.markdown("### 反应条件")
            
            # pH值设置
            pH = st.slider(
                "pH值",
                min_value=5.0,
                max_value=9.0,
                value=7.0,
                step=0.1,
                help="反应溶液的pH值，影响反应路径和产物分布"
            )
            
            # 消毒剂类型
            disinfectant = st.selectbox(
                "消毒剂类型",
                options=["chlorine", "chloramine", "ozone"],
                index=0,
                help="选择使用的消毒剂类型"
            )
            
            disinfectant_info = {
                "chlorine": "氯气 (Cl₂) - 强氧化性，快速反应",
                "chloramine": "氯胺 (NH₂Cl) - 中等氧化性，持续性强", 
                "ozone": "臭氧 (O₃) - 最强氧化性，无残留"
            }
            
            st.info(disinfectant_info[disinfectant])
            
            # 提交按钮
            submitted = st.form_submit_button(
                "🧪 开始预测",
                help="点击开始预测反应产物"
            )
    
    with col2:
        st.markdown("## 🎯 预测结果")
        
        if submitted:
            if not model_available:
                st.error("⚠️ 模型未加载，无法进行预测")
                st.info("请等待模型文件加载完成后重试")
                return
                
            if not reactant_smiles.strip():
                st.error("请输入有效的反应物SMILES!")
                return
            
            # 预测过程动画
            with st.spinner("🔬 模型正在分析反应条件..."):
                time.sleep(1)  # 模拟处理时间
                
                try:
                    # 执行预测 (此时模型必须可用)
                    assert predictor is not None, "模型未正确加载"
                    predicted_smiles = predictor.predict_product(
                        reactant_smiles=reactant_smiles,
                        pH=pH,
                        disinfectant=disinfectant,
                        max_length=max_length,
                        temperature=temperature
                    )
                    
                    # 显示结果
                    st.markdown("""
                    <div class="result-card">
                        <h3>✅ 预测完成!</h3>
                        <p>反应产物已成功预测</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 结果展示
                    st.markdown("### 📋 反应摘要")
                    
                    result_data = {
                        "参数": ["反应物", "产物", "pH值", "消毒剂", "预测时间"],
                        "值": [
                            reactant_smiles,
                            predicted_smiles,
                            f"{pH:.1f}",
                            disinfectant,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ]
                    }
                    
                    result_df = pd.DataFrame(result_data)
                    st.table(result_df)
                    
                    # 分子结构显示区域
                    st.markdown("### 🧬 分子结构")
                    
                    col_reactant, col_arrow, col_product = st.columns([2, 1, 2])
                    
                    with col_reactant:
                        st.markdown("""
                        <div class="prediction-card">
                            <h4>反应物</h4>
                            <p style="font-family: monospace; font-size: 18px; color: #2e7d32;">
                                {}
                            </p>
                        </div>
                        """.format(reactant_smiles), unsafe_allow_html=True)
                    
                    with col_arrow:
                        st.markdown("""
                        <div style="text-align: center; padding: 2rem 0;">
                            <h2>→</h2>
                            <p>{}条件下</p>
                            <p>pH {}</p>
                        </div>
                        """.format(disinfectant, pH), unsafe_allow_html=True)
                    
                    with col_product:
                        st.markdown("""
                        <div class="prediction-card">
                            <h4>预测产物</h4>
                            <p style="font-family: monospace; font-size: 18px; color: #c62828;">
                                {}
                            </p>
                        </div>
                        """.format(predicted_smiles), unsafe_allow_html=True)
                    
                    # 反应条件可视化
                    st.markdown("### 📈 反应条件分析")
                    
                    # 创建条件雷达图
                    categories = ['氧化性', '选择性', '反应速率', '副产物风险', '环境友好性']
                    
                    condition_values = {
                        'chlorine': [9, 6, 9, 7, 5],
                        'chloramine': [7, 8, 6, 5, 7], 
                        'ozone': [10, 7, 10, 8, 9]
                    }
                    
                    fig = go.Figure()
                    
                    values = condition_values[disinfectant] + [condition_values[disinfectant][0]]
                    categories_loop = categories + [categories[0]]
                    
                    fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories_loop,
                        fill='toself',
                        name=disinfectant.capitalize(),
                        line_color='rgb(102, 126, 234)'
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 10]
                            )),
                        showlegend=True,
                        title=f"{disinfectant.capitalize()}特性分析",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 下载结果
                    st.markdown("### 💾 导出结果")
                    
                    result_text = f"""消毒副产物预测结果
==================
反应物SMILES: {reactant_smiles}
产物SMILES: {predicted_smiles}
pH值: {pH}
消毒剂: {disinfectant}
预测时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
模型温度: {temperature}
最大长度: {max_length}
"""
                    
                    st.download_button(
                        label="📥 下载预测结果",
                        data=result_text,
                        file_name=f"prediction_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"预测过程中出现错误: {str(e)}")
                    st.exception(e)
        
        else:
            # 默认展示区域
            st.markdown("""
            <div class="prediction-card">
                <h4>🎯 等待预测</h4>
                <p>请在左侧输入反应条件，然后点击"开始预测"按钮</p>
                <br>
                <p><strong>系统特点:</strong></p>
                <ul>
                    <li>基于Transformer深度学习架构</li>
                    <li>支持多种消毒剂类型</li>
                    <li>考虑pH值对反应的影响</li>
                    <li>快速准确的产物预测</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # 页面底部信息
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🔬 模型架构</h4>
            <p>Transformer编码器-解码器</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>⚡ 响应速度</h4>
            <p>< 5秒预测时间</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>🎯 应用领域</h4>
            <p>水处理 · 环境化学</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 