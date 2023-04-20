# GPT_keyword
import openai
from dotenv import load_dotenv
import os
import time

load_dotenv()

GPTAPI = os.environ.get("GPTAPI")

OPENAI_API_KEY = GPTAPI
openai.api_key = OPENAI_API_KEY


def get_completion(text, model="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text},
    ]
    max_retries = 3
    retries = 0 
    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(model=model, messages=messages)
            answer = response["choices"][0]["message"]["content"]
            return answer
        except Exception as e:
            print("Error:", e)
            retries += 1
            if retries == max_retries:
                print("Max retries exceeded")
                return None
            else:
                print("Retrying...")
                time.sleep(1)


def analyze_keyword(text):
    model_engine = "text-davinci-002"

    max_tokens = 2500

    if text is not None:
        query = f""" {text} in the sentence above Tell me keywords, Change keywords with stock codes to stock codes in Keywords and mark all keywords no explanation needed 
        Example: Keywords: Apple (AAPL), news, price. only answer me"""
    else:
        print("empty text.")

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=query,
        max_tokens=max_tokens,
        temperature=0.3,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return completion.choices[0].text


def get_analyze_keyword(text_list):
    analyze_list = []
    for text in text_list:
        analyze = analyze_keyword(text)
        analyze_list.append(analyze)
    return analyze_list
