import os
from groq import Groq

groq_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


def get_bot_response_using_groq(
    user_prompt: str,
    system_prompt: str = "You are a helpful assistant",
    model: str = "llama3-8b-8192"
) -> str:
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        model=model
    )
    return chat_completion.choices[0].message.content.strip()
