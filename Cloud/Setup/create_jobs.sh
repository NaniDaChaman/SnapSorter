cd ..
cd Kubernetes
kubectl apply -f mlconsumer-job.yaml -n team13
kubectl apply -f couchdbconsumer-job.yaml -n team13
#kubectl apply -f arima-test.yaml -n team13
kubectl apply -f producer-job.yaml -n team13
cd ..
cd Setup