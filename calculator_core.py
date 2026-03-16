import math
import functools


class CalculatorCore:
    """科学计算器核心运算引擎，封装所有运算函数"""

    def __init__(self):
        """初始化运算引擎，配置缓存机制"""
        self._cache = {}
        self._max_cache_size = 100

    def _clear_old_cache(self):
        """清理旧缓存，保持缓存大小在合理范围"""
        if len(self._cache) > self._max_cache_size:
            self._cache = dict(list(self._cache.items())[-50:])

    def _cached(self, func):
        """缓存装饰器，缓存高频计算结果"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, tuple(kwargs.items()))
            if key in self._cache:
                return self._cache[key]
            result = func(*args, **kwargs)
            self._cache[key] = result
            self._clear_old_cache()
            return result
        return wrapper

    def add(self, a: float, b: float) -> float:
        """加法运算：a + b"""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """减法运算：a - b"""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """乘法运算：a * b"""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """除法运算：a / b
        
        Raises:
            ZeroDivisionError: 当b为0时抛出
        """
        if b == 0:
            raise ZeroDivisionError("除数不能为零")
        return a / b

    @functools.lru_cache(maxsize=32)
    def _deg_to_rad(self, angle: float) -> float:
        """角度转弧度"""
        return math.radians(angle)

    @functools.lru_cache(maxsize=32)
    def _rad_to_deg(self, radian: float) -> float:
        """弧度转角度"""
        return math.degrees(radian)

    def sin(self, x: float, use_degree: bool = False) -> float:
        """正弦函数
        
        Args:
            x: 角度值或弧度值
            use_degree: True表示x是角度，False表示x是弧度
        """
        if use_degree:
            x = self._deg_to_rad(x)
        return math.sin(x)

    def cos(self, x: float, use_degree: bool = False) -> float:
        """余弦函数
        
        Args:
            x: 角度值或弧度值
            use_degree: True表示x是角度，False表示x是弧度
        """
        if use_degree:
            x = self._deg_to_rad(x)
        return math.cos(x)

    def tan(self, x: float, use_degree: bool = False) -> float:
        """正切函数
        
        Args:
            x: 角度值或弧度值
            use_degree: True表示x是角度，False表示x是弧度
        """
        if use_degree:
            x = self._deg_to_rad(x)
        if abs(math.cos(x)) < 1e-10:
            raise ValueError(f"tan({x}) 无定义（余弦值为0）")
        return math.tan(x)

    def ln(self, x: float) -> float:
        """自然对数函数ln(x)
        
        Raises:
            ValueError: 当x <= 0时抛出
        """
        if x <= 0:
            raise ValueError("ln(x) 要求 x > 0")
        return math.log(x)

    def log10(self, x: float) -> float:
        """常用对数函数log10(x)
        
        Raises:
            ValueError: 当x <= 0时抛出
        """
        if x <= 0:
            raise ValueError("log10(x) 要求 x > 0")
        return math.log10(x)

    def power(self, base: float, exponent: float) -> float:
        """幂运算：base^exponent
        
        Raises:
            ValueError: 当base为负数且exponent不是整数时抛出
        """
        if base < 0 and not float(exponent).is_integer():
            raise ValueError("负数的非整数次幂无实数解")
        return math.pow(base, exponent)

    def sqrt(self, x: float) -> float:
        """开平方运算：√x
        
        Raises:
            ValueError: 当x < 0时抛出
        """
        if x < 0:
            raise ValueError("√x 要求 x >= 0")
        return math.sqrt(x)

    def factorial(self, n: int) -> int:
        """阶乘运算：n!
        
        Args:
            n: 非负整数
            
        Raises:
            ValueError: 当n < 0或n不是整数时抛出
            OverflowError: 结果过大时抛出
        """
        if n < 0:
            raise ValueError("阶乘要求 n >= 0")
        if not float(n).is_integer():
            raise ValueError("阶乘要求n为整数")
        n = int(n)
        if n > 1000:
            raise OverflowError("n过大，计算结果超出范围")
        return math.factorial(n)

    def abs_value(self, x: float) -> float:
        """绝对值运算：|x|"""
        return abs(x)

    def reciprocal(self, x: float) -> float:
        """倒数运算：1/x
        
        Raises:
            ZeroDivisionError: 当x为0时抛出
        """
        if x == 0:
            raise ZeroDivisionError("0没有倒数")
        return 1 / x

    def exp(self, x: float) -> float:
        """指数函数：e^x"""
        return math.exp(x)

    def clear_cache(self):
        """清除所有缓存"""
        self._cache.clear()
        self._deg_to_rad.cache_clear()
        self._rad_to_deg.cache_clear()
