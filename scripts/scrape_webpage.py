import os
import json
from time import sleep
import requests
import google.generativeai as genai

from urllib.parse import urlparse
from bs4 import BeautifulSoup
from google.generativeai.types import HarmCategory, HarmBlockThreshold

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
# Get key-value pair with key = HarmCategory var, value = HarmBlockThreshold.BLOCK_NONE
# This is to disable blocking for all harmful categories
# The model will still generate content that is safe for all categories
safety_settings = {
    # HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_DEROGATORY: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_VIOLENCE: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
}

model = genai.GenerativeModel(
    'gemini-pro',
    safety_settings=safety_settings,
)

PREFIX = "internal"

with open(f"data/processed/{PREFIX}-website-links.json", 'r') as file:
    content = file.read()

json_content = json.loads(content)

for url in json_content:
    response = requests.get(url)
    if response.ok:
        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove all <nav> elements from the soup
        for nav in soup.find_all('nav'):
            nav.decompose()

        main_div = soup.find('div', id='content')
        if PREFIX == "external":
            main_div = soup.find('div', id='main')
            main_div = main_div.find('div', id='content')
        
        soup = main_div
        prompt = f"""
        Scrape all the text from this HTML and return the output in plain text format. Do not use markdown.

        {soup}
        """
        using_model = "v1"
        try:
            model_response = model.generate_content(prompt)
            model_response = model_response.text.strip()
            using_model = "v1"
        except:
            text_content = ["".join(text) for text in soup.stripped_strings]
            text_content = "\n".join(text_content)
            prompt = f"""
            The following is the the text content of a scraped HTML page, clean and rearrange the content to make it look formatted and look like it makes sense.
            Preserve all the original information. Output the result in plain text, do not use markdown.

            {text_content}
            """
            model_response = model.generate_content(prompt)
            model_response = model_response.text.strip()
            using_model = "v2"

        # Create a filename from the URL path
        parsed_url = urlparse(url)
        # Use os.path.basename to get the last part of the path, and remove any trailing slashes
        filename = os.path.basename(parsed_url.path.rstrip('/')) or 'index'
        filename += '.txt'  # Add the .txt extension to the filename

        # Write all text to a file
        with open(f"data/processed/{PREFIX}-scraped/{filename}", 'w', encoding='utf-8') as file:
            file.write(model_response)
        print(
            f"Content from {url} saved to {filename}, using model: {using_model}")
    else:
        print(f"Failed to retrieve content from {url}")
