#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
def message_text(i):
    url = "https://api.telegram.org/bot6297598995:AAF1kW0FinpGn737xiag1ESOtVUWZUQfTpA/getUpdates"
    response = requests.get(url)
    response_dict = response.json()
    res_text = i
    if (response_dict['result'] == []) == True:
        msgtext = "null"    
    else :
        msgtext = response_dict['result'][-(res_text)]['message']['text']
    return msgtext

