"""
工具函数模块
包含SMILES序列处理、词汇表构建、掩码生成等功能
"""
import torch
import torch.nn as nn
from typing import List, Dict, Tuple, Optional
import json


class SMILESVocabulary:
    """SMILES词汇表类，用于管理字符级词汇表"""
    
    def __init__(self):
        # 特殊词汇
        self.special_tokens = ['<pad>', '<sos>', '<eos>', '<unk>']
        self.pad_token = '<pad>'
        self.sos_token = '<sos>'
        self.eos_token = '<eos>'
        self.unk_token = '<unk>'
        
        # 词汇表字典
        self.char_to_idx = {}
        self.idx_to_char = {}
        self.vocab_size = 0
        
    def build_vocab_from_data(self, data: List[Dict]) -> None:
        """
        从数据集中构建词汇表
        Args:
            data: 包含SMILES字符串的数据列表
        """
        # 收集所有唯一字符
        all_chars = set()
        
        # 从反应物和产物SMILES中提取字符
        for item in data:
            reactant_smiles = item['reactant_smiles']
            product_smiles = item['product_smiles']
            
            # 添加字符到集合中
            all_chars.update(reactant_smiles)
            all_chars.update(product_smiles)
        
        # 构建词汇表（特殊词汇优先）
        vocab_chars = self.special_tokens + sorted(list(all_chars))
        
        # 建立字符到索引的映射
        self.char_to_idx = {char: idx for idx, char in enumerate(vocab_chars)}
        self.idx_to_char = {idx: char for char, idx in self.char_to_idx.items()}
        self.vocab_size = len(vocab_chars)
        
        print(f"词汇表大小: {self.vocab_size}")
        print(f"包含字符: {sorted(list(all_chars))}")
    
    def encode_smiles(self, smiles: str, add_special_tokens: bool = True) -> List[int]:
        """
        将SMILES字符串编码为索引序列
        Args:
            smiles: SMILES字符串
            add_special_tokens: 是否添加特殊标记
        Returns:
            编码后的索引列表
        """
        tokens = []
        
        if add_special_tokens:
            tokens.append(self.char_to_idx[self.sos_token])
        
        # 逐字符编码
        for char in smiles:
            if char in self.char_to_idx:
                tokens.append(self.char_to_idx[char])
            else:
                tokens.append(self.char_to_idx[self.unk_token])
        
        if add_special_tokens:
            tokens.append(self.char_to_idx[self.eos_token])
            
        return tokens
    
    def decode_indices(self, indices: List[int], remove_special_tokens: bool = True) -> str:
        """
        将索引序列解码为SMILES字符串
        Args:
            indices: 索引列表
            remove_special_tokens: 是否移除特殊标记
        Returns:
            解码后的SMILES字符串
        """
        chars = []
        
        for idx in indices:
            if idx in self.idx_to_char:
                char = self.idx_to_char[idx]
                
                # 如果需要移除特殊标记
                if remove_special_tokens and char in self.special_tokens:
                    if char == self.eos_token:  # 遇到结束符就停止
                        break
                    continue
                        
                chars.append(char)
        
        return ''.join(chars)
    
    def get_pad_idx(self) -> int:
        """获取padding标记的索引"""
        return self.char_to_idx[self.pad_token]
    
    def get_sos_idx(self) -> int:
        """获取开始标记的索引"""
        return self.char_to_idx[self.sos_token]
    
    def get_eos_idx(self) -> int:
        """获取结束标记的索引"""
        return self.char_to_idx[self.eos_token]


def encode_conditions(pH: float, disinfectant: str) -> List[float]:
    """
    编码反应条件（pH和消毒剂类型）
    Args:
        pH: pH值
        disinfectant: 消毒剂类型
    Returns:
        编码后的条件向量
    """
    # pH标准化到0-1范围
    normalized_pH = (pH - 5.0) / 4.0  # 假设pH范围是5-9
    
    # 消毒剂类型独热编码
    disinfectant_map = {
        'chlorine': [1.0, 0.0, 0.0],
        'chloramine': [0.0, 1.0, 0.0], 
        'ozone': [0.0, 0.0, 1.0]
    }
    
    disinfectant_encoded = disinfectant_map.get(disinfectant, [0.0, 0.0, 0.0])
    
    # 组合条件向量
    conditions = [normalized_pH] + disinfectant_encoded
    
    return conditions


def create_padding_mask(seq: torch.Tensor, pad_idx: int) -> torch.Tensor:
    """
    创建padding掩码
    Args:
        seq: 输入序列 [batch_size, seq_len]
        pad_idx: padding标记的索引
    Returns:
        掩码张量，True表示需要被掩盖的位置
    """
    return (seq == pad_idx)


def create_causal_mask(size: int) -> torch.Tensor:
    """
    创建因果掩码（用于解码器）
    Args:
        size: 序列长度
    Returns:
        因果掩码张量
    """
    mask = torch.triu(torch.ones(size, size), diagonal=1)
    return mask.bool()


def collate_fn(batch: List[Dict], vocab: SMILESVocabulary) -> Dict[str, torch.Tensor]:
    """
    DataLoader的collate函数，用于批量处理数据
    Args:
        batch: 批量数据
        vocab: 词汇表对象
    Returns:
        处理后的批量数据字典
    """
    # 提取各部分数据
    reactant_smiles = [item['reactant_smiles'] for item in batch]
    product_smiles = [item['product_smiles'] for item in batch]
    conditions = [encode_conditions(item['pH'], item['disinfectant']) for item in batch]
    
    # 编码SMILES
    src_sequences = [vocab.encode_smiles(smiles, add_special_tokens=True) for smiles in reactant_smiles]
    tgt_sequences = [vocab.encode_smiles(smiles, add_special_tokens=True) for smiles in product_smiles]
    
    # 找到最大长度
    max_src_len = max(len(seq) for seq in src_sequences)
    max_tgt_len = max(len(seq) for seq in tgt_sequences)
    
    # 填充序列
    pad_idx = vocab.get_pad_idx()
    
    src_padded = []
    tgt_input_padded = []  # 用于输入（右移一位）
    tgt_output_padded = []  # 用于目标（原始序列）
    
    for src_seq, tgt_seq in zip(src_sequences, tgt_sequences):
        # 源序列填充
        src_padded.append(src_seq + [pad_idx] * (max_src_len - len(src_seq)))
        
        # 目标输入序列（去掉最后一个token）
        tgt_input = tgt_seq[:-1] + [pad_idx] * (max_tgt_len - len(tgt_seq))
        tgt_input_padded.append(tgt_input)
        
        # 目标输出序列（去掉第一个token）
        tgt_output = tgt_seq[1:] + [pad_idx] * (max_tgt_len - len(tgt_seq))
        tgt_output_padded.append(tgt_output)
    
    return {
        'src': torch.tensor(src_padded, dtype=torch.long),
        'tgt_input': torch.tensor(tgt_input_padded, dtype=torch.long),
        'tgt_output': torch.tensor(tgt_output_padded, dtype=torch.long),
        'conditions': torch.tensor(conditions, dtype=torch.float32),
        'src_padding_mask': create_padding_mask(torch.tensor(src_padded), pad_idx),
        'tgt_padding_mask': create_padding_mask(torch.tensor(tgt_input_padded), pad_idx)
    }


def save_vocab(vocab: SMILESVocabulary, filepath: str) -> None:
    """
    保存词汇表到文件
    Args:
        vocab: 词汇表对象
        filepath: 保存路径
    """
    vocab_data = {
        'char_to_idx': vocab.char_to_idx,
        'idx_to_char': vocab.idx_to_char,
        'vocab_size': vocab.vocab_size,
        'special_tokens': vocab.special_tokens
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(vocab_data, f, ensure_ascii=False, indent=2)
    
    print(f"词汇表已保存到: {filepath}")


def load_vocab(filepath: str) -> SMILESVocabulary:
    """
    从文件加载词汇表
    Args:
        filepath: 词汇表文件路径
    Returns:
        词汇表对象
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        vocab_data = json.load(f)
    
    vocab = SMILESVocabulary()
    vocab.char_to_idx = vocab_data['char_to_idx']
    vocab.idx_to_char = {int(k): v for k, v in vocab_data['idx_to_char'].items()}
    vocab.vocab_size = vocab_data['vocab_size']
    vocab.special_tokens = vocab_data['special_tokens']
    
    print(f"词汇表已从 {filepath} 加载完成")
    return vocab 