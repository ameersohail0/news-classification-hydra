from flask import Flask,request
import requests
import os
import subprocess

app = Flask(__name__)

SPARK_SERVER = "http://spark:9999/"

@app.route("/")
def home():
    return "Home Page"

@app.route("/ping",methods=["GET","TRACE"])
def ping():
    if request.method == "GET":
        url = SPARK_SERVER + "ping"
        r = requests.get(url)
        return {'status':200, 'result':r.json()}
    elif request.method == "TRACE":
        return "ping trace method"

@app.route("/classify_news",methods=["POST","TRACE"])
def classify_news():
    given_request = request.get_json()
    if request.method == "POST":
        if {'summary'} == set(given_request.keys()):
            url = SPARK_SERVER + "classify_news"
            r = requests.post(url, json=given_request)
            return {'status':200, 'result':r.json()}
        else:
            return {'status':501, 'result':'all required keys are not given'}
    elif request.method == "TRACE":
        return given_request

@app.route("/add_news",methods=["POST","TRACE"])
def add_news():
    given_request = request.get_json()
    if request.method == "POST":
        if {'timeout','topic'} == set(given_request.keys()):
            topic = given_request.pop('topic')
            proc1 = subprocess.Popen(f"python3 /app/news_streamer.py '{topic}' {given_request['timeout']}", shell = True)
            url = SPARK_SERVER + "add_news"
            r = requests.post(url, json=given_request)
            return {'status':201, 'result':r.json()}
        else:
            return {'status':501, 'result':'all required keys are not given'}
    elif request.method == "TRACE":
        return given_request

@app.route("/train",methods=["POST","TRACE"])
def train():
    given_request = request.get_json()
    if request.method == "POST":
        url = SPARK_SERVER + "train"
        r = requests.post(url)
        return {'status':200, 'result':r.json()}
    elif request.method == "TRACE":
        return given_request

