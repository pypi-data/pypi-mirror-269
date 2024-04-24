"""
@Author: shuangchen
@Time: 2024/3/12
@File: transform.py
@Description: 各类转换工具函数
"""


def numeral2chinese(number: int) -> str:
    """
    阿拉伯数字转中文表达
    :param number: 待转换的数字
    """
    if number > 99999:
        raise ValueError('数字最大99999')
    num_dict = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 0: '零'}
    digit_dict = {1: '十', 2: '百', 3: '千', 4: '万'}

    def max_digit(number, count):
        num = number // 10  # 整除
        if num != 0:
            return max_digit(num, count + 1)
        else:
            digit_num = number % 10  # digit_num是最高位上的数字
            return count, digit_num  # count记录最高位

    max_digit, digit_num = max_digit(number, 0)

    temp = number
    num_list = []  # 储存各位数字（最高位的数字也可以通过num_list[-1]得到
    while temp > 0:
        position = temp % 10
        temp //= 10  # 整除是//
        num_list.append(position)

    chinese = ""
    if max_digit == 0:  # 个位数
        chinese = num_dict[number]
    elif max_digit == 1:  # 十位数
        if digit_num == 1:  # 若十位上是1，则称为“十几”，而一般不称为“一十几”（与超过2位的数分开讨论的原因）
            chinese = "十" + num_dict[num_list[0]]
        else:
            chinese = num_dict[num_list[-1]] + "十" + num_dict[num_list[0]]
    elif max_digit > 1:  # 超过2位的数
        while max_digit > 0:
            if num_list[-1] != 0:  # 若当前位上数字不为0，则加上位称
                chinese += num_dict[num_list[-1]] + digit_dict[max_digit]
                max_digit -= 1
                num_list.pop(-1)
            else:  # 若当前位上数字为0，则不加上位称
                chinese += num_dict[num_list[-1]]
                max_digit -= 1
                num_list.pop(-1)
        chinese += num_dict[num_list[-1]]

    while chinese.endswith("零") and len(chinese) > 1:  # 个位数如果为0，不读出
        chinese = chinese[:-1]
    if chinese.count("零") > 1:  # 中文数字中最多只有1个零
        count_0 = chinese.count("零")
        chinese = chinese.replace("零", "", count_0 - 1)
    return chinese


def numeral2roman(number: int) -> str:
    """
    阿拉伯数字转罗马数字表达
    :param number: 待转换的数字
    """
    num_list = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    str_list = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman = ''
    for i in range(len(num_list)):
        while number >= num_list[i]:
            number -= num_list[i]
            roman += str_list[i]
    return roman


def roman2numeral(roman: str) -> int:
    """
    罗马数字转阿拉伯数字
    :param roman: 待转换的数字
    """
    define_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if roman == '0':
        return 0
    else:
        res = 0
        for i in range(0, len(roman)):
            if i == 0 or define_dict[roman[i]] <= define_dict[roman[i - 1]]:
                res += define_dict[roman[i]]
            else:
                res += define_dict[roman[i]] - 2 * define_dict[roman[i - 1]]
        return res
