#!/usr/bin/env bash
cd ..
cdir=$(pwd)
echo "Current directory is $cdir"
declare -A images=([192.168.1.64:5000/couchdb]='CouchDB_Docker/Dockerfile.db' 
[192.168.1.64:5000/mlmodel]='ML_model/Dockerfile.ml_model'  
[192.168.1.64:5000/apachekafka]='Kafka_Docker/Kafka/Dockerfile' 
[192.168.1.64:5000/iot]='IOT/Dockerfile' 
[192.168.1.64:5000/mlconsumer]='ML_model/Dockerfile.consumer' 
[192.168.1.64:5000/couchdbconsumer]='CouchDB_Docker/Dockerfile.consumer')
for image in "${!images[@]}";
do 
pattern1="/*"
pattern2="*/"
dir=${images[$image]%$pattern1}
#echo "${images}">$dir
#echo "${dir}"
dkfile=${images[$image]##$pattern2}
##{images[$image]%$pattern1}
##{images[$image]##$pattern2}
echo "$image - directory : ${dir} image : ${dkfile} ";
#t1=$[-f ${images[$image]}] 
#echo $t1;
# cd $dir
# docker build -t $image  -f $dkfile .;
# docker push $image;
# docker rmi $image;
# cd $cdir

done