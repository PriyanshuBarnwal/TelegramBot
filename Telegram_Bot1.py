#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("Credintals.json",scope)

client = gspread.authorize(creds)
sheet = client.open("output").sheet1

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT_Pg8k7Ydq94tYrN2UTFINnyesgIMsd1Dkrfd9Ks64zAbDXO4LC22Q6VerpWi5OdGLtJKHm0FGK7xg/pub?gid=1582598662&single=true&output=tsv'

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
           #print("hi")
           send_message(result)  #for starting just comment this line once
    if data["result"]:
        return (data["result"][-1]["update_id"]+1)
        

def auto_answer(message):
    df = pd.read_csv(url, sep="\t")
    answer = df.loc[df['Question'].str.lower() == message.lower()]  
    if not answer.empty:
        answer = answer.iloc[0]['Answer']
        print(type(answer),"-",answer)
        if str(answer) == "nan":
            return "Sorry, I could not understand you !!! I will be very soon replying this one."
        else:
            return answer
    else:
        sheet.insert_row((message.lower(),"","",""),2)
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




