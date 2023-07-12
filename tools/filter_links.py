import sys

# 获取命令行参数中的文件名
input_file = sys.argv[1]

# 定义特定格式的链接前缀列表
valid_prefixes = ['vmess://', 'trojan://', 'clash://', 'ss://', 'vlss://']

# 读取输入文件并筛选出以特定格式开头的行
with open(input_file, 'r') as file:
    lines = file.readlines()
    total_lines = len(lines)

    valid_lines = [line for line in lines if any(line.startswith(prefix) for prefix in valid_prefixes)]
    valid_line_count = len(valid_lines)

# 将筛选后的行写回原文件
with open(input_file, 'w') as file:
    file.writelines(valid_lines)

# 输出筛选前和筛选后的行数
print(f"Total lines: {total_lines}")
print(f"Valid lines: {valid_line_count}")
