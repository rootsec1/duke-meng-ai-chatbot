# Replace default sqlite3 with pysqlite3 to deal with streamlit bug
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import chromadb
import requests
import streamlit as st
import re
# Local
from constants import RAG_PROMPT, QUESTION_WORDS_SET

chromadb_client = chromadb.HttpClient(
    os.environ.get("CHROMA_HOST", st.secrets["CHROMA_HOST"])
)
rag_collection = chromadb_client.get_collection("rag")


def query_vector_database_for_rag_content(query: str) -> str:
    query_vector = rag_collection.query(
        query_texts=[query]
    )
    doc_list = query_vector.get("documents", [])
    doc_list = doc_list[0]
    context = ""
    for doc in doc_list:
        doc = doc.strip()
        doc_lower = doc.lower()
        doc_word_list = doc_lower.split(" ")
        if len(doc_word_list) >= 5:
            contains_question_word = False
            for word in QUESTION_WORDS_SET:
                if doc_word_list[0].lower() == word:
                    contains_question_word = True
                    break
            if not contains_question_word:
                context += f"{doc}\n\n"
    # Replace more than 2 newlines with 2 newlines using regex
    context = re.sub(r"\n{2,}", "\n\n", context)
    context = context.strip()
    return context


def prompt_llm_for_response(prompt: str) -> str:
    API_URL = os.environ.get("MODEL_HOST", st.secrets["MODEL_HOST"])
    HF_TOKEN = os.environ.get("HF_TOKEN", st.secrets["HF_TOKEN"])
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "return_full_text": False
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response = response.json()
    content = ""
    for item in response:
        content += item.get("generated_text", "")
    content = content.strip()
    return content


@st.cache_data
def get_bot_response(user_prompt: str) -> str:
    user_prompt = user_prompt.lower().strip()
    context = query_vector_database_for_rag_content(user_prompt)
    try:
        formatted_prompt = RAG_PROMPT.format(
            context=context,
            user_query=user_prompt,
        )
        print(f"PROMPT 1: {formatted_prompt}")
        llm_response = prompt_llm_for_response(formatted_prompt)
        formatted_prompt = f"{formatted_prompt} {llm_response}"
        print(f"PROMPT 2: {formatted_prompt}")
        llm_response_2 = prompt_llm_for_response(formatted_prompt)
        llm_response += llm_response_2
        return llm_response
    except Exception as ex:
        print(ex)
        return "Serverless endpoint is now booting up. Please try again in a few minutes."
