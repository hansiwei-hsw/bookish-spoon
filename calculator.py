def get_number(prompt):
    """获取用户输入的数字"""
    while True:
        try:
            num = float(input(prompt))
            return num
        except ValueError:
            print("输入错误，请输入有效的数字！")


def get_operator():
    """获取用户输入的运算符"""
    while True:
        op = input("请输入运算符号（+、-、*、/）：")
        if op in ['+', '-', '*', '/']:
            return op
        print("输入错误，请输入有效的运算符号（+、-、*、/）！")


def calculate(num1, op, num2):
    """执行计算操作"""
    if op == '+':
        return num1 + num2
    elif op == '-':
        return num1 - num2
    elif op == '*':
        return num1 * num2
    elif op == '/':
        if num2 == 0:
            raise ZeroDivisionError("除数不能为0！")
        return num1 / num2


def main():
    """主函数，程序的入口点"""
    print("=" * 30)
    print("       简易计算器")
    print("=" * 30)

    # 获取用户输入
    num1 = get_number("请输入第一个数字：")
    op = get_operator()
    num2 = get_number("请输入第二个数字：")

    try:
        # 执行计算
        result = calculate(num1, op, num2)
        # 如果结果是整数，转换为整型
        if result == int(result):
            result = int(result)
        if num1 == int(num1):
            num1 = int(num1)
        if num2 == int(num2):
            num2 = int(num2)
        print(f"计算结果：{num1} {op} {num2} = {result}")
    except ZeroDivisionError as e:
        print(f"计算错误：{e}")


if __name__ == "__main__":
    main()
