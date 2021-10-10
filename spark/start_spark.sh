/app/spark_config.sh
cd /app/
sleep 60

spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.8.jar transformer.py