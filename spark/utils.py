# Import libraries
import os, signal
import json
import time

import subprocess

from trainer import *

# # MongoDB Setup
from pymongo import MongoClient
client = MongoClient()

client = MongoClient('mongo', 27017)

db = client['news_db']

articles = db['articles']

new_articles = db['new_articles']

clf = pickle.load(open("models/news_classifier.pkl", "rb"))
le = pickle.load(open("models/label_encoder.pkl", "rb"))
tfidf = pickle.load(open("models/tfidf_vect.pkl", "rb"))

# function to load the model
def load_model():
    global clf
    clf = pickle.load(open("models/news_classifier.pkl", "rb"))
    # load data if empty
    if (articles.count() == 0) :
        with open("/app/data/news_db.json", encoding = 'utf-8') as f:
            data = json.load(f)
            articles.insert_many(data)

# function to predict the flower using the model
def predict(query_data):
    x = list(query_data.dict().values())
    inp = tfidf.transform(x).toarray()
    res = clf.predict(inp)
    prediction = le.inverse_transform(res)[0]
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
def train_model():
    # load the model
    global clf
    clf = pickle.load(open("models/news_classifier.pkl", "rb"))

    new_data = []
    for data in new_articles.find({}):
        new_data.append(data)
    
    data = pd.DataFrame(new_data)
    
    if(len(data) > 0):
        data['len'] = data['summary'].str.len()
        data['summary_parsed'] = data['summary'].apply(process_text)
        data['topic_target'] = le.fit_transform(data['topic'])

        X_train, X_test, y_train, y_test = train_test_split(
            data['summary_parsed'], 
            data['topic_target'],
            test_size=0.2, 
            random_state=8)

        features_train = tfidf.transform(X_train).toarray()
        labels_train = y_train

        features_test = tfidf.transform(X_test).toarray()
        labels_test = y_test

        clf.fit(features_train, labels_train)

        model_predictions = clf.predict(features_test)
        acc = accuracy_score(labels_test, model_predictions) * 100
        print('Accuracy: ', acc)
        print(classification_report(labels_test, model_predictions))

        # save the model
        pickle.dump(clf, open("models/news_classifier.pkl", "wb"))

        return {
            "message" : "Training Successful",
            "accuracy" : acc}

    return ({"message" : "Not enough new data to train"})