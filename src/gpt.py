# GPT!
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

def summarize(text):
    print("gpt 1번 시작")
    model_engine = "text-davinci-002"

    max_tokens = 2500

    if text is not None:
        sentiment_list = ['positive', 'negative', 'neutral']
        query = f"""Sentiment analysis the contents of [{text}], output one of three words {str(sentiment_list) } based on the analysis, summarize the contents of [] Korean in about 5 lines.
        """
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
    print("gpt 1번 완")
    return completion.choices[0].text


def get_summary_list(text_list):
    print("gpt 2번 시작")
    summary_list = []
    for text in text_list:
        summary = summarize(text)
        summary_list.append(summary)
        
    print("gpt 2번 완")
    return summary_list