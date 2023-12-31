import os
import sys
import re

def remove_non_alphanumeric_urls(filename):
    lines_to_keep = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()

            # 检查行是否以字母或数字结尾，但保留以斜杠 "/" 结尾的网址
            if re.match(r'^.*[a-zA-Z0-9/]+$', line):
                # 查找中文字符的位置
                chinese_index = re.search(r'[\u4e00-\u9fff]', line)
                if chinese_index:
                    # 只保留中文字符前的部分
                    line = line[:chinese_index.start()]

                lines_to_keep.append(line)

    # 将结果写回原文件
    with open(filename, 'w') as file:
        file.write('\n'.join(lines_to_keep))

    print("已剔除不以字母或数字结尾（除斜杠“/”外）的网址，并删除中文字符及其后面的内容。")

# 获取命令行参数
if len(sys.argv) != 2:
    print("Usage: python remove_non_alphanumeric_urls.py <filename>")
else:
    filename = sys.argv[1]  # 获取文件名参数
    remove_non_alphanumeric_urls(filename)  # 调用剔除函数，传入文件名参数
