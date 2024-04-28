import os
import json
import requests
import google.generativeai as genai

from tqdm.auto import tqdm
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from google.generativeai.types import HarmCategory, HarmBlockThreshold

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
}

model = genai.GenerativeModel(
    'gemini-pro',
    safety_settings=safety_settings,
)

PREFIX = "ece"

with open(f"data/processed/{PREFIX}-website-links.json", 'r') as file:
    content = file.read()

json_content = json.loads(content)

for url in tqdm(json_content):
    response = requests.get(url)
    if response.ok:
        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove all <nav> elements from the soup
        for nav in soup.find_all('nav'):
            nav.decompose()

        prompt = f"""
        Scrape all the text from this HTML and return the output in plain text format.
        Clean and rearrange the content to make it look formatted and look like it makes sense.
        Preserve all the original information. Output the result in plain text, do not render output in markdown.

        {soup.text.strip()}
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
            try:
                model_response = model.generate_content(prompt)
                model_response = model_response.text.strip()
                using_model = "v2"
            except:
                prompt = f"""
                The following is the the text content of a scraped HTML page, clean and summarize the content such that it makes sense.
                Preserve all the original information. Output the result in plain text, do not use markdown. 

                {text_content}               
                """
                try:
                    model_response = model.generate_content(prompt)
                    model_response = model_response.text.strip()
                    using_model = "v3"
                except:
                    print(f"Skipping {url} after model {using_model} failed")
                    continue

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
