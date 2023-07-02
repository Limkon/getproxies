import os
import re
import base64
import sys

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

def process_file(file_path, rest_txt_file, rest_urls_file):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    if is_base64_encoded(content):
        # BASE64编码文件，解码并将内容追加到rest.txt文件
        decoded_content = base64.b64decode(content).decode('utf-8')
        with open(rest_txt_file, 'a', encoding='utf-8') as file:
            file.write(decoded_content + '\n')

    else:
        # 检测特定格式
        lines = content.split('\n')
        first_line = lines[0]
        if first_line.startswith(('vmess://', 'trojan://', 'clash://', 'ss://', 'vlss://')):
            # 特定格式文件，将内容追加到rest.txt文件
            with open(rest_txt_file, 'a', encoding='utf-8') as file:
                file.write(content + '\n')
        else:
            # 提取链接并追加到rest_urls文件中
            links = extract_links(content)
            if links:
                with open(rest_urls_file, 'a', encoding='utf-8') as file:
                    for link in links:
                        file.write(link + '\n')

def process_files_in_directory(directory, rest_txt_file, rest_urls_file):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            process_file(file_path, rest_txt_file, rest_urls_file)

def main(data_directory, rest_txt_file, rest_urls_file):
    process_files_in_directory(data_directory, rest_txt_file, rest_urls_file)

    print('处理完成！')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("请提供数据目录、rest.txt文件路径和rest_urls文件路径作为参数")
        print("示例: python process_data.py data rest.txt rest_urls.txt")
        sys.exit(1)

    data_directory = sys.argv[1]
    rest_txt_file = sys.argv[2]
    rest_urls_file = sys.argv[3]

    main(data_directory, rest_txt_file, rest_urls_file)
