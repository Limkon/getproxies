import os
import re
import sys
import asyncio
import datetime
import httpx

from bs4 import BeautifulSoup
from httpx import Timeout

import httpx
import asyncio

from bs4 import BeautifulSoup


async def extract_content(url):
    async with httpx.AsyncClient(timeout=Timeout(5.0)) as client:
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 在此编写自定义的处理方法来选择和提取页面内容
            # 例如：提取页面的文本内容
            content = soup.get_text()
            return content
        else:
            raise Exception(f"Failed to fetch content from URL: {url}")


def save_content(content, output_dir, url):
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    url_without_protocol = re.sub(r'^(https?://)', '', url)
    url_without_protocol = re.sub(r'[:?<>|\"*\r\n/]', '_', url_without_protocol)
    url_without_protocol = url_without_protocol[:20]  # 限制文件名长度不超过20个字符
    file_name = os.path.join(output_dir, url_without_protocol + "_" + date + ".txt")

    # 删除空白行
    content_lines = content.splitlines()
    non_empty_lines = [line for line in content_lines if line.strip()]
    cleaned_content = '\n'.join(non_empty_lines)

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)
    print(f"网站 {url} 内容已保存至文件：{file_name}")


async def process_url(url, output_dir):
    try:
        content = await extract_content(url)
        if content:
            save_content(content, output_dir, url)
            return f"处理 {url} 成功"
        else:
            return f"处理 {url} 失败：无法提取内容"
    except Exception as e:
        return f"处理 {url} 失败：{str(e)}"


async def process_urls(urls, output_dir, num_concurrent):
    tasks = []
    results = []

    for url in urls:
        task = process_url(url, output_dir)
        tasks.append(task)

        if len(tasks) >= num_concurrent:
            results += await asyncio.gather(*tasks)
            tasks = []

    if tasks:
        results += await asyncio.gather(*tasks)

    return results


def main():
    if len(sys.argv) != 4:
        print("请提供要抓取的 URL 列表文件名、保存提取内容的目录和并发请求数")
        print("示例: python extract_urls.py urls.txt data 10")
        sys.exit(1)

    urls_file = sys.argv[1]  # 存储要抓取的 URL 列表的文件名
    output_dir = sys.argv[2]  # 保存提取内容的目录
    num_concurrent = int(sys.argv[3])  # 并发请求数

    with open(urls_file, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file]

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(process_urls(urls, output_dir, num_concurrent))

    for result in results:
        print(result)

    print('所有网站内容保存完成！')


if __name__ == '__main__':
    main()
