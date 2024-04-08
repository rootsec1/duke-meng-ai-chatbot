import requests
from bs4 import BeautifulSoup


def get_all_web_links_in_file(file_path: str, base_domain: str):
    with open(file_path, 'r') as file:
        content = file.read()
    soup = BeautifulSoup(content, "lxml")
    anchors = soup.find_all('a')

    # Find all the anchor tags in the HTML.
    urls = [anchor.get('href') for anchor in anchors if anchor.get('href')]

    # Print out all URLs.
    for url in urls:
        if url is None:
            continue
        if base_domain in url:
            print(f"\"{url}\",")


get_all_web_links_in_file(
    "data/raw/external-website-sitemap.xml",
    "ai.meng.duke.edu"
)
