import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculator_core import CalculatorCore
from input_validator import InputValidator
from result_formatter import ResultFormatter
from history_manager import HistoryManager
from config_handler import ConfigHandler


class CalculatorApp:
    """科学计算器主应用程序"""

    def __init__(self):
        """初始化计算器应用"""
        self.core = CalculatorCore()
        self.validator = InputValidator()
        self.config = ConfigHandler()
        self.formatter = ResultFormatter(
            decimal_places=self.config.decimal_places,
            scientific_threshold=self.config.scientific_threshold
        )
        self.history = HistoryManager()
        self.running = True

    def _sync_config(self):
        """同步配置到各个模块"""
        self.formatter.set_decimal_places(self.config.decimal_places)
        self.formatter.set_scientific_threshold(self.config.scientific_threshold)

    def show_main_menu(self):
        """显示主菜单"""
        print("\n" + "=" * 50)
        print("Python科学计算器 v2.0".center(50))
        print("=" * 50)
        
        mode_info = "[兼容模式]" if self.config.compatibility_mode else ""
        angle_info = "角度模式" if self.config.use_degree else "弧度模式"
        print(f"当前状态: {mode_info} {angle_info}".center(50))
        print("-" * 50)
        
        if self.config.compatibility_mode:
            print("1. 四则运算 (兼容模式)")
        else:
            print("1. 基础四则运算")
            print("2. 三角函数运算")
            print("3. 对数与指数运算")
            print("4. 幂运算与开方")
            print("5. 阶乘与其他运算")
        
        print("\n6. 历史记录")
        print("7. 系统设置")
        print("0. 退出程序")
        print("-" * 50)

    def get_valid_input(self, prompt: str, validate_func=None) -> str:
        """获取有效的用户输入
        
        Args:
            prompt: 提示信息
            validate_func: 验证函数
            
        Returns:
            有效的输入字符串
        """
        while True:
            try:
                user_input = input(prompt).strip()
                if user_input.lower() == 'q':
                    return None
                if validate_func and not validate_func(user_input):
                    print("输入无效，请重试（输入q返回上级）")
                    continue
                return user_input
            except (EOFError, KeyboardInterrupt):
                return None

    def get_number_input(self, prompt: str, validate_func=None) -> float:
        """获取数字输入
        
        Args:
            prompt: 提示信息
            validate_func: 额外验证函数
            
        Returns:
            有效的数字
        """
        while True:
            num_str = self.get_valid_input(prompt, self.validator.is_valid_number)
            if num_str is None:
                return None
            try:
                num = float(num_str)
                if validate_func and not validate_func(num):
                    print("输入值不符合要求，请重试")
                    continue
                return num
            except ValueError:
                print("请输入有效数字")

    def basic_arithmetic_menu(self):
        """基础四则运算菜单"""
        while True:
            print("\n--- 基础四则运算 ---")
            print("1. 加法 (+)")
            print("2. 减法 (-)")
            print("3. 乘法 (*)")
            print("4. 除法 (/)")
            print("0. 返回主菜单")
            
            choice = self.get_valid_input("请选择运算: ", 
                lambda x: self.validator.validate_menu_choice(x, 4))
            if choice is None or choice == '0':
                return
            
            a = self.get_number_input("请输入第一个数: ")
            if a is None:
                continue
            b = self.get_number_input("请输入第二个数: ")
            if b is None:
                continue
            
            try:
                if choice == '1':
                    result = self.core.add(a, b)
                    expr = f"{a} + {b}"
                elif choice == '2':
                    result = self.core.subtract(a, b)
                    expr = f"{a} - {b}"
                elif choice == '3':
                    result = self.core.multiply(a, b)
                    expr = f"{a} * {b}"
                elif choice == '4':
                    result = self.core.divide(a, b)
                    expr = f"{a} / {b}"
                
                print(f"\n结果: {self.formatter.format_result(expr, result)}")
                self.history.add_record(expr, result)
            except Exception as e:
                print(f"\n{self.formatter.format_error(str(e))}")

    def trigonometric_menu(self):
        """三角函数运算菜单"""
        while True:
            mode = "角度" if self.config.use_degree else "弧度"
            print(f"\n--- 三角函数运算 ({mode}) ---")
            print("1. 正弦 (sin)")
            print("2. 余弦 (cos)")
            print("3. 正切 (tan)")
            print("4. 切换角度/弧度模式")
            print("0. 返回主菜单")
            
            choice = self.get_valid_input("请选择: ", 
                lambda x: self.validator.validate_menu_choice(x, 4))
            if choice is None or choice == '0':
                return
            
            if choice == '4':
                new_mode = self.config.toggle_angle_mode()
                print(f"已切换为: {'角度模式' if new_mode else '弧度模式'}")
                continue
            
            x = self.get_number_input("请输入值: ")
            if x is None:
                continue
            
            try:
                func_name = ""
                if choice == '1':
                    result = self.core.sin(x, self.config.use_degree)
                    func_name = "sin"
                elif choice == '2':
                    result = self.core.cos(x, self.config.use_degree)
                    func_name = "cos"
                elif choice == '3':
                    result = self.core.tan(x, self.config.use_degree)
                    func_name = "tan"
                
                print(f"\n结果: {self.formatter.format_trigonometric_result(func_name, x, result, self.config.use_degree)}")
                self.history.add_record(f"{func_name}({x})", result)
            except Exception as e:
                print(f"\n{self.formatter.format_error(str(e))}")

    def logarithm_menu(self):
        """对数与指数运算菜单"""
        while True:
            print("\n--- 对数与指数运算 ---")
            print("1. 自然对数 (ln)")
            print("2. 常用对数 (log10)")
            print("3. 指数函数 (e^x)")
            print("0. 返回主菜单")
            
            choice = self.get_valid_input("请选择: ", 
                lambda x: self.validator.validate_menu_choice(x, 3))
            if choice is None or choice == '0':
                return
            
            try:
                if choice == '1':
                    x = self.get_number_input("请输入x (x > 0): ", lambda n: n > 0)
                    if x is None:
                        continue
                    result = self.core.ln(x)
                    expr = f"ln({x})"
                elif choice == '2':
                    x = self.get_number_input("请输入x (x > 0): ", lambda n: n > 0)
                    if x is None:
                        continue
                    result = self.core.log10(x)
                    expr = f"log10({x})"
                elif choice == '3':
                    x = self.get_number_input("请输入x: ")
                    if x is None:
                        continue
                    result = self.core.exp(x)
                    expr = f"e^{x}"
                
                print(f"\n结果: {self.formatter.format_result(expr, result)}")
                self.history.add_record(expr, result)
            except Exception as e:
                print(f"\n{self.formatter.format_error(str(e))}")

    def power_menu(self):
        """幂运算与开方菜单"""
        while True:
            print("\n--- 幂运算与开方 ---")
            print("1. 幂运算 (x^y)")
            print("2. 开平方 (√x)")
            print("0. 返回主菜单")
            
            choice = self.get_valid_input("请选择: ", 
                lambda x: self.validator.validate_menu_choice(x, 2))
            if choice is None or choice == '0':
                return
            
            try:
                if choice == '1':
                    base = self.get_number_input("请输入底数: ")
                    if base is None:
                        continue
                    exp = self.get_number_input("请输入指数: ")
                    if exp is None:
                        continue
                    result = self.core.power(base, exp)
                    expr = f"{base}^{exp}"
                elif choice == '2':
                    x = self.get_number_input("请输入x (x >= 0): ", lambda n: n >= 0)
                    if x is None:
                        continue
                    result = self.core.sqrt(x)
                    expr = f"√{x}"
                
                print(f"\n结果: {self.formatter.format_result(expr, result)}")
                self.history.add_record(expr, result)
            except Exception as e:
                print(f"\n{self.formatter.format_error(str(e))}")

    def other_menu(self):
        """阶乘与其他运算菜单"""
        while True:
            print("\n--- 阶乘与其他运算 ---")
            print("1. 阶乘 (n!)")
            print("2. 绝对值 (|x|)")
            print("3. 倒数 (1/x)")
            print("0. 返回主菜单")
            
            choice = self.get_valid_input("请选择: ", 
                lambda x: self.validator.validate_menu_choice(x, 3))
            if choice is None or choice == '0':
                return
            
            try:
                if choice == '1':
                    n_str = self.get_valid_input("请输入n (非负整数): ", 
                        self.validator.is_non_negative_integer)
                    if n_str is None:
                        continue
                    n = int(float(n_str))
                    result = self.core.factorial(n)
                    expr = f"{n}!"
                elif choice == '2':
                    x = self.get_number_input("请输入x: ")
                    if x is None:
                        continue
                    result = self.core.abs_value(x)
                    expr = f"|{x}|"
                elif choice == '3':
                    x = self.get_number_input("请输入x (x ≠ 0): ", lambda n: n != 0)
                    if x is None:
                        continue
                    result = self.core.reciprocal(x)
                    expr = f"1/{x}"
                
                print(f"\n结果: {self.formatter.format_result(expr, result)}")
                self.history.add_record(expr, result)
            except Exception as e:
                print(f"\n{self.formatter.format_error(str(e))}")

    def history_menu(self):
        """历史记录菜单"""
        while True:
            print("\n--- 历史记录 ---")
            print("1. 查看最近记录")
            print("2. 导出历史记录")
            print("3. 清空历史记录")
            print("0. 返回主菜单")
            
            choice = self.get_valid_input("请选择: ", 
                lambda x: self.validator.validate_menu_choice(x, 3))
            if choice is None or choice == '0':
                return
            
            if choice == '1':
                records = self.history.get_history(10)
                if not records:
                    print("\n暂无历史记录")
                else:
                    print("\n" + "-" * 50)
                    for i, record in enumerate(records, 1):
                        print(f"\n{i}. {record}")
                    print("-" * 50)
            elif choice == '2':
                if self.history.export_history():
                    print("\n历史记录已导出到文件")
                else:
                    print("\n导出失败")
            elif choice == '3':
                confirm = input("确认清空历史记录? (y/N): ").strip().lower()
                if confirm == 'y':
                    if self.history.clear_history():
                        print("\n历史记录已清空")
                    else:
                        print("\n清空失败")

    def settings_menu(self):
        """系统设置菜单"""
        while True:
            print("\n--- 系统设置 ---")
            print(f"1. 小数位数设置 (当前: {self.config.decimal_places})")
            print(f"2. 角度/弧度切换 (当前: {'角度' if self.config.use_degree else '弧度'})")
            print(f"3. 兼容模式切换 (当前: {'开启' if self.config.compatibility_mode else '关闭'})")
            print(f"4. 科学计数法阈值 (当前: {self.config.scientific_threshold})")
            print("5. 恢复默认设置")
            print("0. 返回主菜单")
            
            choice = self.get_valid_input("请选择: ", 
                lambda x: self.validator.validate_menu_choice(x, 5))
            if choice is None or choice == '0':
                return
            
            if choice == '1':
                places_str = self.get_valid_input("请输入小数位数 (0-10): ", 
                    lambda x: x.isdigit() and 0 <= int(x) <= 10)
                if places_str:
                    self.config.decimal_places = int(places_str)
                    self._sync_config()
                    print(f"小数位数已设置为: {self.config.decimal_places}")
            elif choice == '2':
                new_mode = self.config.toggle_angle_mode()
                print(f"已切换为: {'角度模式' if new_mode else '弧度模式'}")
            elif choice == '3':
                new_mode = self.config.toggle_compatibility_mode()
                print(f"兼容模式已{'开启' if new_mode else '关闭'}")
            elif choice == '4':
                thresh_str = self.get_valid_input("请输入科学计数法阈值: ", 
                    self.validator.is_positive_number)
                if thresh_str:
                    self.config.scientific_threshold = float(thresh_str)
                    self._sync_config()
                    print(f"阈值已设置为: {self.config.scientific_threshold}")
            elif choice == '5':
                confirm = input("确认恢复默认设置? (y/N): ").strip().lower()
                if confirm == 'y':
                    self.config.reset_defaults()
                    self._sync_config()
                    print("已恢复默认设置")

    def compatibility_mode(self):
        """兼容模式运行"""
        print("\n" + "=" * 50)
        print("兼容模式（支持旧版本输入如: 3+5）".center(50))
        print("=" * 50)
        print("直接输入表达式（如: 1+2, -3.5*4）或输入q返回")
        
        while True:
            try:
                expr = input("\n请输入表达式: ").strip()
                if expr.lower() == 'q':
                    break
                if not expr:
                    continue
                
                parsed = self.validator.parse_compatibility_input(expr)
                if parsed is None:
                    print("输入格式无效，请输入类似 '3+5' 的表达式")
                    continue
                
                a, op, b = parsed
                try:
                    if op == '+':
                        result = self.core.add(a, b)
                    elif op == '-':
                        result = self.core.subtract(a, b)
                    elif op == '*':
                        result = self.core.multiply(a, b)
                    elif op == '/':
                        result = self.core.divide(a, b)
                    
                    print(f"结果: {self.formatter.format_result(f'{a}{op}{b}', result)}")
                    self.history.add_record(f"{a}{op}{b}", result)
                except Exception as e:
                    print(f"错误: {str(e)}")
            except (EOFError, KeyboardInterrupt):
                break

    def run(self):
        """运行计算器主循环"""
        print("\n欢迎使用Python科学计算器 v2.0!")
        print("输入过程中可随时输入q返回上级菜单")
        
        while self.running:
            try:
                if self.config.compatibility_mode:
                    self.compatibility_mode()
                    break
                
                self.show_main_menu()
                choice = self.get_valid_input("请选择功能: ", 
                    lambda x: self.validator.validate_menu_choice(x, 7))
                
                if choice is None or choice == '0':
                    self.running = False
                    print("\n感谢使用科学计算器，再见!")
                    break
                
                if choice == '1':
                    self.basic_arithmetic_menu()
                elif choice == '2':
                    self.trigonometric_menu()
                elif choice == '3':
                    self.logarithm_menu()
                elif choice == '4':
                    self.power_menu()
                elif choice == '5':
                    self.other_menu()
                elif choice == '6':
                    self.history_menu()
                elif choice == '7':
                    self.settings_menu()
            except Exception as e:
                print(f"\n系统错误: {str(e)}")
                print("程序将继续运行...")
        
        self.core.clear_cache()


if __name__ == "__main__":
    try:
        app = CalculatorApp()
        app.run()
    except Exception as e:
        print(f"程序启动失败: {str(e)}")
        sys.exit(1)
