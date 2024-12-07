import uuid
import json
import time
from kafka import KafkaProducer, KafkaConsumer
import numpy as np
from datetime import datetime,timedelta
import base64
import arima
import requests
import controller
#import kube_api there isn't a kube_config file inside the container !
#we'll have to send out a request to an api or something ! (we've seen this approach work but more work)
#we can try using kafka to send out our actions (we've not tried connecting kafka to non pod apps)

try:
    consumer = KafkaConsumer(
        'controller',
        bootstrap_servers='172.16.2.137:30000',#could we try and init in
        #dynamically with env vars set by kubernetes
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=f'controller-group',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    print("Kafka consumer started, listening for inference results.")

except Exception as e : 
    print(f"Error making the Kafka consumer : {e}")

addr='http://172.16.2.45:5010'
scale_url = addr + '/scale'

def controller_test(forecast_list):
    avg=np.average(forecast_list)
    if avg>15:
        replicas=5
    else : 
        replicas=3
    return replicas

start_time=None
n=0
arrival_list=[1,2,3,4,4,3,2,2,1]
forecast_list=[]
for message in consumer:
    data = message.value 
    time_now=datetime.fromisoformat(data['SentTime'])
    #print(f"\nData from kafka : {data}\n")
    time_horizon=10
    t_delta=11
    if n==0:
        start_time=time_now
        #print(f'\nNew start time is : {start_time}\n')
        n=n+1
    elif time_now>=start_time+timedelta(seconds=t_delta):
        arrival_list.append(n)
        #print(f"\nOur arrival list loos like : {arrival_list}\n")
        
        forecast_list=arima.get_prediction(np.array(arrival_list[-8:]),time_horizon)
        print(f"\nnext 10 forecast is : \n{forecast_list}\n")
        best_c,best_reward,best_st,best_rt,best_ql=controller.heuristic_single_step_lookahead_search(10,forecast_list,1,14,10,t_delta)
        #replicas=controller_test(forecast_list)
        print(f"Replicas to be created : {best_c}")
        try :
            req_body={'name':'mlmodel-deployment','replicas':best_c,'response':best_rt,'reward':best_reward}
            #scale=kube_api.scale_deployment('mlmodel-deployment',replicas)
            response=requests.post(scale_url,json=req_body)
            print(f"Effect of action : {json.loads(response.text)}")
            #print(f"Scaled ml deployment sucessfully : {scale}")
        except Exception as e : 
            print(f"Could not scale successfully : {e}")
        n=0
        start_time=time_now
    else :
        n=n+1
    
    
        
    #arrivals_list.append(data['SentTime'])
