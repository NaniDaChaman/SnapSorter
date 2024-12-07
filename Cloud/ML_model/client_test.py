from __future__ import print_function
import requests
import json
from PIL import Image
import base64
from io import BytesIO

addr = 'http://localhost:5000'
test_url = addr + '/api/test'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = Image.open('dog.jpg')
buffered = BytesIO()
img.save(buffered, format="JPEG")
img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
print(f"Image encoded : {img}")
# encode image as jpeg
#_, img_encoded = cv2.imencode('.jpg', img)
# send http request with image and receive response
response = requests.post(test_url, json={'image':img_str})
# decode response
print(response.text)
print(json.loads(response.text))

# expected output: {u'message': u'image received. size=124x124'}