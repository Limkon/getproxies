import os
import re
import sys
import time
import datetime
import requests
import concurrent.futures
import base64

from bs4 import BeautifulSoup


def extract_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()
        return content
    else:
        raise Exception(f"Failed to fetch content from URL: {url}")


def save_content(content, output_dir, url, file_name):
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content + '\n')
    print(f"网站 {url} 内容已保存至文件：{file_path}")


def process_url(url, output_dir, file_name):
    try:
        time.sleep(2)  # 等待页面加载
        content = extract_content(url)
        if content:
            if re.match(r'^(vmess://|clash://|ss://|vlss://|trojan://)', content.strip()):
                save_content(content, output_dir, url, file_name)
            else:
                try:
                    decoded_content = base64.b64decode(content).decode('utf-8')
                    if re.match(r'^(vmess://|clash://|ss://|vlss://|trojan://)', decoded_content.strip()):
                        save_content(decoded_content, output_dir, url, file_name)
                except Exception:
                    pass
        return f"处理 {url} 完成"
    except Exception as e:
        return f"处理 {url} 失败：{str(e)}"


def process_urls(urls, output_dir, file_name, num_threads):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_url, url, output_dir, file_name) for url in urls]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(result)


def main():
    if len(sys.argv) != 5:
        print("请提供要抓取的 URL 列表文件名、保存提取内容的目录、文件名和线程数")
        print("示例: python extract_urls.py urls.txt data output.txt 10")
        sys.exit(1)

    urls_file = sys.argv[1]  # 存储要抓取的 URL 列表的文件名
    output_dir = sys.argv[2]  # 保存提取内容的目录
    file_name = sys.argv[3]   # 保存内容的文件名
    num_threads = int(sys.argv[4])  # 线程数

    with open(urls_file, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file]

    process_urls(urls, output_dir, file_name, num_threads)

    print('所有网站内容保存完成！')


if __name__ == '__main__':
    main()
