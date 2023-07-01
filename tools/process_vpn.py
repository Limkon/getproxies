import os
import json
import yaml
import base64

def convert_json_to_v2ray(json_data):
    v2ray_servers = []
    # 编写将 JSON 数据转换为 V2Ray（Vmess）格式的逻辑
    # 将转换后的 V2Ray（Vmess）链接添加到 v2ray_servers 列表中
    return v2ray_servers

def convert_yaml_to_v2ray(yaml_data):
    v2ray_servers = []
    # 编写将 YAML 数据转换为 V2Ray（Vmess）格式的逻辑
    # 将转换后的 V2Ray（Vmess）链接添加到 v2ray_servers 列表中
    return v2ray_servers

def process_file(file_path, merged_content):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    if file_path.endswith(".json"):
        try:
            json_data = json.loads(content)
            v2ray_servers = convert_json_to_v2ray(json_data)
            merged_content.extend(v2ray_servers)
        except Exception as e:
            print(f"Error processing JSON file {file_path}: {str(e)}")
    elif file_path.endswith(".yaml"):
        try:
            yaml_data = yaml.safe_load(content)
            v2ray_servers = convert_yaml_to_v2ray(yaml_data)
            merged_content.extend(v2ray_servers)
        except Exception as e:
            print(f"Error processing YAML file {file_path}: {str(e)}")
    elif file_path.endswith(".txt"):
        try:
            decoded_content = base64.b64decode(content).decode()
            merged_content.append(decoded_content)
        except Exception as e:
            print(f"Error decoding Base64 content in file {file_path}: {str(e)}")

def process_files_in_directory(directory):
    merged_content = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            process_file(file_path, merged_content)
    return merged_content

def main(data_directory, rest_urls_file):
    merged_content = process_files_in_directory(data_directory)
    # 执行后续操作，如保存到文件或进行其他处理

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("请提供数据目录和 rest_urls 文件路径作为参数")
        print("示例: python process_data.py data rest_urls.txt")
        sys.exit(1)

    data_directory = sys.argv[1]
    rest_urls_file = sys.argv[2]
    
    main(data_directory, rest_urls_file)
