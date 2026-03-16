class ResultFormatter:
    """结果处理模块：格式化输出、保留小数、科学计数法切换"""

    ZERO_TOLERANCE = 1e-10

    def __init__(self, decimal_places: int = 4, scientific_threshold: float = 1e6):
        """初始化结果格式化器
        
        Args:
            decimal_places: 默认保留小数位数
            scientific_threshold: 科学计数法阈值（绝对值大于此值时使用科学计数法）
        """
        self.decimal_places = decimal_places
        self.scientific_threshold = scientific_threshold

    def format_number(self, value: float, decimal_places: int = None) -> str:
        """格式化数字输出
        
        Args:
            value: 待格式化的数字
            decimal_places: 保留小数位数，None使用默认值
            
        Returns:
            格式化后的字符串
        """
        if decimal_places is None:
            decimal_places = self.decimal_places

        if abs(value) < self.ZERO_TOLERANCE:
            return "0"

        rounded = round(value, decimal_places + 2)
        if abs(rounded) < self.ZERO_TOLERANCE:
            return "0"

        if abs(value) >= self.scientific_threshold or abs(value) <= 1e-4:
            return self.format_scientific(value, decimal_places)

        if abs(value - int(value)) < self.ZERO_TOLERANCE:
            return str(int(value))

        format_str = "{:." + str(decimal_places) + "f}"
        result = format_str.format(value)
        result = result.rstrip('0').rstrip('.') if '.' in result else result
        return result

    def format_scientific(self, value: float, decimal_places: int = None) -> str:
        """使用科学计数法格式化数字
        
        Args:
            value: 待格式化的数字
            decimal_places: 保留小数位数，None使用默认值
            
        Returns:
            科学计数法表示的字符串
        """
        if decimal_places is None:
            decimal_places = self.decimal_places
        format_str = "{:." + str(decimal_places) + "e}"
        return format_str.format(value)

    def format_result(self, expression: str, result: float, 
                      decimal_places: int = None) -> str:
        """格式化完整运算结果
        
        Args:
            expression: 运算表达式字符串
            result: 运算结果
            decimal_places: 保留小数位数
            
        Returns:
            格式化后的完整结果字符串
        """
        formatted_result = self.format_number(result, decimal_places)
        return f"{expression} = {formatted_result}"

    def set_decimal_places(self, places: int):
        """设置默认保留小数位数
        
        Args:
            places: 小数位数（0-10）
            
        Raises:
            ValueError: 当places不在有效范围时抛出
        """
        if not (0 <= places <= 10):
            raise ValueError("小数位数必须在0到10之间")
        self.decimal_places = places

    def set_scientific_threshold(self, threshold: float):
        """设置科学计数法阈值
        
        Args:
            threshold: 阈值，必须大于0
            
        Raises:
            ValueError: 当threshold <= 0时抛出
        """
        if threshold <= 0:
            raise ValueError("科学计数法阈值必须大于0")
        self.scientific_threshold = threshold

    def format_trigonometric_result(self, func_name: str, 
                                    angle: float, result: float,
                                    use_degree: bool = False,
                                    decimal_places: int = None) -> str:
        """格式化三角函数结果
        
        Args:
            func_name: 函数名（sin/cos/tan）
            angle: 角度/弧度值
            result: 运算结果
            use_degree: True表示角度，False表示弧度
            decimal_places: 保留小数位数
            
        Returns:
            格式化后的结果字符串
        """
        unit = "°" if use_degree else " rad"
        formatted_result = self.format_number(result, decimal_places)
        return f"{func_name}({angle}{unit}) = {formatted_result}"

    def format_error(self, error_msg: str) -> str:
        """格式化错误信息
        
        Args:
            error_msg: 错误信息
            
        Returns:
            格式化后的错误字符串
        """
        return f"错误: {error_msg}"
