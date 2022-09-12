#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd

url = 'https://raw.githubusercontent.com/PriyanshuBarnwal/Projects/main/output.tsv'

df = pd.read_csv(url, sep="\t")

base_url = "https://api.telegram.org/bot950526089:AAEzU80OPxsa_JCIvSO-qYxHIbipa1hZJO8"

def read_message(offset):
    parameters = {
       'offset' : offset
    }
    reqs = requests.get(base_url+"/getupdates", data = parameters)
    print(reqs.text)
    data = reqs.json()
    for result in data["result"]:
           print("hi")
           # send_message(result)  #for starting just comment this line once
    if data["result"]:
        return (data["result"][-1]["update_id"]+1)
        

def auto_answer(message):
    answer = df.loc[df[' Question'].str.lower() == message.lower()]  
    if not answer.empty:
        answer = answer.iloc[0]['Answer']
        return answer
    else:
        df.loc[len(df.index)] = [message,"","",""]
        df.to_csv(url, sep="\t" , index=False)
        print(df.tail(1))
        return "Sorry, I could not understand you !!! I am still learning and try to get better in answering."
      



def send_message(message):
    text = message["message"]["text"]
    message_id = message["message"]["message_id"]
    answer = auto_answer(text)
    parameters = {
      "chat_id" : "-685720655",
      "text" : answer,
      "reply_to_message_id" : message_id
  }

    resp = requests.get(base_url + "/sendMessage", data = parameters)
    print(resp.text)

offset = 0
while True:
    offset = read_message(offset)
    


# In[ ]:




