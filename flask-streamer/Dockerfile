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
RUN pip3 install pandas
RUN pip3 install gdown
RUN pip3 install validators

# Install dotenv, requests
RUN pip3 install python-dotenv
RUN pip3 install requests

# Install Flask
RUN pip3 install flask

# Copy existing database
RUN mkdir /app/templates
RUN mkdir /app/static
COPY /templates /app/templates
COPY /static /app/static

# Copy existing database
COPY news_articles.json /app/news_articles.json

# Copy news stream
COPY news_streamer.py /app/news_streamer.py
COPY .env /app/.env

# adding kafka_create script
COPY kafka_create.sh /app/kafka_create.sh
RUN chmod u+x /app/kafka_create.sh
RUN dos2unix /app/kafka_create.sh

# adding news_stream script
COPY news_stream.sh /app/news_stream.sh
RUN chmod u+x /app/news_stream.sh
RUN dos2unix /app/news_stream.sh

# Application code
COPY app.py /app/app.py

# adding start_flask script
COPY start_flask.sh /app/start_flask.sh
RUN chmod u+x /app/start_flask.sh
RUN dos2unix /app/start_flask.sh

CMD  export LC_ALL=C.UTF-8 && export LANG=C.UTF-8 && /app/start_flask.sh

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# CMD /app/kafka_create.sh && /app/news_stream.sh