# GPT!
import openai
from dotenv import load_dotenv
import os
import re

load_dotenv()

GPTAPI = os.environ.get("GPTAPI")

OPENAI_API_KEY = GPTAPI
openai.api_key = OPENAI_API_KEY



def keyword(text):
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
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
                )
            answer = response['choices'][0]['message']['content']
            stockcode = re.search(r'\[(.*?)\]', answer).group(1)
            return stockcode
        except Exception as e:
            print("Error:", e)
            retries += 1
            if retries == max_retries:
                print("최대 재시도 횟수 초과")
                gpt_error = "오류"
                return gpt_error




def summarize(text):
    print("gpt 1번 시작")
    sentiment_gptquery = f"Sentimentally analyze [{text}] and select only one of Positive, Negative, or Negative"
    sentiment_messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": sentiment_gptquery}
                ]
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            sentiment_response = openai.ChatCompletion.create(
                        temperature=0,
                        top_p=0,
                        model= "gpt-3.5-turbo",
                        messages=sentiment_messages
                        )
            sentiment_answer = sentiment_response['choices'][0]['message']['content']
            break
        except Exception as e:
            print("Error:", e)
            retries += 1
            if retries == max_retries:
                print("최대 재시도 횟수 초과")
                gpt_error = "오류"
                return gpt_error
    summarize_gptquery = f"Summarize [{text}] in 5 lines with a maximum of 38 characters per line."
    summarize_messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": summarize_gptquery}
                ]
    retries = 0
    while retries < max_retries:
        try:
            summarize_response = openai.ChatCompletion.create(
                        temperature=0,
                        top_p=0,
                        model= "gpt-3.5-turbo",
                        messages=summarize_messages
                        )
            summarize_answer = summarize_response['choices'][0]['message']['content']
            break
        except Exception as e:
            print("Error:", e)
            retries += 1
            if retries == max_retries:
                print("최대 재시도 횟수 초과")
                gpt_error = "오류"
                return gpt_error
    return sentiment_answer, summarize_answer


def get_summary_list(text_list):
    print("gpt 2번 시작")
    summary_list = []
    for text in text_list:
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                summary = summarize(text)
                summary_list.append(summary)
            except Exception as e:
                print("Error:", e)
                retries += 1
                if retries == max_retries:
                    print("최대 재시도 횟수 초과")
                    gpt_error = "오류"
                    return gpt_error      
    print("gpt 2번 완")
    return summary_list