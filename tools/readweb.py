import os
import re
import sys
import time
import datetime
import requests
import concurrent.futures

from bs4 import BeautifulSoup


def extract_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 尝试不同的选择器
        selectors = [
            '#app',                 # ID 选择器
            '.content',             # 类选择器
            'div',                  # 元素选择器
            '.my-class',            # 类选择器
            '#my-id',               # ID 选择器
            '[name="my-name"]',     # 属性选择器
            '.my-parent .my-child', # 后代选择器
        ]

        for selector in selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text()
                    return content
            except Exception as e:
                print(f"尝试通过选择器 {selector} 获取 {url} 内容失败：{str(e)}")

        # 如果所有选择器都失败，则执行自定义的处理方法
        print(f"所有选择器都无法获取 {url} 的内容，将执行自定义代码")

        # 在此编写自定义的处理方法来选择和提取页面内容
        # 例如：提取页面的文本内容
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
        if content:
            save_content(content, output_dir, url)
            return f"处理 {url} 成功"
        else:
            return f"处理 {url} 失败：无法提取内容"
    except Exception as e:
        return f"处理 {url} 失败：{str(e)}"


def process_urls(urls, output_dir, num_threads):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_url, url, output_dir) for url in urls]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(result)


def main():
    if len(sys.argv) != 4:
        print("请提供要抓取的 URL 列表文件名、保存提取内容的目录和线程数")
        print("示例: python extract_urls.py urls.txt data 10")
        sys.exit(1)

    urls_file = sys.argv[1]  # 存储要抓取的 URL 列表的文件名
    output_dir = sys.argv[2]  # 保存提取内容的目录
    num_threads = int(sys.argv[3])  # 线程数

    with open(urls_file, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file]

    process_urls(urls, output_dir, num_threads)

    print('所有网站内容保存完成！')


if __name__ == '__main__':
    main()
