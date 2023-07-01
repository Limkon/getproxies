import os
import base64
import yaml
import sys
import json
import magic

def get_file_type(file_path):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    return file_type

def process_data_files(data_dir, output_dir, rest_file):
    # 创建保存目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    rest_content = []

    # 遍历数据文件，逐个检测内容并处理
    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        with open(file_path, "r") as f:
            content = f.read()

            file_type = get_file_type(file_path)
            if file_type == 'application/json':
                # 将文件移到指定目录并将后缀名改为 .json
                new_file_path = os.path.join(output_dir, file + ".json")
                os.rename(file_path, new_file_path)
                print(f"Moved JSON file: {file}")

            elif file_type == 'text/plain' or file_type == 'application/x-yaml':
                # 将文件移到指定目录并将后缀名改为 .yaml
                new_file_path = os.path.join(output_dir, file + ".yaml")
                os.rename(file_path, new_file_path)
                print(f"Moved YAML file: {file}")

            elif file_type == 'application/octet-stream':
                try:
                    # 尝试解密 Base64 编码的内容
                    decoded_content = base64.b64decode(content).decode()

                    # 将解密后的内容追加保存到 rest.txt 文件中
                    rest_content.append(decoded_content)

                    print(f"Processed Base64 file: {file}")
                except Exception as e:
                    # 内容不是 Base64 编码，继续检测是否符合特定格式
                    if content.startswith(("vmess://", "clash://", "ss://", "vlss://", "trojan://")):
                        # 将特定格式的内容追加保存到 rest.txt 文件中
                        rest_content.append(content)

                        print(f"Processed special format file: {file}")
                    else:
                        # 内容既不是 Base64 编码也不符合特定格式，打印错误信息
                        print(f"Error processing file {file}: Content is neither Base64 encoded nor has a special format.")

            else:
                print(f"Warning: Unknown file type for file {file}")

    # 将 rest.txt 文件保存到指定目录
    with open(rest_file, "a") as rest:
        for content in rest_content:
            rest.write(content + "\n")

# 通过命令行参数传递目录和保存目录
if len(sys.argv) < 4:
    print("Usage: python convert.py <data_directory> <output_directory> <rest_file>")
    sys.exit(1)

data_dir = sys.argv[1]  # 第一个命令行参数为目录
output_dir = sys.argv[2]  # 第二个命令行参数为保存目录
rest_file = sys.argv[3]  # 第三个命令行参数为保存的 rest.txt 文件名

# 处理数据文件
process_data_files(data_dir, output_dir, rest_file)
