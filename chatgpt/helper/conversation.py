import openai

from config import config

openai.api_key = config.OPENAI_API_KEY

def chat_completion(messages: list) -> str:
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return completion['choices'][0]['message']['content']
    except:
        return config.ERROR_MESSAGE
