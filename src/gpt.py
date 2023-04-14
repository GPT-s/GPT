# GPT!
import openai
from dotenv import load_dotenv
import os

load_dotenv()

GPTAPI = os.environ.get('GPTAPI')

OPENAI_API_KEY = GPTAPI
openai.api_key = OPENAI_API_KEY

def summarize(text):
    
    model_engine = "text-davinci-002"

    max_tokens = 2500
    
    if text is not None:
        query = f'''Summarize the following paragraphs.
        {text}
        ''' 
    else:
        print("empty text.")


    completion = openai.Completion.create(
        engine=model_engine,
        prompt=query,
        max_tokens=max_tokens,
        temperature=0.3,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return completion.choices[0].text