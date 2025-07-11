"""
推理脚本 - ReactionTransformer 消毒副产物预测
包含模型加载、贪心解码和产物SMILES预测功能
"""
import torch
import torch.nn.functional as F
import os
from typing import List, Tuple, Optional

# 导入自定义模块
from utils import SMILESVocabulary, load_vocab, encode_conditions, create_padding_mask
from model import ReactionTransformer


class ReactionPredictor:
    """反应产物预测器"""
    
    def __init__(self, model_path: str, vocab_path: str, device: Optional[str] = None):
        """
        初始化预测器
        Args:
            model_path: 模型权重文件路径
            vocab_path: 词汇表文件路径
            device: 计算设备
        """
        # 设置设备
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        
        print(f"使用设备: {self.device}")
        
        # 加载词汇表
        print("正在加载词汇表...")
        self.vocab = load_vocab(vocab_path)
        
        # 加载模型
        print("正在加载模型...")
        self._load_model(model_path)
        
        print("预测器初始化完成！")
    
    def _load_model(self, model_path: str):
        """
        加载训练好的模型
        Args:
            model_path: 模型文件路径
        """
        # 加载模型状态
        checkpoint = torch.load(model_path, map_location=self.device)
        
        # 获取模型配置
        model_config = checkpoint['model_config']
        vocab_size = checkpoint['vocab_size']
        
        # 创建模型实例
        self.model = ReactionTransformer(
            vocab_size=vocab_size,
            **model_config
        )
        
        # 加载权重
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.to(self.device)
        self.model.eval()
        
        print(f"模型加载完成，参数数量: {sum(p.numel() for p in self.model.parameters()):,}")
    
    def predict_product(
        self,
        reactant_smiles: str,
        pH: float,
        disinfectant: str,
        max_length: int = 100,
        temperature: float = 1.0
    ) -> str:
        """
        预测反应产物SMILES
        Args:
            reactant_smiles: 反应物SMILES字符串
            pH: 反应pH值
            disinfectant: 消毒剂类型 ('chlorine', 'chloramine', 'ozone')
            max_length: 最大生成长度
            temperature: 采样温度（越高越随机）
        Returns:
            预测的产物SMILES字符串
        """
        with torch.no_grad():
            # 1. 编码输入
            src_tokens = self.vocab.encode_smiles(reactant_smiles, add_special_tokens=True)
            src = torch.tensor([src_tokens], dtype=torch.long).to(self.device)
            
            # 编码反应条件
            conditions = encode_conditions(pH, disinfectant)
            conditions = torch.tensor([conditions], dtype=torch.float32).to(self.device)
            
            # 创建源序列padding掩码
            src_padding_mask = create_padding_mask(src, self.vocab.get_pad_idx()).to(self.device)
            
            # 2. 编码源序列
            memory = self.model.encode(
                src=src,
                conditions=conditions,
                src_key_padding_mask=src_padding_mask
            )
            
            # 创建用于解码的memory掩码（因为在encode中添加了条件向量，所以长度+1）
            memory_padding_mask = torch.zeros(src_padding_mask.size(0), src_padding_mask.size(1) + 1, 
                                            dtype=torch.bool, device=self.device)
            memory_padding_mask[:, 1:] = src_padding_mask  # 第一个位置（条件向量）不掩盖
            
            # 3. 贪心解码
            # 初始化目标序列（只包含SOS标记）
            tgt = torch.tensor([[self.vocab.get_sos_idx()]], dtype=torch.long).to(self.device)
            
            # 生成序列
            for _ in range(max_length):
                # 创建因果掩码
                tgt_len = tgt.size(1)
                tgt_mask = torch.triu(torch.ones(tgt_len, tgt_len), diagonal=1).bool().to(self.device)
                
                # 解码当前序列
                output = self.model.decode(
                    tgt=tgt,
                    memory=memory,
                    tgt_mask=tgt_mask,
                    memory_key_padding_mask=memory_padding_mask
                )
                
                # 获取下一个词的概率分布
                next_token_logits = output[0, -1, :] / temperature
                probs = F.softmax(next_token_logits, dim=-1)
                
                # 贪心选择（选择概率最高的词）
                next_token = torch.argmax(probs, dim=-1).unsqueeze(0).unsqueeze(0)
                
                # 检查是否生成了结束符
                if next_token.item() == self.vocab.get_eos_idx():
                    break
                
                # 将新token添加到序列中
                tgt = torch.cat([tgt, next_token], dim=1)
            
            # 4. 解码为SMILES字符串
            predicted_tokens = tgt[0].cpu().tolist()
            predicted_smiles = self.vocab.decode_indices(predicted_tokens, remove_special_tokens=True)
            
            return predicted_smiles
    
    def predict_batch(
        self,
        inputs: List[Tuple[str, float, str]],
        max_length: int = 100
    ) -> List[str]:
        """
        批量预测多个反应的产物
        Args:
            inputs: 输入列表，每个元素为 (reactant_smiles, pH, disinfectant)
            max_length: 最大生成长度
        Returns:
            预测结果列表
        """
        results = []
        
        for reactant_smiles, pH, disinfectant in inputs:
            predicted_smiles = self.predict_product(
                reactant_smiles, pH, disinfectant, max_length
            )
            results.append(predicted_smiles)
        
        return results
    
    def evaluate_on_examples(self):
        """在示例数据上评估模型性能"""
        # 一些测试例子
        test_examples = [
            ("CCO", 7.0, "chlorine"),
            ("c1ccc(cc1)O", 6.5, "chlorine"),
            ("CC(C)O", 7.5, "chloramine"),
            ("Nc1ccccc1", 6.0, "chlorine"),
            ("c1ccccc1", 7.0, "chlorine")
        ]
        
        print("\n" + "=" * 60)
        print("模型预测示例")
        print("=" * 60)
        
        for i, (reactant, pH, disinfectant) in enumerate(test_examples, 1):
            predicted = self.predict_product(reactant, pH, disinfectant)
            
            print(f"\n示例 {i}:")
            print(f"反应物: {reactant}")
            print(f"pH: {pH}")
            print(f"消毒剂: {disinfectant}")
            print(f"预测产物: {predicted}")
            print("-" * 40)


def main():
    """主函数"""
    print("=" * 60)
    print("ReactionTransformer 消毒副产物预测")
    print("=" * 60)
    
    # 检查必要文件是否存在
    model_path = "transformer_model.pth"
    vocab_path = "vocabulary.json"
    
    if not os.path.exists(model_path):
        print(f"错误: 模型文件 {model_path} 不存在!")
        print("请先运行 train.py 训练模型。")
        return
    
    if not os.path.exists(vocab_path):
        print(f"错误: 词汇表文件 {vocab_path} 不存在!")
        print("请先运行 train.py 生成词汇表。")
        return
    
    try:
        # 创建预测器
        predictor = ReactionPredictor(model_path, vocab_path)
        
        # 运行示例预测
        predictor.evaluate_on_examples()
        
        # 交互式预测
        print("\n" + "=" * 60)
        print("交互式预测（输入 'quit' 退出）")
        print("=" * 60)
        
        while True:
            print("\n请输入反应条件:")
            
            try:
                reactant = input("反应物SMILES: ").strip()
                if reactant.lower() == 'quit':
                    break
                
                pH_str = input("pH值: ").strip()
                if pH_str.lower() == 'quit':
                    break
                pH = float(pH_str)
                
                disinfectant = input("消毒剂类型 (chlorine/chloramine/ozone): ").strip()
                if disinfectant.lower() == 'quit':
                    break
                
                # 验证输入
                if disinfectant not in ['chlorine', 'chloramine', 'ozone']:
                    print("错误: 消毒剂类型必须是 chlorine、chloramine 或 ozone")
                    continue
                
                if pH < 5.0 or pH > 9.0:
                    print("警告: pH值超出正常范围 (5.0-9.0)")
                
                # 进行预测
                print("\n正在预测...")
                predicted = predictor.predict_product(reactant, pH, disinfectant)
                
                print(f"\n预测结果:")
                print(f"反应物: {reactant}")
                print(f"pH: {pH}")
                print(f"消毒剂: {disinfectant}")
                print(f"预测产物: {predicted}")
                
            except ValueError:
                print("错误: pH值必须是数字")
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"预测出错: {e}")
        
        print("\n感谢使用！")
        
    except Exception as e:
        print(f"加载模型时出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 