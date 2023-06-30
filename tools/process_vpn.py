import os
import re
import json
import yaml
import base64
import sys

def convert_to_vmess(json_data):
    # 编写将 JSON 数据转换为 V2Ray（Vmess）格式的代码
    # 返回转换后的 V2Ray（Vmess）链接
    vmess_link = ''  # 定义变量
    return vmess_link

def convert_to_vmess(yaml_data):
    # 编写将 YAML 数据转换为 V2Ray（Vmess）格式的代码
    # 返回转换后的 V2Ray（Vmess）链接
    vmess_link = ''  # 定义变量
    return vmess_link

def decode_base64(encoded_data):
    # 解密 Base64 编码的内容的代码
    # 返回解密后的内容
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    return decoded_data

def extract_links(content):
    # 使用正则表达式提取特定格式的链接
    formats = ['vmess://', 'trojan://', 'clash://', 'ss://', 'vlss://']
    links = re.findall(r'(' + '|'.join(formats) + r')[^\s]+', content)
    return links

def process_file(file_path, rest_urls_file):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 尝试将 JSON 数据转换为 V2Ray（Vmess）格式
    try:
        json_data = json.loads(content)
        vmess_link = convert_to_vmess(json_data)
        with open(rest_urls_file, 'a', encoding='utf-8') as file:
            file.write(vmess_link + '\n')
        return
    except json.JSONDecodeError:
        pass

    # 尝试将 YAML 数据转换为 V2Ray（Vmess）格式
    try:
        yaml_data = yaml.safe_load(content)
        vmess_link = convert_to_vmess(yaml_data)
        with open(rest_urls_file, 'a', encoding='utf-8') as file:
            file.write(vmess_link + '\n')
        return
    except yaml.YAMLError:
        pass

    # 尝试解密 Base64 编码的内容
    try:
        decoded_data = decode_base64(content)
        with open(rest_urls_file, 'a', encoding='utf-8') as file:
            file.write(decoded_data + '\n')
        return
    except:
        pass

    # 提取特定格式的链接
    links = extract_links(content)

    # 保存链接到 rest_urls 文件中
    with open(rest_urls_file, 'a', encoding='utf-8') as file:
        for link in links:
            file.write(link + '\n')

def process_files_in_directory(directory, rest_urls_file):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            process_file(file_path, rest_urls_file)

def main(data_directory, rest_urls_file):
    with open(rest_urls_file, 'w', encoding='utf-8') as file:
        pass

    process_files_in_directory(data_directory, rest_urls_file)

    print('处理完成！')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("请提供数据目录和 rest_urls 文件路径作为参数")
        print("示例: python process_data.py data rest_urls.txt")
        sys.exit(1)

    data_directory = sys.argv[1]
    rest_urls_file = sys.argv[2]

    main(data_directory, rest_urls_file)
