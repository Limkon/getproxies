import os
import requests
import threading
import random
import argparse
import time

# Command-line argument parsing
parser = argparse.ArgumentParser(description='Multi-threaded web crawler')
parser.add_argument('url_file', type=str, help='Path to the file containing the list of URLs')
parser.add_argument('save_directory', type=str, help='Directory to save the pages')
parser.add_argument('--num_threads', type=int, default=5, help='Number of threads')
args = parser.parse_args()

# URL file path
url_file = args.url_file

# Save directory
save_directory = args.save_directory

# Number of threads
num_threads = args.num_threads

# List of headers to simulate multiple browsers
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
    # Add more headers...
]

# Create a global variable to track the start time
start_time = None

def save_page_content(url, headers):
    try:
        # Send HTTP request to get page content
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Get filename from URL
        file_name = os.path.basename(url)

        # Remove ".txt" extension from the filename
        file_name, _ = os.path.splitext(file_name)

        # Save page content as text file
        save_path = os.path.join(save_directory, file_name + '.txt')
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text)

        print(f"Saved page content of {url} to {save_path}")
    except Exception as e:
        print(f"Error occurred while retrieving page content of {url}: {str(e)}")

def crawl_urls(urls):
    global start_time
    for url in urls:
        # Check if more than 10 minutes have passed, if so, save results and exit
        if time.time() - start_time > 600:  # 10 minutes = 600 seconds
            print("Exceeded 10-minute runtime, saving results and exiting")
            return

        headers = random.choice(headers_list)
        save_page_content(url, headers)

def main():
    global start_time
    start_time = time.time()
    
    # Create save directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    # Read the list of URLs from the file
    with open(url_file, 'r') as file:
        urls = file.read().splitlines()

    # Calculate the number of URLs each thread needs to handle
    num_urls = len(urls)
    urls_per_thread = num_urls // num_threads

    # Create threads and start them
    threads = []
    for i in range(num_threads):
        start_index = i * urls_per_thread
        end_index = start_index + urls_per_thread if i < num_threads - 1 else num_urls
        thread_urls = urls[start_index:end_index]

        thread = threading.Thread(target=crawl_urls, args=(thread_urls,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("Crawling completed")

if __name__ == "__main__":
    main()
