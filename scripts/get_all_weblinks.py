import requests
from bs4 import BeautifulSoup


def get_all_web_links_in_file(file_path: str, base_domain: str):
    with open(file_path, 'r') as file:
        content = file.read()
    soup = BeautifulSoup(content, features="xml")
    locs = soup.find_all('loc')

    # Find all the anchor tags in the HTML.
    urls = [loc.text for loc in locs if loc.text]

    # Print out all URLs.
    for url in urls:
        if url is None:
            continue
        if base_domain in url:
            url = url.replace("\n", "").strip()
            print(f"\"{url}\",")


get_all_web_links_in_file(
    "data/raw/sitemap_ece.xml",
    "ece.duke.edu"
)
