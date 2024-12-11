kubectl apply -f apachezk-deployment.yaml -n team13
kubectl apply -f apachekafka-deployment.yaml -n team13
kubectl apply -f ml_server.yaml -n team13
kubectl apply -f couchdb-deployment.yaml -n team13
sleep 5
kubectl get pods -n team13
kubectl apply -f mlconsumer-job.yaml -n team13
kubectl apply -f arima-test.yaml -n team13
kubectl apply -f producer-job.yaml -n team13