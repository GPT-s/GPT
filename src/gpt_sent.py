import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import os

GPTAPI = os.environ.get('GPTAPI')
OPENAI_KEY = GPTAPI
openai.api_key = OPENAI_KEY

def sentiment_analysis(text):
    model_engine = "text-davinci-003"
    max_tokens = 2500
    prompt = f'''Please analyze the sentiment of this article as positive, negative, or neutral:
    {text}
    '''
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.3,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return completion.choices[0].text.strip()
