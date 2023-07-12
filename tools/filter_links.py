import sys

# 获取命令行参数中的文件名
input_file = sys.argv[1]

# 定义特定格式的链接前缀列表
valid_prefixes = ['vmess://', 'trojan://', 'clash://', 'ss://', 'vlss://']

# 读取输入文件并筛选出符合特定格式的链接行
with open(input_file, 'r') as file:
    lines = file.readlines()
    valid_lines = [line.strip() for line in lines if line.strip().startswith(tuple(valid_prefixes))]

# 将筛选后的链接行写回原文件
with open(input_file, 'w') as file:
    file.writelines(valid_lines)
