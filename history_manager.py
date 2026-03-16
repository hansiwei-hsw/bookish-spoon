import os
from datetime import datetime
from typing import List, Optional


class HistoryManager:
    """历史记录模块：保存/读取/清空运算记录，支持导出txt"""

    def __init__(self, history_file: str = "calculator_history.txt", max_records: int = 100):
        """初始化历史记录管理器
        
        Args:
            history_file: 历史记录保存文件名
            max_records: 最大保存记录数
        """
        self.history_file = history_file
        self.max_records = max_records
        self._history: List[str] = []
        self._load_history()

    def _load_history(self):
        """从文件加载历史记录"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content:
                        records = content.strip().split('\n---\n')
                        self._history = [r.strip() for r in records if r.strip()]
            except (IOError, PermissionError):
                self._history = []

    def _save_history(self):
        """保存历史记录到文件"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                f.write('\n---\n'.join(self._history))
        except (IOError, PermissionError):
            pass

    def add_record(self, expression: str, result: float):
        """添加一条运算记录
        
        Args:
            expression: 运算表达式
            result: 运算结果
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = f"[{timestamp}]\n{expression} = {result}"
        
        if self._history and record in self._history[-1]:
            return
        
        self._history.append(record)
        
        if len(self._history) > self.max_records:
            self._history = self._history[-self.max_records:]
        
        self._save_history()

    def get_history(self, limit: int = None) -> List[str]:
        """获取历史记录
        
        Args:
            limit: 返回记录数量限制，None返回全部
            
        Returns:
            历史记录列表（按时间倒序）
        """
        reversed_history = list(reversed(self._history))
        if limit is not None:
            return reversed_history[:limit]
        return reversed_history

    def clear_history(self) -> bool:
        """清空所有历史记录
        
        Returns:
            True表示成功，False表示失败
        """
        self._history = []
        try:
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
            return True
        except (IOError, PermissionError):
            return False

    def export_history(self, export_file: str = None) -> bool:
        """导出历史记录到文件
        
        Args:
            export_file: 导出文件名，None使用默认值
            
        Returns:
            True表示成功，False表示失败
        """
        if export_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_file = f"calculator_history_export_{timestamp}.txt"
        
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write("科学计算器历史记录\n")
                f.write("=" * 50 + "\n\n")
                for record in reversed(self._history):
                    f.write(record + "\n\n")
            return True
        except (IOError, PermissionError):
            return False

    def get_last_record(self) -> Optional[str]:
        """获取最后一条记录
        
        Returns:
            最后一条记录字符串，无记录返回None
        """
        if self._history:
            return self._history[-1]
        return None

    def search_history(self, keyword: str) -> List[str]:
        """搜索历史记录
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的历史记录列表
        """
        keyword_lower = keyword.lower()
        return [r for r in self._history if keyword_lower in r.lower()]
