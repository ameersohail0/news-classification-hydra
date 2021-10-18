/app/spark_config.sh
cd /app/
sleep 5

# spark-submit --conf "spark.mongodb.input.uri=mongodb://mongo:27017/news_db.articles?readPreference=primaryPreferred" --conf "spark.mongodb.output.uri=mongodb://mongo:27017/news_db.articles" --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.8.jar transformer.py

python3 main.py