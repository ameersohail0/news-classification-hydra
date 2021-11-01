#! /usr/bin/python3                                                                                                                                                                                                         

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


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
            df.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").option("spark.mongodb.input.uri",
                                                                                           "mongodb://mongo:27017/news-db.articles").save()
            # df.write.saveAsTable(name='news_db.articles', format='mongo', mode='append')
            # df.write.format("mongo").mode("append").option("database","news_db").option("collection", "articles").save()
            # results = df.toJSON().map(lambda j: json.loads(j)).collect()
            # print(results)
            # if len(results) > 1:
            #     articles.insert_many(results)
            # elif len(results) == 1:
            #     articles.insert(results)
        except Exception as e:
            print("error occurred: ", e)

sc = SparkContext(appName="NEWSTRAINER")
ssc = StreamingContext(sc, 5)

ks = KafkaUtils.createDirectStream(ssc, ['news-trainer'], {'metadata.broker.list': 'broker:9092'})

lines = ks.map(lambda x: x[1])

print(lines)

# ss = SparkSession.builder.appName("NEWSTRAINER").config("spark.sql.warehouse.dir", "/user/hve/warehouse").config("hive.metastore.uris", "thrift://hadoop_hive:9083").enableHiveSupport().getOrCreate()

# ss = SparkSession.builder.appName("NEWSTRAINER").config("spark.mongodb.input.uri", "mongodb://mongo:27017/news-db.articles").config("spark.mongodb.output.uri", "mongodb://mongo:27017/news-db.articles").getOrCreate()                                                                                                                     

ss = SparkSession \
    .builder \
    .appName("NEWSTRAINER") \
    .config("spark.mongodb.input.uri", "mongodb://mongo:27017/news_db.articles") \
    .config("spark.mongodb.output.uri", "mongodb://mongo:27017/news_db.articles") \
    .getOrCreate()
    # .config("spark.mongodb.input.uri", "mongodb://"+os.environ['MONGO_SERVER']+"/news_db.articles") \
    # .config("spark.mongodb.output.uri", "mongodb://"+os.environ['MONGO_SERVER']+"/news_db.articles") \

ss.sparkContext.setLogLevel('WARN')

# ks = KafkaUtils.createDirectStream(ssc, ['news-trainer'], {'metadata.broker.list': 'broker:9092'})                       

# lines = ks.map(lambda x: x[1])

# print(lines)

transform = lines.map(lambda data: (data.split("//")[0], data.split("//")[1]))

transform.foreachRDD(handle_rdd)

ssc.start()
ssc.awaitTermination()

# CREATE TABLE nycparkingtickets (text STRING, words INT, length INT, text STRING) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\|' STORED AS TEXTFILE;
