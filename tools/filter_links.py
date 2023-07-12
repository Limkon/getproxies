import sys
import os
import tempfile
import shutil

# 获取命令行参数中的文件名
input_file = sys.argv[1]

# 定义特定格式的链接前缀列表
valid_prefixes = ['vmess://', 'trojan://', 'clash://', 'ss://', 'vlss://']

# 创建临时文件来保存更改后的内容
temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

# 读取输入文件并筛选出以特定格式开头的行，并将结果写入临时文件
with open(input_file, 'r') as file:
    lines = file.readlines()
    valid_lines = [line for line in lines if any(line.startswith(prefix) for prefix in valid_prefixes)]
    temp_file.write(''.join(valid_lines))

# 关闭临时文件
temp_file.close()

# 将临时文件复制回原始文件
shutil.move(temp_file.name, input_file)
