import os
import base64
import socket
import yaml
import sys
import json

def process_data_files(data_dir, output_file):
    # 读取数据文件列表
    data_files = os.listdir(data_dir)

    merged_content = []

    # 遍历数据文件，逐个检测内容并处理
    for file in data_files:
        file_path = os.path.join(data_dir, file)
        with open(file_path, "r") as f:
            content = f.read()

            if file.endswith(".json"):
                # 如果是 JSON 文件，尝试将其转换为 V2Ray（Vmess）格式
                try:
                    json_data = json.loads(content)
                    v2ray_servers = convert_json_to_v2ray(json_data)
                    merged_content.extend(v2ray_servers)
                    print(f"Processed JSON file: {file}")
                    # os.remove(file_path)  # 删除原始文件
                except Exception as e:
                    print(f"Error processing JSON file {file}: {str(e)}")
            elif file.endswith(".yaml"):
                # 如果是 YAML 文件，尝试将其转换为 V2Ray（Vmess）格式
                try:
                    yaml_data = yaml.safe_load(content)
                    v2ray_servers = convert_yaml_to_v2ray(yaml_data)
                    merged_content.extend(v2ray_servers)
                    print(f"Processed YAML file: {file}")
                    # os.remove(file_path)  # 删除原始文件
                except Exception as e:
                    print(f"Error processing YAML file {file}: {str(e)}")
            elif file.endswith(".txt"):
                try:
                    # 尝试解密 Base64 编码的内容
                    decoded_content = base64.b64decode(content).decode()
                    merged_content.append(decoded_content)
                    print(f"Processed Base64 file: {file}")
                    # os.remove(file_path)  # 删除原始文件
                except Exception as e:
                    # 内容不是 Base64 编码，继续检测是否符合特定格式
                    if content.startswith("vmess://") or content.startswith("clash://") or content.startswith("ss://") or content.startswith("vlss://") or content.startswith("trojan://"):
                        merged_content.append(content)
                        print(f"Processed special format file: {file}")
                        # os.remove(file_path)  # 删除原始文件
                    else:
                        # 内容既不是 Base64 编码也不符合特定格式，删除该文件并打印错误信息
                        print(f"Error processing file {file}: Content is neither Base64 encoded nor has a special format.")
                        # os.remove(file_path)  # 删除不符合条件的文件
            else:
                print(f"Warning: Unknown file type for file {file}")

    # 保存合并后的内容到文件
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # 创建保存目录（如果不存在）
    with open(output_file, "w") as f:
        for content in merged_content:
            f.write(content + "\n")

# 通过命令行参数传递目录和保存文件名
data_dir = sys.argv[1]  # 第一个命令行参数为目录
output_file = sys.argv[2]  # 第二个命令行参数为保存文件名

# 处理数据文件
process_data_files(data_dir, output_file)
