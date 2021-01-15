import pika  
import json  
from django.conf import settings

connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_HOST))  
channel = connection.channel() 
channel.queue_declare(queue=settings.QUEUE_TOPIC) 

print(' [*] Waiting for messages. To exit press CTRL+C') 

def callback(ch, method, properties, body):  
    print("Method: {}".format(method))     
    print("Properties: {}".format(properties))     
    data = json.loads(body)     
    print("Data: {}".format(data))

channel.basic_consume(callback, queue=settings.QUEUE_TOPIC,no_ack=True)  
channel.start_consuming()  