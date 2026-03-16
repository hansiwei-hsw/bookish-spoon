"""
历史记录模块
负责保存/读取/清空运算记录，支持导出txt
"""
import os
from datetime import datetime
from typing import List, Dict, Optional
from config_handler import get_config


class HistoryRecord:
    """历史记录条目类"""
    
    def __init__(self, expression: str, result: str, timestamp: str = None):
        """
        初始化历史记录
        
        Args:
            expression: 表达式
            result: 结果
            timestamp: 时间戳
        """
        self.expression = expression
        self.result = result
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'expression': self.expression,
            'result': self.result,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HistoryRecord':
        """从字典创建"""
        return cls(
            expression=data.get('expression', ''),
            result=data.get('result', ''),
            timestamp=data.get('timestamp')
        )
    
    def __str__(self) -> str:
        return f"{self.timestamp} - {self.expression} = {self.result}"


class HistoryManager:
    """
    历史记录管理器类
    负责管理计算历史记录
    """
    
    HISTORY_FILE = 'calculator_history.txt'
    
    def __init__(self):
        """初始化历史记录管理器"""
        self._records: List[HistoryRecord] = []
        self._load_history()
    
    def _load_history(self) -> None:
        """从文件加载历史记录"""
        if not os.path.exists(self.HISTORY_FILE):
            return
        
        try:
            with open(self.HISTORY_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split(' - ', 1)
                    if len(parts) == 2:
                        timestamp = parts[0]
                        expr_result = parts[1]
                        
                        if ' = ' in expr_result:
                            expr_parts = expr_result.rsplit(' = ', 1)
                            expression = expr_parts[0]
                            result = expr_parts[1] if len(expr_parts) > 1 else ''
                        else:
                            expression = expr_result
                            result = ''
                        
                        record = HistoryRecord(expression, result, timestamp)
                        self._records.append(record)
        except (IOError, PermissionError):
            pass
    
    def _save_history(self) -> bool:
        """保存历史记录到文件"""
        try:
            with open(self.HISTORY_FILE, 'w', encoding='utf-8') as f:
                for record in self._records:
                    f.write(f"{record.timestamp} - {record.expression} = {record.result}\n")
            return True
        except (IOError, PermissionError):
            return False
    
    def add_record(self, expression: str, result: str) -> bool:
        """
        添加历史记录
        
        Args:
            expression: 表达式
            result: 结果
            
        Returns:
            是否添加成功
        """
        config = get_config()
        max_records = config.get('history_max_records', 100)
        
        if len(self._records) >= max_records:
            self._records.pop(0)
        
        record = HistoryRecord(expression, result)
        self._records.append(record)
        
        return self._save_history()
    
    def get_all_records(self) -> List[HistoryRecord]:
        """获取所有历史记录"""
        return self._records.copy()
    
    def get_recent_records(self, count: int = 10) -> List[HistoryRecord]:
        """
        获取最近的历史记录
        
        Args:
            count: 记录数量
            
        Returns:
            最近的记录列表
        """
        return self._records[-count:] if self._records else []
    
    def clear_history(self) -> bool:
        """清空历史记录"""
        self._records.clear()
        return self._save_history()
    
    def search_records(self, keyword: str) -> List[HistoryRecord]:
        """
        搜索历史记录
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的记录列表
        """
        keyword = keyword.lower()
        return [
            record for record in self._records
            if keyword in record.expression.lower() or keyword in record.result.lower()
        ]
    
    def export_to_file(self, filename: str) -> bool:
        """
        导出历史记录到指定文件
        
        Args:
            filename: 目标文件名
            
        Returns:
            是否导出成功
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write("计算器历史记录导出\n")
                f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"记录总数: {len(self._records)}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, record in enumerate(self._records, 1):
                    f.write(f"[{i}] {record}\n")
            
            return True
        except (IOError, PermissionError):
            return False
    
    def get_record_count(self) -> int:
        """获取记录总数"""
        return len(self._records)


_history_instance = None


def get_history() -> HistoryManager:
    """获取历史记录管理器单例"""
    global _history_instance
    if _history_instance is None:
        _history_instance = HistoryManager()
    return _history_instance
