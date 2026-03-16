"""
Python科学计算器 v2.0
程序入口，交互流程控制
"""
import sys
import os
from typing import Optional

from config_handler import get_config, ConfigHandler
from input_validator import InputValidator, get_number_input, get_operator_input
from result_formatter import ResultFormatter, format_result
from calculator_core import get_calculator, CalculatorCore, CalculationError
from history_manager import get_history, HistoryManager


class CalculatorApp:
    """
    计算器应用程序类
    负责交互流程控制
    """
    
    def __init__(self):
        """初始化计算器应用"""
        self.config = get_config()
        self.calculator = get_calculator()
        self.history = get_history()
        self.running = True
    
    def clear_screen(self) -> None:
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self) -> None:
        """显示程序头部信息"""
        print("=" * 50)
        print("       Python 科学计算器 v2.0")
        print("=" * 50)
        
        mode_str = "兼容模式" if self.config.is_compatibility_mode() else "标准模式"
        angle_str = "角度" if self.config.get_angle_mode() == 'degree' else "弧度"
        
        print(f"当前模式: {mode_str} | 角度单位: {angle_str}")
        print(f"小数位数: {self.config.get_decimal_places()}")
        print("-" * 50)
    
    def show_main_menu(self) -> None:
        """显示主菜单"""
        print("\n【主菜单】")
        print("1. 基础运算（四则运算）")
        print("2. 科学运算")
        print("3. 查看历史记录")
        print("4. 系统设置")
        print("5. 帮助说明")
        print("0. 退出程序")
        print("-" * 50)
    
    def show_scientific_menu(self) -> None:
        """显示科学运算菜单"""
        print("\n【科学运算】")
        print("1. 三角函数
        print("2. 反三角函数
        print("3. 对数运算
        print("4. 幂运算与开方 (x^y, √x)")
        print("5. 阶乘运算")
        print("6. 其他运算
        print("0. 返回主菜单")
        print("-" * 50)
    
    def show_settings_menu(self) -> None:
        """显示设置菜单"""
        print("\n【系统设置】")
        print(f"1. 切换角度模式 (当前: {self.config.get_angle_mode()})")
        print(f"2. 设置小数位数 (当前: {self.config.get_decimal_places()})")
        print(f"3. 切换兼容模式 (当前: {'开启' if self.config.is_compatibility_mode() else '关闭'})")
        print("4. 清空历史记录")
        print("5. 清空计算缓存")
        print("6. 重置所有设置")
        print("0. 返回主菜单")
        print("-" * 50)
    
    def do_basic_calculation(self) -> None:
        """执行基础四则运算"""
        print("\n【基础运算】")
        
        try:
            num1 = get_number_input("请输入第一个数字: ")
            op = get_operator_input("请输入运算符 (+, -, *, /): ", scientific=False)
            num2 = get_number_input("请输入第二个数字: ")
            
            result = self.calculator.calculate(num1, op, num2)
            
            expression = ResultFormatter.format_expression(num1, op, num2, result)
            print(f"\n计算结果: {expression}")
            
            self.history.add_record(
                f"{num1} {op} {num2}",
                format_result(result)
            )
            
        except CalculationError as e:
            print(f"\n{ResultFormatter.format_error(str(e))}")
        except KeyboardInterrupt:
            print("\n\n操作已取消")
    
    def do_scientific_calculation(self) -> None:
        """执行科学运算"""
        while True:
            self.show_scientific_menu()
            
            choice = input("请选择运算类型: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self._do_trigonometric()
            elif choice == '2':
                self._do_inverse_trigonometric()
            elif choice == '3':
                self._do_logarithm()
            elif choice == '4':
                self._do_power_sqrt()
            elif choice == '5':
                self._do_factorial()
            elif choice == '6':
                self._do_other()
            else:
                print("无效选项，请重新选择")
    
    def _do_trigonometric(self) -> None:
        """三角函数运算"""
        print("\n【三角函数】")
        print("支持: sin, cos, tan")
        
        try:
            op = input("请输入函数名: ").strip().lower()
            if op not in ['sin', 'cos', 'tan']:
                print("无效的函数名")
                return
            
            angle = get_number_input(f"请输入角度值 (当前模式: {self.config.get_angle_mode()}): ")
            
            result = self.calculator.calculate(angle, op)
            
            expression = ResultFormatter.format_single_operand(op, angle, result)
            print(f"\n计算结果: {expression}")
            
            self.history.add_record(f"{op}({angle})", format_result(result))
            
        except CalculationError as e:
            print(f"\n{ResultFormatter.format_error(str(e))}")
    
    def _do_inverse_trigonometric(self) -> None:
        """反三角函数运算"""
        print("\n【反三角函数】")
        print("支持: asin, acos, atan")
        
        try:
            op = input("请输入函数名: ").strip().lower()
            if op not in ['asin', 'acos', 'atan']:
                print("无效的函数名")
                return
            
            value = get_number_input("请输入值: ")
            
            result = self.calculator.calculate(value, op)
            
            expression = ResultFormatter.format_single_operand(op, value, result)
            print(f"\n计算结果: {expression}")
            
            self.history.add_record(f"{op}({value})", format_result(result))
            
        except CalculationError as e:
            print(f"\n{ResultFormatter.format_error(str(e))}")
    
    def _do_logarithm(self) -> None:
        """对数运算"""
        print("\n【对数运算】")
        print("1. ln(x) - 自然对数")
        print("2. log10(x) - 常用对数")
        print("3. log(x, base) - 自定义底数对数")
        
        choice = input("请选择: ").strip()
        
        try:
            if choice == '1':
                value = get_number_input("请输入值: ")
                result = self.calculator.ln(value)
                self.history.add_record(f"ln({value})", format_result(result))
            elif choice == '2':
                value = get_number_input("请输入值: ")
                result = self.calculator.log10(value)
                self.history.add_record(f"log10({value})", format_result(result))
            elif choice == '3':
                value = get_number_input("请输入真数: ")
                base = get_number_input("请输入底数: ")
                result = self.calculator.log(value, base)
                self.history.add_record(f"log({value}, {base})", format_result(result))
            else:
                print("无效选项")
                return
            
            print(f"\n计算结果: {format_result(result)}")
            
        except CalculationError as e:
            print(f"\n{ResultFormatter.format_error(str(e))}")
    
    def _do_power_sqrt(self) -> None:
        """幂运算与开方"""
        print("\n【幂运算与开方】")
        print("1. x^y - 幂运算")
        print("2. √x - 平方根")
        
        choice = input("请选择: ").strip()
        
        try:
            if choice == '1':
                base = get_number_input("请输入底数: ")
                exp = get_number_input("请输入指数: ")
                result = self.calculator.power(base, exp)
                self.history.add_record(f"{base}^{exp}", format_result(result))
            elif choice == '2':
                value = get_number_input("请输入值: ")
                result = self.calculator.sqrt(value)
                self.history.add_record(f"sqrt({value})", format_result(result))
            else:
                print("无效选项")
                return
            
            print(f"\n计算结果: {format_result(result)}")
            
        except CalculationError as e:
            print(f"\n{ResultFormatter.format_error(str(e))}")
    
    def _do_factorial(self) -> None:
        """阶乘运算"""
        print("\n【阶乘运算】")
        
        try:
            n = int(get_number_input("请输入非负整数: "))
            result = self.calculator.factorial(n)
            
            print(f"\n计算结果: {n}! = {result}")
            self.history.add_record(f"{n}!", str(result))
            
        except CalculationError as e:
            print(f"\n{ResultFormatter.format_error(str(e))}")
        except ValueError:
            print("\n[错误] 请输入整数")
    
    def _do_other(self) -> None:
        """其他运算"""
        print("\n【其他运算】")
        print("1. abs(x) - 绝对值")
        print("2. exp(x) - e的幂次方")
        
        choice = input("请选择: ").strip()
        
        try:
            if choice == '1':
                value = get_number_input("请输入值: ")
                result = self.calculator.abs(value)
                self.history.add_record(f"abs({value})", format_result(result))
            elif choice == '2':
                value = get_number_input("请输入指数: ")
                result = self.calculator.exp(value)
                self.history.add_record(f"exp({value})", format_result(result))
            else:
                print("无效选项")
                return
            
            print(f"\n计算结果: {format_result(result)}")
            
        except CalculationError as e:
            print(f"\n{ResultFormatter.format_error(str(e))}")
    
    def do_compatibility_mode(self) -> None:
        """兼容模式 - 类似旧版本交互"""
        print("\n【兼容模式 - 简易计算器】")
        print("输入格式: 数字1 运算符 数字2")
        print("支持的运算符: +, -, *, /")
        print("输入 'q' 返回主菜单")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n请输入表达式: ").strip()
                
                if user_input.lower() == 'q':
                    break
                
                is_valid, parsed, error = InputValidator.parse_expression(user_input)
                
                if not is_valid:
                    print(f"输入错误: {error}")
                    continue
                
                if len(parsed) == 3:
                    num1, op, num2 = parsed
                    result = self.calculator.calculate(num1, op, num2)
                    
                    expression = ResultFormatter.format_expression(num1, op, num2, result)
                    print(f"计算结果: {expression}")
                    
                    self.history.add_record(f"{num1} {op} {num2}", format_result(result))
                
            except CalculationError as e:
                print(f"计算错误: {e}")
            except KeyboardInterrupt:
                print("\n\n操作已取消")
                break
    
    def show_history(self) -> None:
        """显示历史记录"""
        print("\n【历史记录】")
        
        records = self.history.get_recent_records(20)
        
        if not records:
            print("暂无历史记录")
            return
        
        for i, record in enumerate(records, 1):
            print(ResultFormatter.format_history_record(i, f"{record.expression} = {record.result}", record.timestamp))
        
        print("-" * 50)
        print(f"共 {self.history.get_record_count()} 条记录")
        
        export = input("\n是否导出历史记录到文件? (y/n): ").strip().lower()
        if export == 'y':
            filename = input("请输入文件名 (默认: history_export.txt): ").strip()
            filename = filename or "history_export.txt"
            
            if self.history.export_to_file(filename):
                print(f"历史记录已导出到: {filename}")
            else:
                print("导出失败，请检查文件权限")
    
    def do_settings(self) -> None:
        """系统设置"""
        while True:
            self.show_settings_menu()
            
            choice = input("请选择设置项: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                current = self.config.get_angle_mode()
                new_mode = 'radian' if current == 'degree' else 'degree'
                if self.config.set_angle_mode(new_mode):
                    print(f"角度模式已切换为: {new_mode}")
                else:
                    print("切换失败")
            elif choice == '2':
                try:
                    places = int(input("请输入小数位数 (0-15): "))
                    if self.config.set_decimal_places(places):
                        print(f"小数位数已设置为: {places}")
                    else:
                        print("设置失败，请输入0-15之间的整数")
                except ValueError:
                    print("请输入有效整数")
            elif choice == '3':
                current = self.config.is_compatibility_mode()
                if self.config.set_compatibility_mode(not current):
                    print(f"兼容模式已{'开启' if not current else '关闭'}")
                else:
                    print("切换失败")
            elif choice == '4':
                confirm = input("确定要清空所有历史记录吗? (y/n): ").strip().lower()
                if confirm == 'y':
                    if self.history.clear_history():
                        print("历史记录已清空")
                    else:
                        print("清空失败")
            elif choice == '5':
                self.calculator.clear_cache()
                print("计算缓存已清空")
            elif choice == '6':
                confirm = input("确定要重置所有设置为默认值吗? (y/n): ").strip().lower()
                if confirm == 'y':
                    if self.config.reset_to_default():
                        print("设置已重置为默认值")
                    else:
                        print("重置失败")
            else:
                print("无效选项")
    
    def show_help(self) -> None:
        """显示帮助说明"""
        print("\n【帮助说明】")
        print("=" * 50)
        print("基础运算:")
        print("  支持 +, -, *, / 四则运算")
        print()
        print("科学运算:")
        print("  三角函数: sin, cos, tan")
        print("  反三角函数: asin, acos, atan")
        print("  对数: ln, log10, log(x, base)")
        print("  幂运算: x^y, sqrt(x)")
        print("  其他: factorial(n), abs(x), exp(x)")
        print()
        print("角度模式:")
        print("  degree - 角度制 (如 sin(30) = 0.5)")
        print("  radian - 弧度制 (如 sin(π/6) = 0.5)")
        print()
        print("兼容模式:")
        print("  开启后可使用旧版本输入方式")
        print("  格式: 数字1 运算符 数字2")
        print("=" * 50)
        
        input("\n按回车键返回...")
    
    def run(self) -> None:
        """运行计算器"""
        try:
            while self.running:
                self.show_header()
                
                if self.config.is_compatibility_mode():
                    self.do_compatibility_mode()
                else:
                    self.show_main_menu()
                    
                    choice = input("请选择功能: ").strip()
                    
                    if choice == '1':
                        self.do_basic_calculation()
                    elif choice == '2':
                        self.do_scientific_calculation()
                    elif choice == '3':
                        self.show_history()
                    elif choice == '4':
                        self.do_settings()
                    elif choice == '5':
                        self.show_help()
                    elif choice == '0':
                        self.running = False
                        print("\n感谢使用，再见！")
                    else:
                        print("无效选项，请重新选择")
                
                if self.running and not self.config.is_compatibility_mode():
                    input("\n按回车键继续...")
                    
        except KeyboardInterrupt:
            print("\n\n程序已退出")
        finally:
            self._cleanup()
    
    def _cleanup(self) -> None:
        """清理资源"""
        self.config.save_config()


def main():
    """程序入口"""
    app = CalculatorApp()
    app.run()


if __name__ == "__main__":
    main()
