# SnapSorter
A streamlined Kubernetes-based microservice that uses Python-driven
ML to classify and store images, with Docker and Ansible enhancing
deployment and management. .

## Cloud Deployment : 
- We've deployed our program in chameleon cloud as part of our class project for Principles of Cloud Computing. 
- Please ask Professor Aniruddha Gokhale for the ssh keys to access the cloud. 
- Please not that the VM's might be deprovisioned by Professor Aniruddha Gokhale and I'm working on a minikube version of our application.
- You need to install kubernetes and a private docker registry in your application docker and Python 3.9.x or above
- Deploying our application : 
 1. In the Kubernetes folder run : kubectl apply -f apachekafka-deployment.yaml apachezk-deployment.yaml ml_server.yaml mlconsumer-job.yaml producer-job.yaml couchdb-deployment.yaml couchdbconsumer-job.yaml -n team13
2. In the PythonKub Folder run : pip install -r requirments.txt
3. In the PythonKub Folder run : python app.py

