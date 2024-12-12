cd ..
cd Kubernetes
kubectl delete -f producer-job.yaml -n team13
kubectl delete -f arima-test.yaml -n team13
kubectl delete -f mlconsumer-job.yaml -n team13

kubectl apply -f producer-job.yaml -n team13
kubectl apply -f arima-test.yaml -n team13
kubectl apply -f mlconsumer-job.yaml -n team13