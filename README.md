# News Classification - Capstone Project - Team Hydra

### Team Members
1. Ameer Sohail Shaik
2. Pavan Krishna

### Service description
Docker container with a seperate container for : 
1. zookeeper
2. broker
3. flask-streamer
4. mongo
5. spark

### Container description
#### zookeeper
Description : Kafka Zookeeper Service running to support the kafka streaming service
Port : 2181

#### broker
Description : Kafka Broker Service running to support the kafka streaming service
Port : 9092

#### flask-streamer
Description : Front End Application running on Flask - Streams data on request
Port : 5000

#### mongo
Description : MongoDB Server for database
Port : 27017

#### spark
Description : Backend Application running on FastAPI - Runs Spark code on demand - Classifies and Trains data
Port : 9999

### Model
Model Used : SVM + Calibrated Classifier CV
Accuracy : 75%

### Command to start server
`docker-compose up`
