#! /bin/bash

sleep 10
cd /app
mongoimport --collection=articles --db=news-db /app/news_articles.json
python3 /app/news_stream.py