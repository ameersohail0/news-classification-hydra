#! /usr/bin/python3                                                                                                                                                                                                         
                                                                                                                        
from pyspark import SparkContext                                                                                        
from pyspark.sql import SparkSession                                                                                    
from pyspark.streaming import StreamingContext                                                                          
from pyspark.streaming.kafka import KafkaUtils               
import pickle
import pandas as pd
import numpy as np

def handle_rdd(rdd):                                                                                                    
    if not rdd.isEmpty():                                                                                               
        global ss                                                                                                       
        df = ss.createDataFrame(rdd, schema=['PLATE_ID', 'REGISTRATION_STATE', 'VIOLATION_CODE', 'VIOLATION_PRECINCT', 'ISSUER_PRECINCT', 'ISSUER_CODE', 'LAW_SECTION', 'SUB_DIVISION', 'VEHICLE_YEAR', 'FEET_FROM_CURB', 'VIOLATION_LOCATION'])                                                
        df.show()                                                                                                       
        df.write.saveAsTable(name='default.nycparkingtickets', format='hive', mode='append')    
                           
def predict_location(data):
    model = pickle.load(open('XGBoost_model.pkl',"rb"))[0]
    data = data.split()
    X = pd.DataFrame([data])
    prediction = model.predict(X)

    return int(prediction[0])
                                                                                                                        
sc = SparkContext(appName="NYCPARKINGTICKETS")                                                                                     
ssc = StreamingContext(sc, 5)                                                                                           
                                                                                                                 
ss = SparkSession.builder.appName("NYCPARKINGTICKETS").config("spark.sql.warehouse.dir", "/user/hve/warehouse").config("hive.metastore.uris", "thrift://hadoop_hive:9083").enableHiveSupport().getOrCreate()                                                                                                  
                                                                                                                        
ss.sparkContext.setLogLevel('WARN')            
                                                                                                            
ks = KafkaUtils.createDirectStream(ssc, ['nycparkingtickets'], {'metadata.broker.list': 'broker:9092'})                       
                                                                                                                 
lines = ks.map(lambda x: x[1])                                                                                          
                                                                                                            
transform = lines.map(lambda data: (int(data.split()[0]), int(data.split()[1]), int(data.split()[2]), int(data.split()[3]), int(data.split()[4]), int(data.split()[5]), int(data.split()[6]), int(data.split()[7]), int(data.split()[8]), int(data.split()[9]), predict_location(data)))

transform.foreachRDD(handle_rdd)                                                                                      
                                                                                                                        
ssc.start()                                                                                                             
ssc.awaitTermination()

# CREATE TABLE nycparkingtickets (text STRING, words INT, length INT, text STRING) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\|' STORED AS TEXTFILE;