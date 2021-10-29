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
RUN apt install supervisor -y

# Downloading kafka
RUN wget https://archive.apache.org/dist/kafka/2.2.0/kafka_2.12-2.2.0.tgz
RUN tar -xvf kafka_2.12-2.2.0.tgz
RUN mv kafka_2.12-2.2.0 kafka
RUN rm kafka_2.12-2.2.0.tgz

# Install python-kafka
RUN pip3 install kafka-python

# adding zookeper script
COPY zookeper.sh /app/zookeper.sh
RUN chmod u+x /app/zookeper.sh
RUN dos2unix /app/zookeper.sh

CMD /app/zookeper.sh