"""
ReactionTransformer 模型定义
基于Transformer的化学反应路径预测模型
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from typing import Optional, Tuple

class PositionalEncoding(nn.Module):
    """位置编码模块"""
    
    def __init__(self, d_model: int, max_len: int = 5000):
        """
        初始化位置编码
        Args:
            d_model: 模型维度
            max_len: 最大序列长度
        """
        super().__init__()
        
        # 创建位置编码矩阵
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        # 计算编码值
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                           (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        
        # 注册为buffer，不参与梯度更新
        self.register_buffer('pe', pe)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        前向传播
        Args:
            x: 输入张量 [seq_len, batch_size, d_model]
        Returns:
            添加位置编码后的张量
        """
        # 获取序列长度和批次大小
        seq_len, batch_size = x.size(0), x.size(1)
        # 提取对应长度的位置编码并扩展到匹配批次大小
        pe_tensor = torch.as_tensor(self.pe)  # 显式转换为tensor类型
        pe_slice = pe_tensor[:seq_len, :].expand(-1, batch_size, -1)
        return x + pe_slice


class ConditionEncoder(nn.Module):
    """反应条件编码器"""
    
    def __init__(self, condition_dim: int, d_model: int):
        """
        初始化条件编码器
        Args:
            condition_dim: 条件向量维度（pH + 消毒剂类型）
            d_model: 模型维度
        """
        super().__init__()
        
        # 多层感知机编码反应条件
        self.condition_mlp = nn.Sequential(
            nn.Linear(condition_dim, d_model // 2),
            nn.ReLU(),
            nn.Linear(d_model // 2, d_model),
            nn.ReLU(),
            nn.Linear(d_model, d_model)
        )
        
    def forward(self, conditions: torch.Tensor) -> torch.Tensor:
        """
        编码反应条件
        Args:
            conditions: 条件张量 [batch_size, condition_dim]
        Returns:
            编码后的条件向量 [batch_size, d_model]
        """
        return self.condition_mlp(conditions)


class ReactionTransformer(nn.Module):
    """反应路径预测Transformer模型"""
    
    def __init__(
        self,
        vocab_size: int,
        d_model: int = 256,
        nhead: int = 8,
        num_encoder_layers: int = 6,
        num_decoder_layers: int = 6,
        dim_feedforward: int = 1024,
        dropout: float = 0.1,
        condition_dim: int = 4,  # pH + 3个消毒剂类型
        max_len: int = 200
    ):
        """
        初始化ReactionTransformer模型
        Args:
            vocab_size: 词汇表大小
            d_model: 模型维度
            nhead: 多头注意力头数
            num_encoder_layers: 编码器层数
            num_decoder_layers: 解码器层数
            dim_feedforward: 前馈网络维度
            dropout: dropout率
            condition_dim: 条件向量维度
            max_len: 最大序列长度
        """
        super().__init__()
        
        self.d_model = d_model
        self.vocab_size = vocab_size
        
        # 词嵌入层
        self.src_embedding = nn.Embedding(vocab_size, d_model)
        self.tgt_embedding = nn.Embedding(vocab_size, d_model)
        
        # 位置编码
        self.pos_encoder = PositionalEncoding(d_model, max_len)
        
        # 条件编码器
        self.condition_encoder = ConditionEncoder(condition_dim, d_model)
        
        # Transformer主体
        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=num_encoder_layers,
            num_decoder_layers=num_decoder_layers,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=False  # 使用seq_len优先的格式
        )
        
        # 输出投影层
        self.output_projection = nn.Linear(d_model, vocab_size)
        
        # 初始化参数
        self._init_weights()
    
    def _init_weights(self):
        """初始化模型参数"""
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
    
    def forward(
        self,
        src: torch.Tensor,
        tgt: torch.Tensor,
        conditions: torch.Tensor,
        src_mask: Optional[torch.Tensor] = None,
        tgt_mask: Optional[torch.Tensor] = None,
        src_key_padding_mask: Optional[torch.Tensor] = None,
        tgt_key_padding_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        前向传播
        Args:
            src: 源序列 [batch_size, src_len]
            tgt: 目标序列 [batch_size, tgt_len]
            conditions: 反应条件 [batch_size, condition_dim]
            src_mask: 源序列掩码
            tgt_mask: 目标序列掩码
            src_key_padding_mask: 源序列padding掩码
            tgt_key_padding_mask: 目标序列padding掩码
        Returns:
            输出logits [batch_size, tgt_len, vocab_size]
        """
        # 转置为 [seq_len, batch_size] 格式
        src = src.transpose(0, 1)
        tgt = tgt.transpose(0, 1)
        
        # 词嵌入
        src_emb = self.src_embedding(src) * math.sqrt(self.d_model)
        tgt_emb = self.tgt_embedding(tgt) * math.sqrt(self.d_model)
        
        # 添加位置编码
        src_emb = self.pos_encoder(src_emb)
        tgt_emb = self.pos_encoder(tgt_emb)
        
        # 编码反应条件
        condition_emb = self.condition_encoder(conditions)  # [batch_size, d_model]
        condition_emb = condition_emb.unsqueeze(0)  # [1, batch_size, d_model]
        
        # 将条件向量加到源序列的第一个位置
        src_emb = torch.cat([condition_emb, src_emb], dim=0)
        
        # 调整掩码尺寸（为条件向量添加一个位置）
        if src_key_padding_mask is not None:
            # 为条件向量添加False（不掩盖）
            condition_padding = torch.zeros(src_key_padding_mask.size(0), 1, 
                                          dtype=torch.bool, device=src_key_padding_mask.device)
            src_key_padding_mask = torch.cat([condition_padding, src_key_padding_mask], dim=1)
        
        # Transformer前向传播
        output = self.transformer(
            src_emb, tgt_emb,
            src_mask=src_mask,
            tgt_mask=tgt_mask,
            src_key_padding_mask=src_key_padding_mask,
            tgt_key_padding_mask=tgt_key_padding_mask
        )
        
        # 输出投影
        output = self.output_projection(output)
        
        # 转回 [batch_size, seq_len, vocab_size] 格式
        output = output.transpose(0, 1)
        
        return output
    
    def encode(
        self,
        src: torch.Tensor,
        conditions: torch.Tensor,
        src_mask: Optional[torch.Tensor] = None,
        src_key_padding_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        编码器前向传播
        Args:
            src: 源序列 [batch_size, src_len]
            conditions: 反应条件 [batch_size, condition_dim]
            src_mask: 源序列掩码
            src_key_padding_mask: 源序列padding掩码
        Returns:
            编码器输出 [src_len+1, batch_size, d_model]
        """
        # 转置为 [seq_len, batch_size] 格式
        src = src.transpose(0, 1)
        
        # 词嵌入和位置编码
        src_emb = self.src_embedding(src) * math.sqrt(self.d_model)
        src_emb = self.pos_encoder(src_emb)
        
        # 编码反应条件
        condition_emb = self.condition_encoder(conditions)
        condition_emb = condition_emb.unsqueeze(0)
        
        # 组合源序列和条件
        src_emb = torch.cat([condition_emb, src_emb], dim=0)
        
        # 调整掩码
        if src_key_padding_mask is not None:
            condition_padding = torch.zeros(src_key_padding_mask.size(0), 1, 
                                          dtype=torch.bool, device=src_key_padding_mask.device)
            src_key_padding_mask = torch.cat([condition_padding, src_key_padding_mask], dim=1)
        
        # 编码
        memory = self.transformer.encoder(src_emb, mask=src_mask, src_key_padding_mask=src_key_padding_mask)
        
        return memory
    
    def decode(
        self,
        tgt: torch.Tensor,
        memory: torch.Tensor,
        tgt_mask: Optional[torch.Tensor] = None,
        tgt_key_padding_mask: Optional[torch.Tensor] = None,
        memory_key_padding_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        解码器前向传播
        Args:
            tgt: 目标序列 [batch_size, tgt_len]
            memory: 编码器输出 [src_len+1, batch_size, d_model]
            tgt_mask: 目标序列掩码
            tgt_key_padding_mask: 目标序列padding掩码
            memory_key_padding_mask: 编码器输出padding掩码
        Returns:
            解码器输出 [batch_size, tgt_len, vocab_size]
        """
        # 转置为 [seq_len, batch_size] 格式
        tgt = tgt.transpose(0, 1)
        
        # 词嵌入和位置编码
        tgt_emb = self.tgt_embedding(tgt) * math.sqrt(self.d_model)
        tgt_emb = self.pos_encoder(tgt_emb)
        
        # 解码
        output = self.transformer.decoder(
            tgt_emb, memory,
            tgt_mask=tgt_mask,
            tgt_key_padding_mask=tgt_key_padding_mask,
            memory_key_padding_mask=memory_key_padding_mask
        )
        
        # 输出投影
        output = self.output_projection(output)
        
        # 转回 [batch_size, seq_len, vocab_size] 格式
        output = output.transpose(0, 1)
        
        return output


def create_model(vocab_size: int, **kwargs) -> ReactionTransformer:
    """
    创建ReactionTransformer模型的便捷函数
    Args:
        vocab_size: 词汇表大小
        **kwargs: 其他模型参数
    Returns:
        ReactionTransformer模型实例
    """
    return ReactionTransformer(vocab_size=vocab_size, **kwargs) 