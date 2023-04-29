# GPT!
import openai
from dotenv import load_dotenv
import os
import re

load_dotenv()

GPTAPI = os.environ.get("GPTAPI")

OPENAI_API_KEY = GPTAPI
openai.api_key = OPENAI_API_KEY


# def get_completion(text, model="gpt-3.5-turbo"):
#     messages = [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": text},
#     ]
#     max_retries = 3
#     retries = 0
#     while retries < max_retries:
#         try:
#             response = openai.ChatCompletion.create(model=model, messages=messages)
#             answer = response["choices"][0]["message"]["content"]
#             return answer
#         except Exception as e:
#             print("Error:", e)
#             retries += 1
#             if retries == max_retries:
#                 print("최대 재시도 횟수 초과")
#                 return None
#             else:
#                 print("재시도...")
#                 time.sleep(1)

def keyword(text):
    try:
        gptquery = f"{text}in the sentence above Tell me keywords,\n\
                                            Change keywords with stock codes to stock codes in Keywords and mark all keywords\n\
                                            no explanation needed\n\
                                            Example:\n\
                                            Keywords: Amazon (AMZN), today's price, recent news.\n\
                                            stock Keywords: [AMZN]or\n\
                                            stock Keywords: [001122.ks]or\n\
                                            no Keywords: [N/A]"  
        messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": gptquery}
                    ]
        response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                    )
        answer = response['choices'][0]['message']['content']
        stockcode = re.search(r'\[(.*?)\]', answer).group(1)
        return stockcode
    except Exception as e:
        keyword()



def summarize(text):
    print("gpt 1번 시작")
    try:
        gptquery = f"Sentimentally analyze [{text}] and select only one of Positive, Negative, or Negative"
        messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": gptquery}
                    ]
        response = openai.ChatCompletion.create(
                    temperature=0,
                    top_p=0,
                    model= "gpt-3.5-turbo",
                    messages=messages
                    )
        sentiment_answer = response['choices'][0]['message']['content']
        gptquery = f"Summarize [{text}] in 5 lines with a maximum of 38 characters per line."
        messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": gptquery}
                    ]
        response = openai.ChatCompletion.create(
                    temperature=0,
                    top_p=0,
                    model= "gpt-3.5-turbo",
                    messages=messages
                    )
        summarize_answer = response['choices'][0]['message']['content']
        print("gpt 1번 완")
        return sentiment_answer,summarize_answer
    # 수정
    except Exception as e:
        summarize()


def get_summary_list(text_list):
    print("gpt 2번 시작")
    summary_list = []
    for text in text_list:
        summarize_answer = summarize(text)
        summary_list.append(summarize_answer)
        
    print("gpt 2번 완")
    return summary_list