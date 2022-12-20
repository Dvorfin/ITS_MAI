import paho.mqtt.client as mqtt
import os
import sys

# python3 botcontrol.py 10.0.2.2. 1883 abotcmd1 1.0 30.0 path.txt

# collecting params from input
broker = 'localhost'
port = 1883
topic = 'abotcmd1'

# python3 botcontrol.py localhost 1883 abotcmd1 

cmd = ''

def on_message(client, userdata, msg):
    print(str(msg.payload.decode("utf-8")))
    cmd = ''
    cmd = str(msg.payload.decode("utf-8"))


def on_connect(client, userdata, flags, rc):
    print(f"Connected with res code {str(rc)}")
    print(f"Subscribed on topic: {topic}")


def main():
    client = mqtt.Client("alpha_bot_1")
    client.connect(broker, port)
    client.subscribe(topic)

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()


if __name__ == '__main__':

    main()