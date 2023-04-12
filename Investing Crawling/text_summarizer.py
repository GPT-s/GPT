#!/usr/bin/env python
# coding: utf-8

# In[2]:


import openai

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

def summarize(text):
    
    model_engine = "text-davinci-002"

    max_tokens = 2500
    
    query = f'''Please summarize the following paragraph and translate it into Korean.

    {text}
    ''' 
    
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

