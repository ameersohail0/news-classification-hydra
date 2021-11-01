FROM ubuntu:18.04
LABEL team="Hydra"

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV DISPLAY=:99

SHELL ["/bin/bash", "-c"]

# Install apt dependencies
RUN apt update

# Install dependencies
RUN apt install -y dos2unix
RUN apt install wget -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install openjdk-8-jdk -y
RUN apt install scala -y
RUN apt install python3-lxml -y
RUN pip3 install pyspark==2.4.6
RUN pip3 install nltk
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install scikit-learn
RUN pip3 install bs4
RUN pip3 install lxml

# Install PyMongo
RUN pip3 install pymongo

# Install fastAPI
RUN pip3 install uvicorn==0.14.0
RUN pip3 install fastapi==0.68.0
RUN pip3 install requests==2.21.0

RUN pip3 install sklearn

# Installing XGBoost
# RUN apt install cmake -y
# RUN pip3 install --upgrade pip
# RUN pip3 install --upgrade setuptools
# RUN pip3 install ez_setup
# RUN pip3 install wheel
# RUN pip3 install sklearn
# RUN pip3 install xgboost

# Downloading Spark
RUN wget https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz
RUN tar -xvf spark-2.4.8-bin-hadoop2.7.tgz
RUN mv spark-2.4.8-bin-hadoop2.7.tgz spark
# RUN rm spark-2.4.8-bin-hadoop2.7.tgz

# RUN wget https://mirrors.estointernet.in/apache/spark/spark-3.1.2/spark-3.1.2-bin-hadoop2.7.tgz
# RUN tar -xvf spark-3.1.2-bin-hadoop2.7.tgz
# RUN mv spark-3.1.2-bin-hadoop2.7 spark
# RUN rm spark-3.1.2-bin-hadoop2.7.tgz

# Downloading Spark Streaming Kafka
RUN wget https://search.maven.org/remotecontent?filepath=org/apache/spark/spark-streaming-kafka-0-8-assembly_2.11/2.4.8/spark-streaming-kafka-0-8-assembly_2.11-2.4.8.jar -O spark-streaming-kafka-0-8-assembly_2.11-2.4.8.jar

# Backup original bashrc
RUN cp ~/.bashrc ~/.bashrc.bak

# adding spark_config script
COPY spark_config.sh /app/spark_config.sh
RUN chmod u+x /app/spark_config.sh
RUN dos2unix /app/spark_config.sh
RUN /app/spark_config.sh


ENV PYSPARK_PYTHON python3

COPY main.py /app/main.py
COPY utils.py /app/utils.py
RUN mkdir models

COPY scrapping.py /app/scrapping.py
COPY models/news_classifier.pkl /app/models/news_classifier.pkl
COPY models/news_classifier_softmax.pkl /app/models/news_classifier_softmax.pkl
COPY models/news_classifier_nb.pkl /app/models/news_classifier_nb.pkl
COPY models/count_vector.pkl /app/models/count_vector.pkl
COPY models/tfidf.pkl /app/models/tfidf.pkl

RUN mkdir data
COPY data/news_db.json /app/data/news_db.json
COPY data/news_new.json /app/data/news_new.json

# # Application code
COPY transformer.py /app/transformer.py


# COPY XGBoost_model.pkl /app/XGBoost_model.pkl

COPY start_spark.sh /app/start_spark.sh
RUN chmod u+x /app/start_spark.sh
RUN dos2unix /app/start_spark.sh

CMD ["/bin/bash","-c","/app/start_spark.sh"]

# CMD ["/bin/bash"]