"""
训练脚本 - ReactionTransformer 模型训练
包含数据加载、词汇表构建、模型训练和权重保存功能
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import json
import os
from tqdm import tqdm
from functools import partial
from typing import Optional

# 导入自定义模块
from utils import SMILESVocabulary, collate_fn, save_vocab, create_causal_mask
from model import ReactionTransformer


class ReactionDataset(Dataset):
    """反应数据集类"""
    
    def __init__(self, data_path: str):
        """
        初始化数据集
        Args:
            data_path: 数据文件路径
        """
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        print(f"加载了 {len(self.data)} 条反应数据")
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]


def train_model(
    data_path: str = "data/sample_data.json",
    model_save_path: str = "transformer_model.pth",
    vocab_save_path: str = "vocabulary.json",
    batch_size: int = 4,
    num_epochs: int = 100,
    learning_rate: float = 0.0001,
    device: Optional[str] = None
):
    """
    训练ReactionTransformer模型
    Args:
        data_path: 训练数据路径
        model_save_path: 模型保存路径
        vocab_save_path: 词汇表保存路径
        batch_size: 批量大小
        num_epochs: 训练轮数
        learning_rate: 学习率
        device: 计算设备
    """
    
    # 设置设备
    if device is None:
        device_obj = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    else:
        device_obj = torch.device(device)
    print(f"使用设备: {device_obj}")
    
    # 1. 加载数据
    print("正在加载数据...")
    dataset = ReactionDataset(data_path)
    
    # 2. 构建词汇表
    print("正在构建词汇表...")
    vocab = SMILESVocabulary()
    vocab.build_vocab_from_data(dataset.data)
    
    # 保存词汇表
    save_vocab(vocab, vocab_save_path)
    
    # 3. 创建数据加载器
    collate_fn_with_vocab = partial(collate_fn, vocab=vocab)
    dataloader = DataLoader(
        dataset, 
        batch_size=batch_size, 
        shuffle=True, 
        collate_fn=collate_fn_with_vocab
    )
    
    # 4. 创建模型
    print("正在创建模型...")
    model = ReactionTransformer(
        vocab_size=vocab.vocab_size,
        d_model=256,
        nhead=8,
        num_encoder_layers=4,  # 减少层数适应小数据集
        num_decoder_layers=4,
        dim_feedforward=1024,
        dropout=0.1,
        condition_dim=4,
        max_len=200
    )
    
    model = model.to(device_obj)
    print(f"模型参数数量: {sum(p.numel() for p in model.parameters()):,}")
    
    # 5. 设置优化器和损失函数
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss(ignore_index=vocab.get_pad_idx())
    
    # 学习率调度器
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.5)
    
    # 6. 训练循环
    print("开始训练...")
    model.train()
    
    for epoch in range(num_epochs):
        total_loss = 0.0
        num_batches = 0
        
        # 使用进度条
        pbar = tqdm(dataloader, desc=f"Epoch {epoch+1}/{num_epochs}")
        
        for batch in pbar:
            # 移动数据到设备
            src = batch['src'].to(device_obj)
            tgt_input = batch['tgt_input'].to(device_obj)
            tgt_output = batch['tgt_output'].to(device_obj)
            conditions = batch['conditions'].to(device_obj)
            src_padding_mask = batch['src_padding_mask'].to(device_obj)
            tgt_padding_mask = batch['tgt_padding_mask'].to(device_obj)
            
            # 创建因果掩码（防止解码器看到未来信息）
            tgt_len = tgt_input.size(1)
            tgt_mask = create_causal_mask(tgt_len).to(device_obj)
            
            # 前向传播
            optimizer.zero_grad()
            
            output = model(
                src=src,
                tgt=tgt_input,
                conditions=conditions,
                tgt_mask=tgt_mask,
                src_key_padding_mask=src_padding_mask,
                tgt_key_padding_mask=tgt_padding_mask
            )
            
            # 计算损失
            output_flat = output.view(-1, vocab.vocab_size)
            target_flat = tgt_output.view(-1)
            loss = criterion(output_flat, target_flat)
            
            # 反向传播
            loss.backward()
            
            # 梯度裁剪（防止梯度爆炸）
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            optimizer.step()
            
            # 记录损失
            total_loss += loss.item()
            num_batches += 1
            
            # 更新进度条
            pbar.set_postfix({'loss': f'{loss.item():.4f}'})
        
        # 计算平均损失
        avg_loss = total_loss / num_batches
        
        # 更新学习率
        scheduler.step()
        current_lr = scheduler.get_last_lr()[0]
        
        # 每10个epoch打印一次详细信息
        if (epoch + 1) % 10 == 0:
            print(f"\nEpoch {epoch+1}/{num_epochs}")
            print(f"平均损失: {avg_loss:.4f}")
            print(f"当前学习率: {current_lr:.6f}")
            print("-" * 50)
    
    # 7. 保存模型
    print("正在保存模型...")
    
    # 保存完整模型状态
    model_state = {
        'model_state_dict': model.state_dict(),
        'vocab_size': vocab.vocab_size,
        'model_config': {
            'd_model': 256,
            'nhead': 8,
            'num_encoder_layers': 4,
            'num_decoder_layers': 4,
            'dim_feedforward': 1024,
            'dropout': 0.1,
            'condition_dim': 4,
            'max_len': 200
        },
        'epoch': num_epochs,
        'loss': avg_loss
    }
    
    torch.save(model_state, model_save_path)
    print(f"模型已保存到: {model_save_path}")
    
    print("训练完成！")
    return model, vocab


def main():
    """主函数"""
    print("=" * 60)
    print("ReactionTransformer 消毒副产物路径预测模型训练")
    print("=" * 60)
    
    # 检查数据文件是否存在
    data_path = "data/sample_data.json"
    if not os.path.exists(data_path):
        print(f"错误: 数据文件 {data_path} 不存在!")
        print("请确保已正确放置示例数据文件。")
        return
    
    # 开始训练
    try:
        model, vocab = train_model(
            data_path=data_path,
            model_save_path="transformer_model.pth",
            vocab_save_path="vocabulary.json",
            batch_size=2,  # 小批量适应小数据集
            num_epochs=50,  # 减少训练轮数
            learning_rate=0.0005,  # 调整学习率
            device=None  # 自动选择设备
        )
        
        print("\n" + "=" * 60)
        print("训练成功完成！")
        print("生成的文件:")
        print("- transformer_model.pth: 训练好的模型权重")
        print("- vocabulary.json: 词汇表文件")
        print("\n现在可以运行 predict.py 进行推理测试")
        print("=" * 60)
        
    except Exception as e:
        print(f"训练过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 