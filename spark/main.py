import uvicorn
import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import scrapping
from flask import jsonify

from utils import load_model, predict, train_model, transformer

# defining the main app
app = FastAPI(title="PySpark News Classifier", docs_url="/")

# calling the load_model during startup.
# this will train the model and keep it loaded for prediction.
app.add_event_handler("startup", load_model)

# class which is expected in the payload
class QueryIn(BaseModel):
    url: str


# class which is returned in the response
class QueryOut(BaseModel):
    topic: str

# class TrainIn(BaseModel):
#     summary: str
#     topic: str

class DataIn(BaseModel):
    timeout: int

# Route definitions
@app.get("/ping")
# Healthcheck route to ensure that the API is up and running
def ping():
    return {"ping": "pong"}


@app.post("/classify_news", response_model=QueryOut, status_code=200)
# Route to do the classifcation using the ML model defined.
# Payload: QueryIn containing the parameters
# Response: QueryOut containing the topic of news predicted (200)
def classify_news(query_url: QueryIn):
    df, original_data, final_res = scrapping.web_scrapping(str(query_url))
    predictions, probs = predict(df)

    return jsonify({"pred": predictions, "probs": probs, "o_data": original_data})



@app.post("/add_news", status_code=200)
# Route to further train the model based on user input in form of feedback loop
# Payload: FeedbackIn containing the parameters and correct news topic
# Response: Dict with detail confirming success (200)
def add_news(data: DataIn):
    transformer(data)
    # response = requests.post("/reload_model")
    return {"message" : "news added to database successfully"}

@app.post("/train", status_code=200)
# Route to further train the model based on user input in form of feedback loop
# Payload: FeedbackIn containing the parameters and correct news topic
# Response: Dict with detail confirming success (200)
def train():
    resp = train_model()
    return resp

# Main function to start the app when main.py is called
if __name__ == "__main__":
    # Uvicorn is used to run the server and listen for incoming API requests on 0.0.0.0:8888
    uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True)