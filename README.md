# SnapSorter
A streamlined Kubernetes-based microservice that uses Python-driven
ML to classify and store images, with Docker and Ansible enhancing
deployment and management. .

## Cloud Deployment : 
- We've deployed our program in chameleon cloud as part of our class project for Principles of Cloud Computing. 
- Please ask Professor Aniruddha Gokhale for the ssh keys to access the cloud. 
- Please not that the VM's might be deprovisioned by Professor Aniruddha Gokhale and I'm working on a minikube version of our application.
- You need to install kubernetes and a private docker registry in your application docker and Python 3.9.x or above
- Build All our Images : run create_images.sh
- Deploy your pods :
  1. run Cloud/Setup/create_deployments.sh
  2. run Cloud/Setup/create_jobs.sh


