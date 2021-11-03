#! /usr/bin/python3                                                                                                                                                                                                         

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import json

# # MongoDB Setup
from pymongo import MongoClient

client = MongoClient('mongo', 27017)

db = client['news_db']

articles = db['articles']


def handle_rdd(rdd):
    if not rdd.isEmpty():
        try:
            global ss
            df = ss.createDataFrame(rdd, schema=['category', 'short_description'])
            df.show()
            # df.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").option("spark.mongodb.input.uri","mongodb://mongo:27017/news-db.articles").save()
            # df.write.saveAsTable(name='news_db.articles', format='mongo', mode='append')
            # df.write.format("mongo").mode("append").option("database","news_db").option("collection", "articles").save()
            results = df.toJSON().map(lambda j: json.loads(j)).collect()
            if len(results) > 1:
                articles.insert_many(results)
            elif len(results) == 1:
                articles.insert(results)
        except Exception as e:
            print("error occurred: ", e)

sc = SparkContext(appName="NEWSTRAINER")
ssc = StreamingContext(sc, 5)

ks = KafkaUtils.createDirectStream(ssc, ['news-trainer'], {'metadata.broker.list': 'broker:9092'})

lines = ks.map(lambda x: x[1])

print(lines)

ss = SparkSession \
    .builder \
    .appName("NEWSTRAINER") \
    .config("spark.mongodb.input.uri", "mongodb://mongo:27017/news_db.articles") \
    .config("spark.mongodb.output.uri", "mongodb://mongo:27017/news_db.articles") \
    .getOrCreate()

ss.sparkContext.setLogLevel('WARN')


transform = lines.map(lambda data: (data.split("//")[0], data.split("//")[1]))

transform.foreachRDD(handle_rdd)

ssc.start()
ssc.awaitTermination()
