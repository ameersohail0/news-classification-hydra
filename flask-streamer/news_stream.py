#! /usr/bin/python3                                                                                                      

from kafka import KafkaProducer                                                                                         
from random import randint                                                                                              
from time import sleep                                                                                                  
import sys
import pandas as pd

import os
from dotenv import load_dotenv
import requests
import json

# Sleep from Time library
from time import sleep
                                                                                                                        
BROKER = "broker:9092"                                                                                    
TOPIC = 'news-trainer'                                                                                                                                                                                 
                                                                                                                        
try:                                                                                                                    
    p = KafkaProducer(bootstrap_servers=BROKER)                                                                         
except Exception as e:                                                                                                  
    print(f"ERROR --> {e}")                                                                                             
    sys.exit(1)

load_dotenv()

url = "https://free-news.p.rapidapi.com/v1/search"

headers = {
    'x-rapidapi-host': "free-news.p.rapidapi.com",
    'x-rapidapi-key': os.getenv('API_KEY') # hide API key
    }

# # MongoDB Setup
# from pymongo import MongoClient
# client = MongoClient()

# client = MongoClient('mongo', 27017)

# db = client['news-db']

# articles = db['articles']

TOPICS = ["Sports","Business","Tech","Finance","Crime"]

# for topic in TOPICS:
#     for page_no in range(1,5):
#         querystring = {"q":topic,"lang":"en","page":str(page_no),"page_size":"25"}
#         response = requests.request("GET", url, headers=headers, params=querystring)
#         try:
#             for article in response.json()['articles']:
#                 try:
#                     message = article["topic"]+"//"+article["title"]+"//"+article["summary"]                                                                                       
#                     print(f">>> {message.split('//')}")                                                                                           
#                     p.send(TOPIC, bytes(message, encoding="utf8"))
#                 except:
#                     print("message can't be sent")                                                                      
#                 sleep(1)
#         except :
#             print(f"max limit for topic {topic} reached")

#         sleep(2)

news = json.load(open("news_articles.json",encoding="utf-8"))

while True:                                                                                                             
    for article in news:
        try:
            message = article["topic"]+"//"+article["title"]+"//"+article["summary"]
            print(f">>> {message.split('//')}")
            p.send(TOPIC, bytes(message, encoding="utf8"))
        except:
            print("message can't be sent")
        sleep(1)
