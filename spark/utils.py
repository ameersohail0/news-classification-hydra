# Import libraries
import os
import subprocess

import json
import pickle
import time

import pandas as pd

from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from trainer import process_text, category_list

# # MongoDB Setup
from pymongo import MongoClient

client = MongoClient('mongo', 27017)

db = client['news_db']
articles = db['articles']

# load model and other functions
clf = pickle.load(open("models/news_classifier.pkl", "rb"))
count_vect = CountVectorizer(vocabulary=pickle.load(open("models/count_vector.pkl", "rb")))
tfidf = pickle.load(open("models/tfidf.pkl", "rb"))

# function to load the model
def load_model():
    global clf
    clf = pickle.load(open("models/news_classifier.pkl", "rb"))
    # load data if empty
    if articles.count() == 0:
        with open("/app/data/news_new.json", encoding = 'utf-8') as f:
            data = json.load(f)
            articles.insert_many(data)


# function to predict the flower using the model
def predict(query_data):
    x = list(query_data.dict().values())

    print(x)

    df = pd.DataFrame(x, columns=['data'])
    df['data'] = df['data'].apply(process_text)

    x_new_counts = count_vect.transform(df.data)
    x_new_tfidf = tfidf.transform(x_new_counts)

    res = clf.predict(x_new_tfidf)
    #prediction = le.inverse_transform(res)[0]
    prediction = category_list[res[0]]
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

    news_data = []
    for data in articles.find({}):
        news_data.append(data)
    
    data = pd.DataFrame(news_data)

    if len(data) > 0:
        data['summary'] = data['short_description'].apply(process_text)
        cat_list = [category_list.index(i) for i in data['category']]
        data['flag'] = cat_list

        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(data.summary)

        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

        _,X_test,_,y_test = train_test_split(X_train_tfidf, data.flag,
                                                            test_size=0.25, random_state=9)

        clf = svm.LinearSVC()  # Initializing the model instance
        clf.fit(X_train_tfidf, data.flag)  # Training the model

        # Saving the model
        pickle.dump(clf, open('models/news_classifier.pkl', 'wb'))
        pickle.dump(count_vect, open('models/count_vector.pkl', 'wb'))
        pickle.dump(tfidf_transformer, open('models/tfidf.pkl', 'wb'))

        model_predictions = clf.predict(X_test)
        acc = accuracy_score(y_test, model_predictions) * 100

        return {
            "message": "Training Successful",
            "accuracy": acc}

    return {"message" : "Not enough new data to train"}