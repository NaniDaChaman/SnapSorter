import json
import base64
from kafka import KafkaConsumer, KafkaProducer
from PIL import Image
from io import BytesIO
# import torch
# import torchvision.transforms as transforms
# import torchvision.models as models
import requests
url = "/get_pred/dog.jpg"

CIFAR10_LABELS = [
    'airplane', 'automobile', 'bird', 'cat', 'deer', 
    'dog', 'frog', 'horse', 'ship', 'truck'
]

consumer = KafkaConsumer(
    'iot-topic',
    bootstrap_servers="172.16.2.137:30000",  
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),  
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='ml-inference-group'  
)
# subscribe to iot-topic
consumer.subscribe (topics=["iot-topic"])
print("Kafka consumer initialized successfully.")

producer = KafkaProducer(
    bootstrap_servers="172.16.2.137:30000",  
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  
)

# model = models.resnet18(pretrained=True)
# model.fc = torch.nn.Linear(model.fc.in_features, len(CIFAR10_LABELS))
# model.eval()

# preprocess = transforms.Compose([
#     transforms.Resize((224, 224)),  
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
# ])

# def infer_image(image_base64):
#     image_data = base64.b64decode(image_base64)
#     image = Image.open(BytesIO(image_data)).convert("RGB")  

#     input_tensor = preprocess(image).unsqueeze(0)
#     with torch.no_grad():  
#         output = model(input_tensor)  
#         _, predicted_index = output.max(1)  

#     predicted_label = CIFAR10_LABELS[predicted_index.item()]  
#     return predicted_label

def infer_image_api(image):
    #img=Image.fromarray(image)
    #img.save(filename)
    #api and job is running on different pods 
    #they'll need the some kind of shared perminent storage to infer image
    #how will you do that!
    url = f"/api/test"
    response= requests.post(f"http://172.16.2.184:30004/{url}"#change the ip:host pairing to c2-w3
                            ,json={"image":image})#find a way to infer this
    print("\nImage looks like : \n")
    print(image)
    try :
        predicted_label=json.loads(response.text)['Prediction']#will response return a dict ?
        return predicted_label
    except Exception as e:
        print('Exeption occured one of the responses was not Json object')
        print(e)
        print(f'Response status code : {response.status_code}')
        print(f'Response status code : {response.text}')
#w/o the need for us having to see kubectl get pods

def send_inference_result_to_database(image_id, predicted_label, producer_id):
    result_data = {
        "ID": image_id,
        "InferredValue": predicted_label
    }
    producer.send('iot-predictions', value=result_data)
    producer.flush()  
    print(f"Sent inference result (with label) for image ID {image_id} to Kafka 'iot-predictions'.")

def send_inference_result_to_producer(image_id, producer_id):
    result_data = {
        "ID": image_id,
        "producer_id": producer_id  
    }
    print(f"Sending result data to producer: {result_data}")  # 打印发送前的数据
    producer.send('time-topic', value=result_data)
    producer.flush()  
    print(f"Sent inference result (ID and producer ID) for image ID {image_id} to Kafka 'time-topic'.")

try:
    for message in consumer:
        data = message.value  
        print(f"Received data from Kafka with ID: {data['ID']}")

        image_base64 = data['Data']  
        producer_id = data['producer_id']  

        predicted_label = infer_image_api(image_base64)
        print(f"Predicted class for image with ID {data['ID']}: {predicted_label}")

        send_inference_result_to_database(data['ID'], predicted_label, producer_id)  
        send_inference_result_to_producer(data['ID'], producer_id)  

except Exception as e:
    print(f"Error consuming message or performing inference: {e}")
finally:
    #infer_image('123')
    consumer.close()
    producer.close()
    print("Kafka consumer and producer closed.")