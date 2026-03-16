import re
from typing import Tuple, Optional


class InputValidator:
    """输入校验模块：验证数字/运算符合法性，格式化输入"""

    def __init__(self):
        """初始化输入校验器"""
        self.allowed_operators = {'+', '-', '*', '/', '^', '√'}
        self.scientific_functions = {
            'sin', 'cos', 'tan', 'ln', 'log10',
            'sqrt', 'factorial', 'abs', 'exp', 'reciprocal'
        }

    def is_valid_number(self, value: str) -> bool:
        """检查字符串是否为有效数字（支持整数、小数、负数）
        
        Args:
            value: 待检查的字符串
            
        Returns:
            True表示有效数字，False表示无效
        """
        if not value or value.strip() == '':
            return False
        try:
            float(value)
            return True
        except ValueError:
            return False

    def is_valid_operator(self, op: str) -> bool:
        """检查是否为合法运算符
        
        Args:
            op: 运算符字符串
            
        Returns:
            True表示合法，False表示非法
        """
        return op in self.allowed_operators

    def is_valid_scientific_function(self, func_name: str) -> bool:
        """检查是否为合法科学函数名
        
        Args:
            func_name: 函数名
            
        Returns:
            True表示合法，False表示非法
        """
        return func_name.lower() in self.scientific_functions

    def validate_compatibility_input(self, expr: str) -> bool:
        """兼容模式输入校验（旧版本简单表达式如"3+5"）
        
        Args:
            expr: 输入表达式字符串
            
        Returns:
            True表示合法，False表示非法
        """
        expr = expr.strip()
        if not expr:
            return False
        
        pattern = r'^-?\d+(\.\d+)?[+\-*/]-?\d+(\.\d+)?$'
        return bool(re.match(pattern, expr))

    def parse_compatibility_input(self, expr: str) -> Optional[Tuple[float, str, float]]:
        """解析兼容模式输入表达式
        
        Args:
            expr: 输入表达式如"3+5"或"-2.5*3"
            
        Returns:
            元组(第一个数字, 运算符, 第二个数字)，解析失败返回None
        """
        expr = expr.strip()
        if not self.validate_compatibility_input(expr):
            return None
        
        operator_pos = -1
        operator = None
        
        for i, char in enumerate(expr[1:], 1):
            if char in '+-*/':
                operator_pos = i
                operator = char
                break
        
        if operator_pos == -1:
            return None
        
        num1_str = expr[:operator_pos]
        num2_str = expr[operator_pos + 1:]
        
        try:
            num1 = float(num1_str)
            num2 = float(num2_str)
            return (num1, operator, num2)
        except ValueError:
            return None

    def sanitize_input(self, input_str: str) -> str:
        """清理输入字符串（去除多余空格、标准化格式）
        
        Args:
            input_str: 原始输入字符串
            
        Returns:
            清理后的字符串
        """
        if not input_str:
            return ''
        
        cleaned = input_str.strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned

    def validate_menu_choice(self, choice: str, max_choice: int) -> bool:
        """验证菜单选择是否有效
        
        Args:
            choice: 用户输入的选择
            max_choice: 最大有效选择值
            
        Returns:
            True表示有效，False表示无效
        """
        if not choice or not choice.strip():
            return False
        try:
            choice_num = int(choice)
            return 0 <= choice_num <= max_choice
        except ValueError:
            return False

    def is_non_negative_integer(self, value: str) -> bool:
        """检查是否为非负整数字符串
        
        Args:
            value: 待检查的字符串
            
        Returns:
            True表示是非负整数，False表示不是
        """
        if not self.is_valid_number(value):
            return False
        num = float(value)
        return num >= 0 and num.is_integer()

    def is_positive_number(self, value: str) -> bool:
        """检查是否为正数字符串
        
        Args:
            value: 待检查的字符串
            
        Returns:
            True表示是正数，False表示不是
        """
        if not self.is_valid_number(value):
            return False
        return float(value) > 0

    def is_non_negative_number(self, value: str) -> bool:
        """检查是否为非负数字符串
        
        Args:
            value: 待检查的字符串
            
        Returns:
            True表示是非负数，False表示不是
        """
        if not self.is_valid_number(value):
            return False
        return float(value) >= 0
