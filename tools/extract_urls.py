import requests
import random
import os
import concurrent.futures
import argparse
from bs4 import BeautifulSoup

def extract_subscription_urls(search_query, search_engine):
    if search_engine == "google":
        search_url = f"https://www.google.com/search?q={search_query}"
    elif search_engine == "yandex":
        search_url = f"https://yandex.com/search/?text={search_query}"
    else:
        raise ValueError("Invalid search engine")

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"
    ]
    user_agent = random.choice(user_agents)
    headers = {"User-Agent": user_agent}

    response = requests.get(search_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all("a")

    subscription_urls = []
    for result in search_results:
        href = result.get("href")
        if href and href.startswith("http"):
            subscription_urls.append(href)

    return subscription_urls

def search_and_save_urls(search_query, output_file):
    engines = ["google", "yandex"]

    with open(output_file, "a") as file:
        for engine in engines:
            urls = extract_subscription_urls(search_query, engine)
            file.write(f"{engine.capitalize()} Search Results:\n")
            file.write("\n".join(urls) + "\n\n")

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
