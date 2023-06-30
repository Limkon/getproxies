import os
import re
import sys
import datetime
import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup


def extract_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()
        return content
    else:
        raise Exception(f"Failed to fetch content from URL: {url}")


def save_content(content, output_dir, url):
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    url_without_protocol = re.sub(r'^(https?://)', '', url)
    file_name = os.path.join(output_dir, re.sub(r'[:?<>|\"*\r\n/]', '_', url_without_protocol) + "_" + date + ".txt")
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"网站 {url} 内容已保存至文件：{file_name}")


def process_url(url, output_dir):
    try:
        content = extract_content(url)
        save_content(content, output_dir, url)
    except Exception as e:
        print(f"处理 {url} 失败：{str(e)}")


def process_urls(urls, output_dir):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_url, url, output_dir) for url in urls]
        for future in futures:
            future.result()


def main():
    if len(sys.argv) != 3:
        print("请提供要抓取的 URL 列表文件名和保存提取内容的目录")
        print("示例: python extract_urls.py urls.txt data")
        sys.exit(1)

    urls_file = sys.argv[1]  # 存储要抓取的 URL 列表的文件名
    output_dir = sys.argv[2]  # 保存提取内容的目录

    with open(urls_file, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file]

    process_urls(urls, output_dir)

    print('所有网站内容保存完成！')


if __name__ == '__main__':
    main()
