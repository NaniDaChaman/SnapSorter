kubectl delete -f arima-test.yaml -n team13
kubectl delete -f producer-job.yaml -n team13
kubectl delete -f ml_server.yaml -n team13
kubectl delete -f mlconsumer-job.yaml -n team13