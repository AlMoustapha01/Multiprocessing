import pika  
import json  
from django.conf import settings
from .models import Article

connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_HOST))  
channel = connection.channel()
channel.queue_declare(queue=settings.QUEUE_TOPIC)
article = list(Article.objects.values())

message = json.dumps(article)  
channel.basic_publish(exchange='', routing_key=settings.QUEUE_TOPIC, body=message) 

print(" [x] Sent data to RabbitMQ") 

connection.close()  