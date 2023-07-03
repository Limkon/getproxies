import os
import requests
import threading
import random
import argparse

# 命令参数解析
parser = argparse.ArgumentParser(description='多线程爬虫')
parser.add_argument('url_file', type=str, help='网址列表文件路径')
parser.add_argument('save_directory', type=str, help='保存目录')
parser.add_argument('--num_threads', type=int, default=5, help='线程数量')
args = parser.parse_args()

# 网址列表文件路径
url_file = args.url_file

# 保存目录
save_directory = args.save_directory

# 线程数量
num_threads = args.num_threads

# 多个请求头，模拟多个浏览器
headers_list = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"
    },
    # 添加更多的请求头...
]

def save_page_content(url, headers):
    try:
        # 发送HTTP请求获取页面内容
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # 获取文件名
        file_name = os.path.basename(url)
        save_path = os.path.join(save_directory, file_name + '.txt')

        # 保存页面内容到文本文件
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text)

        print(f"已保存 {url} 的页面内容到 {save_path}")
    except Exception as e:
        print(f"获取 {url} 页面内容时发生错误：{str(e)}")

def crawl_urls(urls):
    for url in urls:
        headers = random.choice(headers_list)
        save_page_content(url, headers)

def main():
    # 创建保存目录
    os.makedirs(save_directory, exist_ok=True)

    # 从文件中读取网址列表
    with open(url_file, 'r') as file:
        urls = file.read().splitlines()

    # 计算每个线程需要处理的网址数量
    num_urls = len(urls)
    urls_per_thread = num_urls // num_threads

    # 创建线程并启动
    threads = []
    for i in range(num_threads):
        start_index = i * urls_per_thread
        end_index = start_index + urls_per_thread if i < num_threads - 1 else num_urls
        thread_urls = urls[start_index:end_index]

        thread = threading.Thread(target=crawl_urls, args=(thread_urls,))
        thread.start()
        threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("爬取完成")

if __name__ == "__main__":
    main()
