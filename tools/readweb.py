import os
import re
import sys
import time
import datetime
import random
import requests
import concurrent.futures
import logging
from bs4 import BeautifulSoup

# 设置日志记录
logging.basicConfig(filename='log.txt', level=logging.INFO)


def extract_content(url):
    try:
        headers = {
            'User-Agent': random_user_agent()  # 随机选择一个User-Agent
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # 检查请求是否成功
        soup = BeautifulSoup(response.text, 'html.parser')

        selectors = [
            '#app',
            '.content',
            'div',
            '.my-class',
            '#my-id',
            '[name="my-name"]',
            '.my-parent .my-child',
        ]

        for selector in selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text()
                    return content.strip()
            except Exception as e:
                logging.error(f"尝试通过选择器 {selector} 获取 {url} 内容失败：{str(e)}")

        logging.info(f"所有选择器都无法获取 {url} 的内容，将执行自定义代码")

        # 在此编写自定义的处理方法来选择和提取页面内容
        # 例如：提取页面的文本内容
        content = soup.get_text()
        return content.strip()

    except requests.exceptions.RequestException as e:
        logging.error(f"请求 {url} 发生异常：{str(e)}")
    except Exception as e:
        logging.error(f"处理 {url} 失败：{str(e)}")

    return None


def save_content(content, output_dir, url):
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    url_without_protocol = re.sub(r'^(https?://)', '', url)
    url_without_protocol = re.sub(r'[:?<>|\"*\r\n/]', '_', url_without_protocol)
    url_without_protocol = url_without_protocol[:20]
    file_name = os.path.join(output_dir, url_without_protocol + "_" + date + ".txt")
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    logging.info(f"网站 {url} 内容已保存至文件：{file_name}")


def process_url(url, output_dir):
    try:
        time.sleep(2)
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
            logging.info(result)


def random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        # 添加更多的 User-Agent
    ]
    return random.choice(user_agents)


def main():
    if len(sys.argv) != 4:
        print("请提供要抓取的 URL 列表文件名、保存提取内容的目录和线程数")
        print("示例: python extract_urls.py urls.txt data 10")
        sys.exit(1)

    urls_file = sys.argv[1]
    output_dir = sys.argv[2]
    num_threads = int(sys.argv[3])

    with open(urls_file, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file]

    process_urls(urls, output_dir, num_threads)

    print('所有网站内容保存完成！')


if __name__ == '__main__':
    main()
