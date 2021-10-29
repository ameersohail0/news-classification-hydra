# Import libraries
import os, signal
import json
import time
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import re

import nltk
nltk.download('stopwords')
nltk.download('punkt')

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
count_vect = CountVectorizer(vocabulary=pickle.load(open("models/label_encoder.pkl", "rb")))
tfidf = pickle.load(open("models/tfidf.pkl", "rb"))

category_list = ['POLITICS', "WELLNESS", 'ENTERTAINMENT',
             "STYLE & BEAUTY", "TRAVEL", "PARENTING",
             "FOOD & DRINK", "QUEER VOICES", "HEALTHY LIVING",
             "BUSINESS", "COMEDY", "SPORTS", "HOME & LIVING",
             "BLACK VOICES", "THE WORLDPOST", "WEDDINGS", "PARENTS",
             "DIVORCE", "WOMEN", "IMPACT", "CRIME",
             "MEDIA", "WEIRD NEWS", "WORLD NEWS", "TECH",
             "GREEN", "TASTE", "RELIGION", "SCIENCE",
             "MONEY", "STYLE", "ARTS & CULTURE", "ENVIRONMENT",
             "WORLDPOST", "FIFTY", "GOOD NEWS", "LATINO VOICES",
             "CULTURE & ARTS", "COLLEGE", "EDUCATION", "ARTS"]


# function to load the model
def load_model():
    global clf
    clf = pickle.load(open("models/news_classifier.pkl", "rb"))
    # load data if empty
    if articles.count() == 0:
        with open("/app/data/news_db.json", encoding = 'utf-8') as f:
            data = json.load(f)
            articles.insert_many(data)


# function to predict the flower using the model
def predict(query_data):
    x = list(query_data.dict().values())
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
    from sklearn.preprocessing import LabelEncoder
    import pandas as pd
    from sklearn import svm

    # load the model
    # global clf
    # clf = pickle.load(open("models/news_classifier.pkl", "rb"))

    new_data = []
    for data in articles.find({}):
        new_data.append(data)
    
    data = pd.DataFrame(new_data)

    if len(data) > 0:
        data['summary'] = data['summary'].apply(process_text)
        cat_list = [category_list.index(i) for i in data['category']]
        data['flag'] = cat_list

        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(data.summary)

        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

        X_train, X_test, y_train, y_test = train_test_split(X_train_tfidf, data.flag,
                                                            test_size=0.25, random_state=9)

        clf_svm = svm.LinearSVC()  # Initializing the model instance
        clf_svm.fit(X_train_tfidf, data.flag)  # Training the model
        # Saving the model
        pickle.dump(clf_svm, open('models/news_classifier.pkl', 'wb'))

        model_predictions = clf.predict(X_test)
        acc = accuracy_score(y_test, model_predictions) * 100

        return {
            "message": "Training Successful",
            "accuracy": acc}


    # if len(data) > 0:
    #     data['len'] = data['summary'].str.len()
    #     data['summary_parsed'] = data['summary'].apply(process_text)
    #     data['topic_target'] = le.fit_transform(data['topic'])
    #
    #     X_train, X_test, y_train, y_test = train_test_split(
    #         data['summary_parsed'],
    #         data['topic_target'],
    #         test_size=0.2,
    #         random_state=8)
    #
    #     features_train = tfidf.transform(X_train).toarray()
    #     labels_train = y_train
    #
    #     features_test = tfidf.transform(X_test).toarray()
    #     labels_test = y_test
    #
    #     clf.fit(features_train, labels_train)
    #
    #     model_predictions = clf.predict(features_test)
    #     acc = accuracy_score(labels_test, model_predictions) * 100
    #     print('Accuracy: ', acc)
    #     print(classification_report(labels_test, model_predictions))
    #
    #     # save the model
    #     pickle.dump(clf, open("models/news_classifier.pkl", "wb"))
    #
    #     return {
    #         "message" : "Training Successful",
    #         "accuracy" : acc}

    return {"message" : "Not enough new data to train"}


def process_text(text):
    pattern = r'[0-9]'
    pattern2 = r'([\.0-9]+)$'
    text = str(text)
    text = re.sub(pattern, '', text)
    text = re.sub(pattern2, '', text)
    text = str(text)
    text = text.lower().replace('\n', ' ').replace('\r', '').strip()
    text = re.sub(' +', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    text = " ".join(filtered_sentence)
    return text

