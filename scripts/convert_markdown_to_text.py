import markdown
import os

from bs4 import BeautifulSoup

PREFIX = "internal"
file_list = os.listdir(f"data/processed/{PREFIX}-scraped")

for file_name in file_list:
    with open(f"data/processed/{PREFIX}-scraped/{file_name}", "r") as file:
        content = file.read()

    # Convert Markdown to HTML
    html = markdown.markdown(content)

    # Use BeautifulSoup to convert HTML to plain text
    soup = BeautifulSoup(html, features='html.parser')
    plain_text = soup.get_text()

    with open(f"data/processed/cleaned/{PREFIX}-{file_name}", "w") as file:
        file.write(plain_text)

print("All files converted from Markdown to plain text.")
