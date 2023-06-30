import os
import re
import sys
import time
import datetime
import requests
import concurrent.futures
import base64
import json
import yaml

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def extract_content(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无界面模式
    chrome_service = Service('/path/to/chromedriver')  # 指定 chromedriver 路径
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    driver.get(url)
    time.sleep(5)  # 等待页面加载完成，根据需要调整等待时间

    content = ''

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
            element = driver.find_element(By.CSS_SELECTOR, selector)
            content = element.get_attribute('innerText')
            if content:
                break
        except Exception as e:
            print(f"尝试通过选择器 {selector} 获取 {url} 内容失败：{str(e)}")

    driver.quit()
    return content


def save_content(content, output_dir, url):
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    url_without_protocol = re.sub(r'^(https?://)', '', url)
    file_name = os.path.join(output_dir, re.sub(r'[:?<>|\"*\r\n/]', '_', url_without_protocol) + "_" + date + ".txt")
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"网站 {url} 内容已保存至文件：{file_name}")
    return file_name


def process_url(url, output_dir, rest_urls_file):
    try:
        content = extract_content(url)
        if is_yaml(content):
            file_name = save_content(content, output_dir, url)
            return f"处理 {url} 成功", file_name
        elif is_json(content):
            file_name = save_content(content, output_dir, url)
            return f"处理 {url} 成功", file_name
        elif has_specific_format(content):
            file_name = save_content(content, output_dir, url)
            return f"处理 {url} 成功", file_name
        elif is_base64_encoded(content):
            file_name = save_content(content, output_dir, url)
            return f"处理 {url} 成功", file_name
        else:
            extracted_urls = extract_links(content)
            save_links(extracted_urls, rest_urls_file)
            return f"处理 {url} 成功", None
    except Exception as e:
        return f"处理 {url} 失败：{str(e)}", None

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
        base64.b64decode(content)
        return True
    except base64.binascii.Error:
        return False


def extract_links(content):
    # 在此编写提取链接的代码
    # 返回提取到的链接列表
    links = re.findall(r'(https?://\S+)', content)
    return links


def save_links(urls, rest_urls_file):
    with open(rest_urls_file, 'a', encoding='utf-8') as file:
        for url in urls:
            file.write(url + '\n')


def process_urls(urls, output_dir, num_threads, rest_urls_file):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_url, url, output_dir, rest_urls_file) for url in urls]

        for future in concurrent.futures.as_completed(futures):
            result, file_name = future.result()
            print(result)
            if file_name:
                os.remove(file_name)


def main():
    if len(sys.argv) != 5:
        print("请提供要抓取的 URL 列表文件名、保存提取内容的目录、线程数和剩余 URL 文件名")
        print("示例: python extract_urls.py urls.txt data 10 rest_urls.txt")
        sys.exit(1)

    urls_file = sys.argv[1]  # 存储要抓取的 URL 列表的文件名
    output_dir = sys.argv[2]  # 保存提取内容的目录
    num_threads = int(sys.argv[3])  # 线程数
    rest_urls_file = sys.argv[4]  # 剩余 URL 文件名

    with open(urls_file, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file]

    process_urls(urls, output_dir, num_threads, rest_urls_file)

    print('所有网站内容保存完成！')


if __name__ == '__main__':
    main()
