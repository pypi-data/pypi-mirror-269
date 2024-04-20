"""
time: 2024-02-19
处于大三的寒假, 正在看张宇的考研数学, 空余时间复现的泰勒展开式近似重要函数, 以及书上涉及的一些重要函数
参考书籍《张宇考研数学基础30讲》 P-27 (2025版)
"""
import math
import pyzjr.Math.constant as const
from pyzjr.Math.arithmetic import odd_factorial, even_factorial

__all__ = ["cos", "sin", "tan", "cot", "sec", "csc", "arcsin", "arccos", "arctan", "angle_to_2pi",
           "to_degree", "to_radians", "exp", "log_e", "sinh", "arsinh", "cosh", "arcosh",
           "sigmoid", "tanh", "artanh", "relu", "taylor_sin", "taylor_cos", "taylor_arcsin",
           "taylor_tan", "taylor_arctan", "taylor_log_1_plus_x", "taylor_exp",
           "taylor_series_1_plus_x_to_a"]

def cos(x):
    """弧度制 cos"""
    return math.cos(x)

def sin(x):
    """弧度制 sin"""
    return math.sin(x)

def tan(x):
    """弧度制 tan"""
    return math.tan(x)

def cot(x):
    tan_value = tan(x)
    if tan_value == 0:
        raise ValueError("cot(x) is undefined when tan(x) is zero.")
    return 1 / tan_value

def sec(x):
    """弧度制 sec"""
    cos_value = cos(x)
    if cos_value == 0:
        raise ValueError("sec(x) is undefined when cos(x) is zero.")
    return 1 / cos_value

def csc(x):
    """弧度制 csc"""
    sin_value = sin(x)
    if sin_value == 0:
        raise ValueError("csc(x) is undefined when sin(x) is zero.")
    return 1 / sin_value

def arccos(x):
    """计算反正弦值"""
    return math.acos(x)

def arcsin(x):
    """计算反正弦值"""
    return math.asin(x)

def arctan(x):
    """计算反正弦值"""
    return math.atan(x)

def angle_to_2pi(angle):
    """将角度映射到0到2π"""
    two_pi = 2 * const.pi
    return angle % two_pi

def to_degree(radians_value):
    """弧度转度数"""
    return math.degrees(radians_value)

def to_radians(angle_degrees):
    """度数转弧度"""
    return math.radians(angle_degrees)

def exp(x):
    """计算以e为底的指数函数值"""
    return (const.e) ** x

def log_e(x):
    """计算以e为底的对数函数值"""
    return math.log(x)

def sinh(x):
    """双曲正弦函数"""
    return (exp(x) - exp(-x)) / 2

def arsinh(x):
    """反双曲正弦函数"""
    return log_e(x + math.sqrt(x**2 + 1))

def cosh(x):
    """双曲余弦函数"""
    return (exp(x) + exp(-x)) / 2

def arcosh(x):
    """反双曲余弦函数"""
    return log_e(x + math.sqrt(x**2 - 1))

def tanh(x):
    """双曲正切函数"""
    return (exp(x) - exp(-x)) / (exp(x) + exp(-x))

def artanh(x):
    """反双曲正切函数"""
    return 0.5 * log_e((1+x) / (1-x))

def sigmoid(x):
    """Sigmoid 函数"""
    return 1 / (1 + exp(-x))

def relu(x):
    """ReLU 激活函数"""
    return max(0, x)

def taylor_exp(x, n):
    """泰勒近似 exp
    Example:
        approximation = taylor_exp(2, 20)
        exact_value = math.exp(2)
        print("Approximation:", approximation)
        print("Exact Value:", exact_value)
    """
    result = 0
    for i in range(n):
        result += (x ** i) / math.factorial(i)
    return result


def taylor_sin(x, n):
    """泰勒近似 sin
    Example:
        angle_degrees = 30
        angle_radians = math.radians(angle_degrees)
        approximation = taylor_sin(angle_radians, 5)
        exact_value = math.sin(angle_radians)
        print("Approximation:", approximation)
        print("Exact Value:", exact_value)
    """
    result = 0
    for i in range(n):
        term = ((-1) ** i) * (x ** (2*i + 1)) / math.factorial(2*i + 1)
        result += term
    return result


def taylor_cos(x, n):
    """泰勒近似 cos
    Example:
        angle_degrees = 60
        angle_radians = math.radians(angle_degrees)
        approximation = taylor_cos(angle_radians, 5)
        exact_value = math.cos(angle_radians)
        print("Approximation:", approximation)
        print("Exact Value:", exact_value)
    """
    result = 1
    for i in range(1, n):
        term = ((-1) ** i) * (x ** (2*i)) / math.factorial(2*i)
        result += term
    return result

def taylor_tan(x, n):
    """泰勒近似 tan
    因为分子分母无规律，这里只提供了前24项
    Example:
        angle_degrees = 45
        angle_radians = math.radians(angle_degrees)
        approximation = taylor_tan(angle_radians, 24)
        exact_value = math.tan(angle_radians)
        print("Approximation:", approximation)
        print("Exact Value:", exact_value)
    """
    # 从 1 - 23 奇数项系数
    coefficients = [1, 1/3, 2/15, 17/315, 62/2835, 1382/155925, 21844/6081075, 929569/638512875,
                    6404582/10854718875, 443861162/1856156927625, 18888466084/194896477400625,
                    113927491862/49308808782358125]
    result = 0
    iter = 0
    for i in range(n):
        if i <= 24 and i % 2 == 1:
            coefficient = coefficients[iter]
            iter += 1
            term = coefficient * (x ** i)
            result += term
    return result

def taylor_log_1_plus_x(x, n):
    """泰勒展开 In(1+x)
    Example:
        approximation = taylor_log_1_plus_x(0.5, 10)
        exact_value = math.log1p(0.5)
        print("Approximation:", approximation)
        print("Exact Value:", exact_value)
    """
    result = 0
    for i in range(1, n + 1):
        term = ((-1)**(i-1) * x**i) / i
        result += term
    return result

def taylor_arcsin(x, n):
    """泰勒展开 arcsinx
    x 属于 (-1, 1)
    Example:
        approximation = taylor_arcsin(0.5, 10)
        exact_value = math.asin(0.5)
        print("Approximation:", approximation)
        print("Exact Value:", exact_value)
    """
    if abs(x) > 1:
        raise ValueError("Input x must be between -1 and 1 for arcsin(x)")

    result = x
    for i in range(1, n+1):
        odd = 2 * i + 1
        term = ((x ** odd) / odd) * (odd_factorial(i) / even_factorial(i))
        result += term

    return result

def taylor_arctan(x, n):
    """泰勒展开 arctan(x)
    x 属于 (-1, 1)
    Example:
        approximation = taylor_arctan(0.5, 10)
        exact_value = math.atan(0.5)
        print("Approximation:", approximation)
        print("Exact Value:", exact_value)
    """
    if abs(x) > 1:
        raise ValueError("Input x must be between -1 and 1 for arctan(x)")

    result = 0
    for i in range(n):
        term = ((-1)**i * x**(2 * i + 1)) / (2 * i + 1)
        result += term

    return result

def taylor_series_1_plus_x_to_a(x, a, n):
    """(1+x)^a 的泰勒展开
    a 整数近似才比较相近, 用浮点数需要四舍五入
    Example:
        a = 3
        approximation = taylor_series_1_plus_x_to_a(0.5, a, 10)
        exact_value = (1 + 0.5) ** a
        print(f"Approximation: {approximation}, Exact Value: {exact_value}")
    """
    def binomial_coefficient(a, n):
        a = round(a)
        if n < 0 or n > a:
            return 0
        return math.factorial(a) // (math.factorial(n) * math.factorial(a - n))
    result = 0
    for i in range(n + 1):
        term = binomial_coefficient(a, i) * x**i
        result += term
    return result

