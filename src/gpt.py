# GPT!
import openai
from dotenv import load_dotenv
import os
import re
import time

# load_dotenv()

# GPTAPI = os.environ.get("GPTAPI")

# OPENAI_API_KEY = GPTAPI
# openai.api_key = OPENAI_API_KEY

class GPT:
    def __init__(self):
        load_dotenv()

        GPTAPI = os.environ.get("GPTAPI")
        OPENAI_API_KEY = GPTAPI
        openai.api_key = OPENAI_API_KEY

    def keyword(self, text):
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




    def summarize(self, text):
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
                print(1)
                sentiment_response = openai.ChatCompletion.create(
                            temperature=0,
                            top_p=0,
                            model= "gpt-3.5-turbo",
                            messages=sentiment_messages
                            )
                sentiment_answer = sentiment_response['choices'][0]['message']['content']
                print(2)
                break
            except Exception as e:
                print("Error:", e)
                print(3)
                retries += 1
                if retries == max_retries:
                    print("최대 재시도 횟수 초과")
                    print(4)
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
                print(5)
                summarize_response = openai.ChatCompletion.create(
                            temperature=0,
                            top_p=0,
                            model= "gpt-3.5-turbo",
                            messages=summarize_messages
                            )
                summarize_answer = summarize_response['choices'][0]['message']['content']
                print(6)
                break
            except Exception as e:
                print("Error:", e)
                print(7)
                retries += 1
                if retries == max_retries:
                    print("최대 재시도 횟수 초과")
                    print(8)
                    gpt_error = "오류"
                    return gpt_error
        print(9)
        print("gpt 1번 완")
        return sentiment_answer, summarize_answer


    def summarize_news(self, text):
        print("gpt 1번 시작")
        model_engine = "text-davinci-002"
        max_tokens = 2500
        if text is not None:
            query = f"""Sentimentally analyze [{text}] and select only one of Positive, Negative, or Neutral. Also, summarize [] in 5 lines with a maximum of 38 characters per line.
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

    def get_summary_list(self, text_list):
        print("gpt 2번 시작")
        summary_list = []
        for text in text_list:
            summary = GPT.summarize_news(text)
            summary_list.append(summary)
        print("gpt 2번 완")
        return summary_list

# def summarize_news(text):
#     print("gpt 1번 시작")
#     model_engine = "text-davinci-002"
#     max_tokens = 2500
#     if text is not None:
#         query = f"""Sentimentally analyze [{text}] and select only one of Positive, Negative, or Neutral. Also, summarize [] in 5 lines with a maximum of 38 characters per line.
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
#     print("gpt 1번 완")
#     return completion.choices[0].text

# def get_summary_list(text_list):
#     print("gpt 2번 시작")
#     summary_list = []
#     for text in text_list:
#         summary = summarize_news(text)
#         summary_list.append(summary)
#     print("gpt 2번 완")
#     return summary_list


# def get_summary_list(text_list):
#     print("gpt 2번 시작")
#     summary_list = []
#     for text in text_list:
#         sentiment_answer, summarize_answer = summarize(text)
#         # summary = str(sentiment_answer)+"\n"+str(summarize_answer)
#         summary_list.append(summarize_answer)
#         # summary_list.append(summary)
#     print("gpt 2번 완")
#     return summary_list
