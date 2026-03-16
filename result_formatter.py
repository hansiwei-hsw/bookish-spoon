"""
结果格式化模块
负责格式化输出结果、保留小数位数、科学计数法切换等
"""
from typing import Union
from config_handler import get_config


class ResultFormatter:
    """
    结果格式化器类
    负责格式化计算结果
    """
    
    @staticmethod
    def format_result(
        result: Union[int, float],
        decimal_places: int = None,
        use_scientific: bool = None,
        scientific_threshold: float = None
    ) -> str:
        """
        格式化计算结果
        
        Args:
            result: 计算结果
            decimal_places: 小数位数（None则从配置读取）
            use_scientific: 是否使用科学计数法（None则自动判断）
            scientific_threshold: 科学计数法阈值
            
        Returns:
            格式化后的结果字符串
        """
        config = get_config()
        
        if decimal_places is None:
            decimal_places = config.get_decimal_places()
        
        if scientific_threshold is None:
            scientific_threshold = config.get_scientific_threshold()
        
        if isinstance(result, int):
            return str(result)
        
        if result == int(result) and use_scientific is not True:
            return str(int(result))
        
        abs_result = abs(result)
        
        if use_scientific is True or (use_scientific is None and (abs_result >= scientific_threshold or (abs_result > 0 and abs_result < 1e-4))):
            return f"{result:.{decimal_places}e}"
        
        format_str = f"{{:.{decimal_places}f}}"
        formatted = format_str.format(result)
        
        if '.' in formatted:
            formatted = formatted.rstrip('0').rstrip('.')
        
        return formatted
    
    @staticmethod
    def format_expression(
        num1: Union[int, float],
        op: str,
        num2: Union[int, float],
        result: Union[int, float],
        decimal_places: int = None
    ) -> str:
        """
        格式化完整表达式
        
        Args:
            num1: 第一个操作数
            op: 运算符
            num2: 第二个操作数
            result: 计算结果
            decimal_places: 小数位数
            
        Returns:
            格式化后的表达式字符串
        """
        config = get_config()
        
        if decimal_places is None:
            decimal_places = config.get_decimal_places()
        
        def format_num(n):
            if isinstance(n, int) or (isinstance(n, float) and n == int(n)):
                return str(int(n))
            return f"{n:.{decimal_places}f}".rstrip('0').rstrip('.')
        
        n1_str = format_num(num1)
        n2_str = format_num(num2)
        result_str = ResultFormatter.format_result(result, decimal_places)
        
        return f"{n1_str} {op} {n2_str} = {result_str}"
    
    @staticmethod
    def format_single_operand(
        op: str,
        num: Union[int, float],
        result: Union[int, float],
        decimal_places: int = None
    ) -> str:
        """
        格式化单操作数表达式
        
        Args:
            op: 运算符
            num: 操作数
            result: 计算结果
            decimal_places: 小数位数
            
        Returns:
            格式化后的表达式字符串
        """
        config = get_config()
        
        if decimal_places is None:
            decimal_places = config.get_decimal_places()
        
        def format_num(n):
            if isinstance(n, int) or (isinstance(n, float) and n == int(n)):
                return str(int(n))
            return f"{n:.{decimal_places}f}".rstrip('0').rstrip('.')
        
        num_str = format_num(num)
        result_str = ResultFormatter.format_result(result, decimal_places)
        
        return f"{op}({num_str}) = {result_str}"
    
    @staticmethod
    def format_error(error_msg: str) -> str:
        """
        格式化错误信息
        
        Args:
            error_msg: 错误信息
            
        Returns:
            格式化后的错误字符串
        """
        return f"[错误] {error_msg}"
    
    @staticmethod
    def format_history_record(
        index: int,
        expression: str,
        timestamp: str = None
    ) -> str:
        """
        格式化历史记录条目
        
        Args:
            index: 序号
            expression: 表达式
            timestamp: 时间戳
            
        Returns:
            格式化后的历史记录字符串
        """
        if timestamp:
            return f"[{index}] {timestamp} - {expression}"
        return f"[{index}] {expression}"


def format_result(result: Union[int, float], **kwargs) -> str:
    """
    便捷函数：格式化结果
    
    Args:
        result: 计算结果
        **kwargs: 其他参数
        
    Returns:
        格式化后的字符串
    """
    return ResultFormatter.format_result(result, **kwargs)
