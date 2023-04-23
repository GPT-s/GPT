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


# def summarize(text):
#     model_engine = "text-davinci-002"

#     max_tokens = 2500

#     if text is not None:
#         query = f"""Summarize the following paragraphs.
#         {text}
#         """
#     else:
#         print("empty text.")

#     completion = openai.Completion.create(
#         engine=model_engine,
#         prompt=query,
#         max_tokens=max_tokens,
#         temperature=0.3,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0,
#     )
#     return completion.choices[0].text


# 토큰 제한 때메 테스트점

def summarize(text):
    # 텍스트를 토큰으로 분리
    tokens = text.split()

    # 토큰의 최대 길이를 4097로 제한
    max_tokens = 4097
    tokens = tokens[:max_tokens]

    # 제한된 토큰들을 다시 텍스트로 변환
    truncated_text = ' '.join(tokens)

    # 요약 작업
    openai.api_key = OPENAI_API_KEY
    completion = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"summarize the following text: {truncated_text}",
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    summary = completion.choices[0].text.strip()
    return summary


def get_summary_list(text_list):
    summary_list = []
    for text in text_list:
        summary = summarize(text)
        summary_list.append(summary)
    print("요약 완")
    print("요약 완")
    print("요약 완")
    print("요약 완")
    print("요약 완")
    return summary_list
