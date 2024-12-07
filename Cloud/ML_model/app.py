from flask import Flask,jsonify,request,url_for,render_template,redirect,Response
import model as md
import numpy as np
from PIL import Image
import json
import base64
from io import BytesIO
#import jsonpickle


app= Flask(__name__)
@app.route("/get_pred/<filename>")
def get_pred(filename):
    prediction = md.model_pred(md.model_prob(filename))
    data={"Prediction" : prediction}
    return jsonify(data)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/handle_form",methods=["POST"])
def handle_form():
    #return "You did it"
    ufile=request.form['image']
    #print(ufile)
   
    #print(ufile.filename)
    
    return redirect(url_for("get_pred",filename=ufile))

@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    #parr = np.fromstring(r.data, np.uint8)
    # decode image
    response=json.loads(r.data)
    img_str= response['image']
    img_bytes = base64.b64decode(img_str)
    img = Image.open(BytesIO(img_bytes))
    # do some fancy processing here....
    prediction = md.model_pred(md.model_prob_img(img))
    data={"Prediction" : prediction}
    return jsonify(data)
    # build a response dict to send back to client
    #response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                #}
    # encode response using jsonpickle
    #response_pickled = jsonpickle.encode(response)

    #return Response(response=response_pickled, status=200, mimetype="application/json")


if __name__=="__main__":
    md.load_model()
    #url_for("hello_world")
    app.run(host = '0.0.0.0',port =5001)