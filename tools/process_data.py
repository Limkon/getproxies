import os
import re
import json
import yaml
import base64
import sys

def is_yaml(content):
    try:
        yaml.safe_load(content)
        return True
    except yaml.YAMLError:
        return False

def is_json(content):
    try:
        json.loads(content)
        return True
    except ValueError:
        return False

def has_specific_format(content):
    formats = ['vmess://', 'trojan://', 'clash://', 'ss://', 'vlss://']
    return any(format in content for format in formats)

def is_base64_encoded(content):
    try:
        content.encode('ascii')  # 转换为ASCII编码
        base64.b64decode(content)
        return True
    except (UnicodeEncodeError, base64.binascii.Error):
        return False

def extract_links(content):
    # 使用正则表达式提取链接
    links = re.findall(r'https?://\S+', content)
    return links

def process_file(file_path, rest_urls_file):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    if has_specific_format(content):
        # 保留特定格式文件并提取链接
        links = extract_links(content)
        if links:
            with open(rest_urls_file, 'a', encoding='utf-8') as file:
                for link in links:
                    file.write(link + '\n')
        return

    if is_yaml(content):
        # 保留 YAML 文件
        return

    if is_json(content):
        # 保留 JSON 文件
        return

    if is_base64_encoded(content):
        # 保留 BASE64 编码文件
        return

    # 删除原始文件
    os.remove(file_path)

def process_files_in_directory(directory, rest_urls_file):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            process_file(file_path, rest_urls_file)

def main(data_directory, rest_urls_file):
    process_files_in_directory(data_directory, rest_urls_file)

    print('处理完成！')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("请提供数据目录和rest_urls文件路径作为参数")
        print("示例: python process_data.py data rest_urls.txt")
        sys.exit(1)

    data_directory = sys.argv[1]
    rest_urls_file = sys.argv[2]

    main(data_directory, rest_urls_file)
