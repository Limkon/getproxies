import sys
import os
import tempfile
import shutil

# 获取命令行参数中的文件名
input_file = sys.argv[1]

# 定义特定格式的链接前缀列表
valid_prefixes = ['vmess://', 'trojan://', 'clash://', 'ss://', 'vlss://']

# 读取输入文件并筛选出以特定格式开头的行
with open(input_file, 'r') as file:
    lines = file.readlines()
    valid_lines = [line for line in lines if any(line.startswith(prefix) for prefix in valid_prefixes)]

# 创建临时文件来保存筛选后的内容
temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
temp_file.writelines(valid_lines)
temp_file.close()

# 删除原始文件
os.remove(input_file)

# 将临时文件重命名为原始文件名
shutil.move(temp_file.name, input_file)

# 输出处理完成的消息
print("File processing completed.")
