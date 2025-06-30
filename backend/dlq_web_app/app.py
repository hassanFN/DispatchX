from flask import Flask, render_template
from confluent_kafka import Consumer
import os 
import json

#----------Config---------#
BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
GROUP_ID = os.getenv("GROUP_ID", "DLQ_GROUP")
TOPIC = os.getenv("DLQ_TOPIC", "DLQ_TOPIC")
#--------------------------

#------Function for deserialization--------#
def value_deserializer(data):
        return data.decode("utf-8") if data else None
#-------------------------------------------#

app = Flask(__name__)

@app.route("/")


def index():

    consumer_config = {
    "bootstrap.servers": BOOTSTRAP,
    "group.id": GROUP_ID,
    "auto.offset.reset": "earliest"
}
   
    consumer  = Consumer(consumer_config)
    consumer.subscribe([TOPIC])
    messages = []
    print(f'Subscribed to {TOPIC} and read to poll messages')
    for i in range(5):
          message = consumer.poll(timeout=1.0)
          if message is not None and message.value() is not None:
            print(f'Got a message. Message is now deserializing!')
            try:
                messages.append(json.loads(value_deserializer(message.value())))
                print("Message was Deserialized successfully!")
            except Exception as e:
                 print(f'failed to decode message: {e}')
    consumer.close()
    return render_template("index.html", messages=messages)
    

    
     


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)




