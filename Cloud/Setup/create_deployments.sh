cd ..
cd Kubernetes
kubectl apply -f apachezk-deployment.yaml -n team13
kubectl apply -f apachekafka-deployment.yaml -n team13
kubectl apply -f ml_server.yaml -n team13
kubectl apply -f couchdb-deployment.yaml -n team13
cd ..
cd Setup