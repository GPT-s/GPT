#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests

def send_message(chat_id, text):
    url = "https://api.telegram.org/bot6297598995:AAF1kW0FinpGn737xiag1ESOtVUWZUQfTpA/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(url, params=params)
    return response.json()

