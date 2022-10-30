import os
import paho.mqtt.client as mqtt


broker = 'localhost'
port = 1883
topic = 'test/topic1'
data = []
t = 2


def count_average(num):
    global t
    data.append(float(num))
    if len(data) >= 3:
        res = data[t] * 0.6 + data[t-1] * 0.3 + data[t-2] * 0.1
        t += 1
        print(f'Average: {round(res, 3)}')


def on_message(client, userdata, msg):
    #print("Msg received: " + msg.topic + " " + str(msg.payload.decode("utf-8"))) 
   # print(message.topic)
    count_average(msg.payload.decode("utf-8"))


def on_connect(client, userdata, flags, rc):
    print(f"Connected with res code: {str(rc)}")
    print(f"Subscriber connected to topic: {topic}")



def main():
    client = mqtt.Client("sub_test_1")
    client.connect(broker, port)  # connecting to topic
    client.subscribe(topic)        # subscribing to topic 
    client.on_connect = on_connect  # on connect
    client.on_message = on_message  # on msg

    client.loop_forever()       # looping 


if __name__ == '__main__':

    main()
    
 