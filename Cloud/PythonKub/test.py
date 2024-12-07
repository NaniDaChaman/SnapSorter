from kubernetes import client, config

try :
    config.load_kube_config()
    print("Loaded local env")
    v1 = client.AppsV1Api()
except Exception as e:
    print(f"couldn't load local env :{e}")

try :
    config.load_incluster_config()
    print("Loaded remote env")
    v1 = client.CoreV1Api()
except Exception as e:
    print(f"couldn't load remote env :{e}")


def sanity_check():
    
    print("\n\nNodes we have : \n\n")
    print(v1.list_node())
    print("\n\nNamespaces we have : \n\n")
    print(v1.list_namespace())
    print("\n\nPods we have : \n\n")
    print(v1.list_namespaced_pod(namespace='team13'))

def create_nginx():
    metadata = client.V1ObjectMeta(name='nginx-deployment')
    container1 = client.V1Container(name='nginx', image='nginx:1.14.2',ports=[client.V1ContainerPort(80)])#contaier part of spec
    #how can we add containerport
    containers=[container1]
    pod_spec = client.V1PodSpec(containers=containers)
    #how do we add replicas to pod spec
    pod_body = client.V1Pod(metadata=metadata, spec=pod_spec, kind='Deployment', api_version='apps.v1')
    pod = v1.create_namespaced_deployment(namespace='team13', body=pod_body)#diff functions for the type of pod/resource type you want to create

try:    
    #sanity_check()
    print("Sanity check is working ")
except Exception as e:
    print(f"Exception at Sanity Check : {e}")

try:    
    create_nginx()
except Exception as e:
    print(f"Exception at Creating Nginx : {e}")
