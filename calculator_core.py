"""
核心运算引擎模块
封装所有运算函数，实现运算逻辑，包含缓存机制
"""
import math
from typing import Union, Dict, Tuple, Optional, Callable
from functools import lru_cache
from config_handler import get_config


class CalculationError(Exception):
    """计算错误异常"""
    pass


class CalculatorCore:
    """
    计算器核心引擎类
    实现所有基础和科学运算
    """
    
    def __init__(self):
        """初始化计算器核心"""
        self._cache: Dict[str, float] = {}
        self._cache_enabled = True
        self._update_cache_config()
    
    def _update_cache_config(self) -> None:
        """更新缓存配置"""
        config = get_config()
        self._cache_enabled = config.is_cache_enabled()
        max_size = config.get_cache_max_size()
        
        if len(self._cache) > max_size:
            keys_to_remove = list(self._cache.keys())[:len(self._cache) - max_size]
            for key in keys_to_remove:
                del self._cache[key]
    
    def _get_cache_key(self, operation: str, *args) -> str:
        """生成缓存键，统一浮点数格式"""
        formatted_args = []
        for arg in args:
            if isinstance(arg, float):
                formatted_args.append(f"{arg:.10f}")
            else:
                formatted_args.append(str(arg))
        return f"{operation}:{':'.join(formatted_args)}"
    
    def _get_from_cache(self, key: str) -> Optional[float]:
        """从缓存获取结果"""
        if self._cache_enabled and key in self._cache:
            return self._cache[key]
        return None
    
    def _save_to_cache(self, key: str, result: float) -> None:
        """保存结果到缓存"""
        if self._cache_enabled:
            config = get_config()
            max_size = config.get_cache_max_size()
            
            if len(self._cache) >= max_size:
                first_key = next(iter(self._cache))
                del self._cache[first_key]
            
            self._cache[key] = result
    
    def clear_cache(self) -> None:
        """清空缓存"""
        self._cache.clear()
    
    @staticmethod
    def _to_radians(angle: float) -> float:
        """将角度转换为弧度"""
        config = get_config()
        if config.get_angle_mode() == 'degree':
            return math.radians(angle)
        return angle
    
    @staticmethod
    def _from_radians(radians: float) -> float:
        """将弧度转换为角度"""
        config = get_config()
        if config.get_angle_mode() == 'degree':
            return math.degrees(radians)
        return radians
    
    def add(self, a: float, b: float) -> float:
        """加法运算"""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """减法运算"""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """乘法运算"""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """
        除法运算
        
        Raises:
            CalculationError: 除数为0时抛出
        """
        if b == 0:
            raise CalculationError("除数不能为0")
        return a / b
    
    def sin(self, angle: float) -> float:
        """
        正弦函数
        
        Args:
            angle: 角度或弧度（取决于配置）
        """
        cache_key = self._get_cache_key('sin', angle)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        radians = self._to_radians(angle)
        result = math.sin(radians)
        self._save_to_cache(cache_key, result)
        return result
    
    def cos(self, angle: float) -> float:
        """
        余弦函数
        
        Args:
            angle: 角度或弧度（取决于配置）
        """
        cache_key = self._get_cache_key('cos', angle)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        radians = self._to_radians(angle)
        result = math.cos(radians)
        self._save_to_cache(cache_key, result)
        return result
    
    def tan(self, angle: float) -> float:
        """
        正切函数
        
        Args:
            angle: 角度或弧度（取决于配置）
            
        Raises:
            CalculationError: 角度无效时抛出
        """
        cache_key = self._get_cache_key('tan', angle)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        radians = self._to_radians(angle)
        
        try:
            result = math.tan(radians)
            if math.isinf(result) or math.isnan(result):
                raise CalculationError(f"tan({angle}) 无定义")
            self._save_to_cache(cache_key, result)
            return result
        except (ValueError, OverflowError):
            raise CalculationError(f"tan({angle}) 计算错误")
    
    def asin(self, value: float) -> float:
        """
        反正弦函数
        
        Args:
            value: 输入值（-1到1之间）
            
        Raises:
            CalculationError: 值超出范围时抛出
        """
        if value < -1 or value > 1:
            raise CalculationError(f"asin的参数必须在[-1, 1]范围内，当前值: {value}")
        
        cache_key = self._get_cache_key('asin', value)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        radians = math.asin(value)
        result = self._from_radians(radians)
        self._save_to_cache(cache_key, result)
        return result
    
    def acos(self, value: float) -> float:
        """
        反余弦函数
        
        Args:
            value: 输入值（-1到1之间）
            
        Raises:
            CalculationError: 值超出范围时抛出
        """
        if value < -1 or value > 1:
            raise CalculationError(f"acos的参数必须在[-1, 1]范围内，当前值: {value}")
        
        cache_key = self._get_cache_key('acos', value)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        radians = math.acos(value)
        result = self._from_radians(radians)
        self._save_to_cache(cache_key, result)
        return result
    
    def atan(self, value: float) -> float:
        """反正切函数"""
        cache_key = self._get_cache_key('atan', value)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        radians = math.atan(value)
        result = self._from_radians(radians)
        self._save_to_cache(cache_key, result)
        return result
    
    def ln(self, value: float) -> float:
        """
        自然对数
        
        Args:
            value: 输入值（必须大于0）
            
        Raises:
            CalculationError: 值小于等于0时抛出
        """
        if value <= 0:
            raise CalculationError(f"ln的参数必须大于0，当前值: {value}")
        
        cache_key = self._get_cache_key('ln', value)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        result = math.log(value)
        self._save_to_cache(cache_key, result)
        return result
    
    def log10(self, value: float) -> float:
        """
        常用对数（以10为底）
        
        Args:
            value: 输入值（必须大于0）
            
        Raises:
            CalculationError: 值小于等于0时抛出
        """
        if value <= 0:
            raise CalculationError(f"log10的参数必须大于0，当前值: {value}")
        
        cache_key = self._get_cache_key('log10', value)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        result = math.log10(value)
        self._save_to_cache(cache_key, result)
        return result
    
    def log(self, value: float, base: float = 10) -> float:
        """
        对数函数
        
        Args:
            value: 输入值（必须大于0）
            base: 底数（必须大于0且不等于1）
            
        Raises:
            CalculationError: 参数无效时抛出
        """
        if value <= 0:
            raise CalculationError(f"对数的真数必须大于0，当前值: {value}")
        if base <= 0 or base == 1:
            raise CalculationError(f"对数的底数必须大于0且不等于1，当前值: {base}")
        
        cache_key = self._get_cache_key('log', value, base)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        result = math.log(value, base)
        self._save_to_cache(cache_key, result)
        return result
    
    def sqrt(self, value: float) -> float:
        """
        平方根
        
        Args:
            value: 输入值（必须非负）
            
        Raises:
            CalculationError: 值为负数时抛出
        """
        if value < 0:
            raise CalculationError(f"sqrt的参数不能为负数，当前值: {value}")
        
        cache_key = self._get_cache_key('sqrt', value)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        result = math.sqrt(value)
        self._save_to_cache(cache_key, result)
        return result
    
    def power(self, base: float, exponent: float) -> float:
        """
        幂运算
        
        Args:
            base: 底数
            exponent: 指数
            
        Raises:
            CalculationError: 运算无效时抛出
        """
        cache_key = self._get_cache_key('power', base, exponent)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        try:
            if base < 0 and not exponent == int(exponent):
                raise CalculationError(f"负数的非整数次幂无定义: {base}^{exponent}")
            
            result = math.pow(base, exponent)
            
            if math.isinf(result):
                raise CalculationError(f"计算结果溢出: {base}^{exponent}")
            
            self._save_to_cache(cache_key, result)
            return result
        except (ValueError, OverflowError) as e:
            raise CalculationError(f"幂运算错误: {e}")
    
    def factorial(self, n: int) -> int:
        """
        阶乘运算
        
        Args:
            n: 非负整数
            
        Raises:
            CalculationError: 参数无效时抛出
        """
        if not isinstance(n, int) and n != int(n):
            raise CalculationError(f"阶乘的参数必须是整数，当前值: {n}")
        
        n = int(n)
        
        if n < 0:
            raise CalculationError(f"阶乘的参数不能为负数，当前值: {n}")
        
        if n > 170:
            raise CalculationError(f"阶乘参数过大（最大170），当前值: {n}")
        
        cache_key = self._get_cache_key('factorial', n)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return int(cached)
        
        result = math.factorial(n)
        self._save_to_cache(cache_key, float(result))
        return result
    
    def abs(self, value: float) -> float:
        """绝对值"""
        return abs(value)
    
    def exp(self, value: float) -> float:
        """
        e的幂次方
        
        Args:
            value: 指数
            
        Raises:
            CalculationError: 结果溢出时抛出
        """
        cache_key = self._get_cache_key('exp', value)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        try:
            result = math.exp(value)
            if math.isinf(result):
                raise CalculationError(f"exp({value}) 结果溢出")
            self._save_to_cache(cache_key, result)
            return result
        except OverflowError:
            raise CalculationError(f"exp({value}) 结果溢出")
    
    def calculate(self, num1: float, op: str, num2: float = None) -> float:
        """
        通用计算接口
        
        Args:
            num1: 第一个操作数（或单操作数运算的操作数）
            op: 运算符
            num2: 第二个操作数（单操作数运算时为None）
            
        Returns:
            计算结果
            
        Raises:
            CalculationError: 运算错误时抛出
        """
        binary_ops = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide,
            '^': self.power,
            'pow': self.power,
        }
        
        unary_ops = {
            'sin': self.sin,
            'cos': self.cos,
            'tan': self.tan,
            'asin': self.asin,
            'acos': self.acos,
            'atan': self.atan,
            'ln': self.ln,
            'log': self.log10,
            'log10': self.log10,
            'sqrt': self.sqrt,
            'factorial': self.factorial,
            '!': self.factorial,
            'abs': self.abs,
            'exp': self.exp,
        }
        
        op_lower = op.lower()
        
        if op_lower in binary_ops:
            if num2 is None:
                raise CalculationError(f"运算符 '{op}' 需要两个操作数")
            return binary_ops[op_lower](num1, num2)
        
        if op_lower in unary_ops:
            return unary_ops[op_lower](num1)
        
        raise CalculationError(f"未知运算符: {op}")


_calculator_instance = None


def get_calculator() -> CalculatorCore:
    """获取计算器单例"""
    global _calculator_instance
    if _calculator_instance is None:
        _calculator_instance = CalculatorCore()
    return _calculator_instance
