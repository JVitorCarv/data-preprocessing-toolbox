import os
import requests
from duckduckgo_search import DDGS
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def download_image(image_url, folder_path, image_name):
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("http://", adapter)
    http.mount("https://", adapter)

    try:
        response = http.get(image_url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        image_path = os.path.join(folder_path, image_name)
        with open(image_path, "wb") as handler:
            handler.write(response.content)
        print(f"Downloaded: {image_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {image_url}: {e}")


def search_and_download_images(query, folder_path, max_results=5):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    ddgs = DDGS()
    results = ddgs.images(keywords=query, max_results=max_results)

    for i, result in enumerate(results):
        image_url = result["image"]
        image_name = f"ddg_{i + 1}.jpg"
        download_image(image_url, folder_path, image_name)


if __name__ == "__main__":
    search_term = "Fiat Uno Mille"
    download_folder = "downloaded_images"
    search_and_download_images(search_term, download_folder, max_results=500)
