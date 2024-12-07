# Copyright 2016 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Creates a deployment using AppsV1Api from file nginx-deployment.yaml.
"""

from os import path

import yaml

from kubernetes import client, config
try : 
    config.load_kube_config()
    k8s_apps_v1 = client.AppsV1Api()
    print(f"Kubes cluter loaded sucessfully !!!w")
except Exception as e : 
    print(f"Failed to load local kubernetes cluster {e}")

def create_deployment():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
   

    with open(path.join(path.dirname(__file__), "nginx-deployment.yaml")) as f:
        dep = yaml.safe_load(f)#yaml thing not a kube thing
        
        print("og replicas : ")
        print(dep['spec']['replicas'])
        dep['spec']['replicas']=3# you can set it up when it doesn't exist but you cant' change it
        #when it already exists might need to look into scale api
        print(f"changed replicas : {dep['spec']['replicas']}") #we can change a file stuff before 
        #deploying it 
        resp = k8s_apps_v1.create_namespaced_deployment(
            body=dep, namespace="team13")
        print(f"Deployment created. Status='{resp.metadata.name}'")
        return (resp.metadata.name,3)

def scale_deployment(name,replicas) :
    #scale_request =client.V1ScaleSpec(replicas=replicas)#scale request doesn't seem to work
    patch = {
    'spec': {
        'replicas': replicas
        }
    }#this works
    return k8s_apps_v1.patch_namespaced_deployment_scale(name,"team13" , patch)

def test(name,replicas):
    string = f'name is {name} and replicas are {replicas}'
    print (string)
    return string

if __name__ == '__main__':
    name='nginx-deployment'#use the metadata name
    replicas=3# this wprks
    try:
        create_deployment()
    except Exception as e:
        print(f"Creation exception : {e}")
    try:
        scale=scale_deployment(name,replicas)
        print(f"Deployment Scale successfule : {scale.status}")
    except Exception as e:
        print(f"Deployment exception : {e}")
    
    
