#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
def chat_id(i):
    url = "https://api.telegram.org/bot6297598995:AAF1kW0FinpGn737xiag1ESOtVUWZUQfTpA/getUpdates"
    response = requests.get(url)
    response_dict = response.json()
    res_chat = i
    if(response_dict['result'] == []) == True:
        ct_id = "null"
    else :
        ct_id = response_dict['result'][-(res_chat)]['message']['from']['id']
    return ct_id

