import pickle
from sklearn.naive_bayes import GaussianNB

import os, signal
import json
import time

import subprocess

# # MongoDB Setup
from pymongo import MongoClient
client = MongoClient()

client = MongoClient('mongo', 27017)

db = client['news_db']

articles = db['articles']

clf = GaussianNB()

# function to load the model
def load_model():
    global clf
    clf = pickle.load(open("models/news_classifier.pkl", "rb"))
    # load data
    with open("/app/data/news_db.json", encoding = 'utf-8') as f:
        data = json.load(f)
        articles.insert_many(data)

# function to predict the flower using the model
def predict(query_data):
    x = list(query_data.dict().values())
    prediction = clf.predict([x])[0]
    return prediction

def transformer(data):
    # listen to kafka and add data to pymongo
    time_delay = list(data.dict().values())[0]
    proc1 = subprocess.Popen("spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.8.jar transformer.py", shell = True)
    time.sleep(time_delay)
    print ('killing proc1 = ', proc1.pid)
    subprocess.Popen.kill(proc1)
    os.system("kill $(ps aux | grep 'pyspark' | awk '{print $2}')")

# function to train and save the model as part of the feedback loop
def train_model(data):
    # load the model
    clf = pickle.load(open("models/news_classifier.pkl", "rb"))

    # pull out the relevant X and y from the FeedbackIn object
    X = [list(d.dict().values())[:-1] for d in data]
    y = [d.wine_class for d in data]

    # fit the classifier again based on the new data obtained
    clf.fit(X, y)

    # save the model
    pickle.dump(clf, open("models/news_classifier.pkl", "wb"))