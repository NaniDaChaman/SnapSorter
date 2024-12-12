
cd ..
cd Kubernetes
kubectl delete -f producer-job.yaml -n team13
kubectl delete -f ml_server.yaml -n team13
kubectl delete -f mlconsumer-job.yaml -n team13
kubectl delete -f apachezk-deployment.yaml -n team13
kubectl delete -f apachekafka-deployment.yaml -n team13
kubectl delete -f couchdbconsumer-job.yaml -n team13
kubectl delete -f couchdb-deployment.yaml -n team13
kubectl delete -f arima-test.yaml -n team13
cd ..
cd Setup