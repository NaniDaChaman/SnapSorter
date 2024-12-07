from flask import Flask,jsonify,request,url_for,render_template,redirect,Response
import json
import deploy
import datetime
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

app =Flask(__name__)
df=pd.DataFrame(columns=['Replicas','Response Time','Reward','Time'])
start_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
@app.route("/scale",methods=['POST'])
def scale_up():
    r=request
    response=json.loads(r.data)
    name=response['name']
    replicas=response['replicas']
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    new_row=[replicas,response['response'],response['reward'],current_time]
    df.loc[len(df)]=new_row
    df.to_csv(f'Autoscale_Monitoring_{start_time}')
    fig,(ax1,ax2,ax3)=plt.subplots(1,3,sharex=True,figsize=(15,5))
    ax1.set_title('Replicas')
    ax2.set_title('Response Time')
    ax3.set_title('Reward')

    ax1.plot(df['Time'],df['Replicas'],color='Red')
    ax2.plot(df['Time'],df['Response Time'])
    ax3.plot(df['Time'],df['Reward'],color='Green')
    fig.savefig(f'Autoscale_Monitoring_{start_time}.png')
    #df[current_time]={'Replicas':replicas,'Response Time':response['response'],'Reward':response['reward']}
    scale=deploy.scale_deployment(name,replicas)
    try :
        name_deployment=scale.metadata.name
        new_count=scale.spec.replicas
        old_count=scale.status.replicas
        data={"name":name_deployment,"old_count":old_count,"new_count":new_count}
        return jsonify(data)
    except Exception as e :
        print(f'Error occured when scaling the resource : {name}')
        print(e)
        return jsonify({}),500

@app.route("/scale_test/<string:name>/<int:replicas>",methods=['GET'])
def scale_up_test(name,replicas):
    #r=request
    #response=json.loads(r.data)
    #name=response['name']
    #replicas=response['replicas']
    response=deploy.test(name,replicas)
    data={'response':response}
    return jsonify(data),200

if __name__=="__main__":
    app.run(host = '0.0.0.0',port =5010)


