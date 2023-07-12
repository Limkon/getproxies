import fileinput
import sys

# 获取命令行参数中的文件名
input_file = sys.argv[1]

# 定义特定格式的链接前缀列表
valid_prefixes = ['vmess://', 'trojan://', 'clash://', 'ss://', 'vlss://']

# 备份原始文件
backup_file = input_file + ".bak"
with open(input_file, 'r') as file, open(backup_file, 'w') as backup:
    backup.writelines(file.readlines())

# 删除不以特定格式开头的行并保存回原始文件
with fileinput.FileInput(input_file, inplace=True) as file:
    for line in file:
        if any(line.startswith(prefix) for prefix in valid_prefixes):
            print(line, end='')

# 输出处理完成的消息
print("File processing completed.")
