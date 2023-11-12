import requests
import random
import os
import concurrent.futures
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_subscription_urls(search_query, search_engine):
    # ... （之前的代码保持不变）

    subscription_urls = []
    for result in search_results:
        href = result.get("href")
        if href:
            parsed_url = urlparse(href)
            if parsed_url.scheme and parsed_url.netloc:
                subscription_urls.append(parsed_url.geturl())

    return subscription_urls

def search_and_save_urls(search_query, output_file):
    engines = ["google", "yandex"]

    with open(output_file, "a") as file:
        for engine in engines:
            urls = extract_subscription_urls(search_query, engine)
            file.write(f"{engine.capitalize()} Search Results:\n")
            for url in urls:
                file.write(f"{url}\n")
            file.write("\n")

    print('搜索和保存URL完成！')

def main():
    parser = argparse.ArgumentParser(description="Search and save subscription URLs")
    parser.add_argument("output_file", help="Output file path")
    args = parser.parse_args()

    search_queries = ["节点订阅", "节点池2023", "Free proxies"]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for search_query in search_queries:
            futures.append(executor.submit(search_and_save_urls, search_query, args.output_file))

        # 等待所有搜索任务完成
        concurrent.futures.wait(futures)

    print('搜索和保存URL完成！')

if __name__ == '__main__':
    main()
