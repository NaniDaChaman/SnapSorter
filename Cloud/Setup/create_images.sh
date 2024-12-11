#!/usr/bin/env bash
cd ..
#echo "$pwd"
declare -A images=(['192.168.1.64:5000/couchdb'] 'CouchDB_Docker/Dockerfile.db' 
['192.168.1.81:5000/mlmodel'] 'ML_model/Dockerfile.ml_model'  
['192.168.1.64:5000/apachekafka'] 'Kafka_Docker/Kafka/Dockerfile' 
['192.168.1.64:5000/iot'] 'IOT/Dockerfile' 
['192.168.1.81:5000/mlconsumer'] 'ML_model/Dockerfile.consumer' 
['192.168.1.64:5000/couchdbconsumer'] 'CouchDB_Docker/Dockerfile.consumer')
for image in "${!images[@]}";
do 
#echo "$image - ${images[$image]}";
#t1=$[-f ${images[$image]}] 
#echo $t1;
docker build -t $image  -f ${images[$image]};
docker push $image;
done