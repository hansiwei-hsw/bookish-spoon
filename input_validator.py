"""
输入校验模块
负责验证用户输入的数字、运算符合法性，并格式化输入
"""
import re
from typing import Tuple, Optional, Union, List


class InputValidator:
    """
    输入校验器类
    负责验证和格式化用户输入
    """
    
    VALID_BASIC_OPERATORS = ['+', '-', '*', '/']
    VALID_SCIENTIFIC_OPERATORS = [
        'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
        'ln', 'log', 'log10',
        'sqrt', 'pow', '^',
        'factorial', '!',
        'abs', 'exp'
    ]
    
    NUMBER_PATTERN = re.compile(r'^[+-]?\d*\.?\d+(?:[eE][+-]?\d+)?$')
    
    @classmethod
    def validate_number(cls, input_str: str) -> Tuple[bool, Optional[float], str]:
        """
        验证输入是否为有效数字
        
        Args:
            input_str: 用户输入字符串
            
        Returns:
            Tuple[是否有效, 转换后的数字, 错误信息]
        """
        if not input_str or not input_str.strip():
            return False, None, "输入不能为空"
        
        input_str = input_str.strip()
        
        try:
            num = float(input_str)
            return True, num, ""
        except ValueError:
            return False, None, f"'{input_str}' 不是有效的数字"
    
    @classmethod
    def validate_integer(cls, input_str: str, min_val: int = None, max_val: int = None) -> Tuple[bool, Optional[int], str]:
        """
        验证输入是否为有效整数
        
        Args:
            input_str: 用户输入字符串
            min_val: 最小值限制
            max_val: 最大值限制
            
        Returns:
            Tuple[是否有效, 转换后的整数, 错误信息]
        """
        if not input_str or not input_str.strip():
            return False, None, "输入不能为空"
        
        input_str = input_str.strip()
        
        try:
            num = int(float(input_str))
            if float(input_str) != num:
                return False, None, "请输入整数"
            
            if min_val is not None and num < min_val:
                return False, None, f"数值不能小于 {min_val}"
            
            if max_val is not None and num > max_val:
                return False, None, f"数值不能大于 {max_val}"
            
            return True, num, ""
        except ValueError:
            return False, None, f"'{input_str}' 不是有效的整数"
    
    @classmethod
    def validate_operator(cls, input_str: str, scientific: bool = False) -> Tuple[bool, Optional[str], str]:
        """
        验证运算符是否有效
        
        Args:
            input_str: 用户输入字符串
            scientific: 是否包含科学运算符
            
        Returns:
            Tuple[是否有效, 运算符, 错误信息]
        """
        if not input_str or not input_str.strip():
            return False, None, "运算符不能为空"
        
        op = input_str.strip().lower()
        
        if op in cls.VALID_BASIC_OPERATORS:
            return True, op, ""
        
        if scientific and op in cls.VALID_SCIENTIFIC_OPERATORS:
            return True, op, ""
        
        valid_ops = cls.VALID_BASIC_OPERATORS.copy()
        if scientific:
            valid_ops.extend(cls.VALID_SCIENTIFIC_OPERATORS)
        
        return False, None, f"无效运算符，有效运算符: {', '.join(valid_ops)}"
    
    @classmethod
    def validate_positive_number(cls, input_str: str) -> Tuple[bool, Optional[float], str]:
        """
        验证输入是否为正数
        
        Args:
            input_str: 用户输入字符串
            
        Returns:
            Tuple[是否有效, 转换后的数字, 错误信息]
        """
        is_valid, num, error = cls.validate_number(input_str)
        if not is_valid:
            return False, None, error
        
        if num <= 0:
            return False, None, "数值必须大于0"
        
        return True, num, ""
    
    @classmethod
    def validate_non_negative_number(cls, input_str: str) -> Tuple[bool, Optional[float], str]:
        """
        验证输入是否为非负数
        
        Args:
            input_str: 用户输入字符串
            
        Returns:
            Tuple[是否有效, 转换后的数字, 错误信息]
        """
        is_valid, num, error = cls.validate_number(input_str)
        if not is_valid:
            return False, None, error
        
        if num < 0:
            return False, None, "数值不能为负数"
        
        return True, num, ""
    
    @classmethod
    def validate_menu_choice(cls, input_str: str, valid_choices: List[str]) -> Tuple[bool, Optional[str], str]:
        """
        验证菜单选择是否有效
        
        Args:
            input_str: 用户输入字符串
            valid_choices: 有效选项列表
            
        Returns:
            Tuple[是否有效, 选项, 错误信息]
        """
        if not input_str or not input_str.strip():
            return False, None, "请输入选项"
        
        choice = input_str.strip()
        
        if choice in valid_choices:
            return True, choice, ""
        
        return False, None, f"无效选项，请选择: {', '.join(valid_choices)}"
    
    @classmethod
    def parse_expression(cls, expression: str) -> Tuple[bool, Optional[List], str]:
        """
        解析简单表达式（兼容模式使用）
        支持格式: "num1 op num2" 或 "op num"
        
        Args:
            expression: 表达式字符串
            
        Returns:
            Tuple[是否有效, 解析结果列表, 错误信息]
        """
        if not expression or not expression.strip():
            return False, None, "表达式不能为空"
        
        expression = expression.strip()
        tokens = expression.split()
        
        if len(tokens) == 3:
            valid1, num1, err1 = cls.validate_number(tokens[0])
            if not valid1:
                return False, None, f"第一个操作数无效: {err1}"
            
            valid_op, op, err_op = cls.validate_operator(tokens[1], scientific=True)
            if not valid_op:
                return False, None, f"运算符无效: {err_op}"
            
            valid2, num2, err2 = cls.validate_number(tokens[2])
            if not valid2:
                return False, None, f"第二个操作数无效: {err2}"
            
            return True, [num1, op, num2], ""
        
        elif len(tokens) == 2:
            valid_op, op, err_op = cls.validate_operator(tokens[0], scientific=True)
            if not valid_op:
                return False, None, f"运算符无效: {err_op}"
            
            valid_num, num, err_num = cls.validate_number(tokens[1])
            if not valid_num:
                return False, None, f"操作数无效: {err_num}"
            
            return True, [op, num], ""
        
        else:
            return False, None, "表达式格式错误，应为 'num1 op num2' 或 'op num'"


def get_number_input(prompt: str, validator_func=None) -> float:
    """
    获取用户输入的数字（带校验循环）
    
    Args:
        prompt: 提示信息
        validator_func: 自定义校验函数
        
    Returns:
        用户输入的有效数字
    """
    while True:
        user_input = input(prompt)
        
        if validator_func:
            is_valid, value, error = validator_func(user_input)
        else:
            is_valid, value, error = InputValidator.validate_number(user_input)
        
        if is_valid:
            return value
        
        print(f"输入错误: {error}")


def get_operator_input(prompt: str, scientific: bool = False) -> str:
    """
    获取用户输入的运算符（带校验循环）
    
    Args:
        prompt: 提示信息
        scientific: 是否包含科学运算符
        
    Returns:
        用户输入的有效运算符
    """
    while True:
        user_input = input(prompt)
        is_valid, op, error = InputValidator.validate_operator(user_input, scientific)
        
        if is_valid:
            return op
        
        print(f"输入错误: {error}")
