import requests
import random
import os
from bs4 import BeautifulSoup
import sys

def extract_subscription_urls(search_query, search_engine):
    if search_engine == "google":
        search_url = f"https://www.google.com/search?q={search_query}"
    elif search_engine == "yandex":
        search_url = f"https://yandex.com/search/?text={search_query}"
    else:
        raise ValueError("Invalid search engine")

    # 随机选择User-Agent标头
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

# 保存提取到的订阅地址到文件中，封装成一个函数，并接收文件名作为参数
def save_urls_to_file(urls, file_name):
    with open(file_name, "a") as file:  # 注意，这里使用 "a" 模式来追加内容到文件
        file.write("\n".join(urls) + "\n")

# 从环境变量中获取搜索关键字和搜索引擎
search_query = os.getenv("SEARCH_QUERY", "订阅节点")
search_engine = os.getenv("SEARCH_ENGINE", "google")  # 默认设置为 "google"

# 获取保存文件名的命令行参数
if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = "sec_urls"  # 如果未提供文件名参数，则使用默认文件名 "sec_urls"

# 使用 Google 搜索并随机调整请求头信息
if search_engine == "google":
    urls_google = extract_subscription_urls(search_query, "google")
    print("Google Search Results:")
    for url in urls_google:
        print(url)

    # 将搜索引擎设置为 "yandex"，继续执行搜索
    search_engine = "yandex"

# 使用 Yandex 搜索并随机调整请求头信息
if search_engine == "yandex":
    urls_yandex = extract_subscription_urls(search_query, "yandex")
    print("Yandex Search Results:")
    for url in urls_yandex:
        print(url)

    # 合并 Google 和 Yandex 的结果
    urls = urls_google + urls_yandex

    # 保存提取到的订阅地址到文件中，调用保存函数并传入文件名参数
    save_urls_to_file(urls, file_name)
