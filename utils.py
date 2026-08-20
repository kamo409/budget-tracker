"""
utils.py
工具函数
"""


def colored(text, color):
    """给文字上色"""
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m",
    }
    c = colors.get(color, "")
    r = colors["reset"]
    return c + text + r


def input_float(prompt):
    """输入金额，必须大于0"""
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("金额必须大于0")
        except:
            print("请输入数字")


def print_divider():
    """打印分隔线"""
    print("-" * 50)