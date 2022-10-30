import os
import paho.mqtt.client as mqtt
import time


broker = 'localhost'
port = 1883
topic = 'test/topic1'


def read_data_from_file():
    #os.chdir('/home/toor/ITS_MAI/task4/')
    readpath = '/home/toor/ITS_MAI/task4/data.txt'  # path to file 
    if not os.path.exists(readpath):
        print('File not found')
    else:
        with open(readpath) as f:
            #contents = f.read()
            contents = f.readlines()
            return contents


def system_command(cmd):
    os.system(cmd)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(userdata)))
    print(f"Publisher connected to topic: {topic}")


def publish(client, msg):
    content = read_data_from_file()
    for val in content:
       # print(f"Send: {val[:-1]}")
        res = client.publish(topic, val[:-1])
        if res[0]:
            print(f"Failed to send msg to topic {topic}")
        else:
            print(f"Send {val[:-1]} to topic {topic}")
        time.sleep(2)


def main():
    content_from_file = read_data_from_file()  # read data from txt
    client = mqtt.Client("pub_test_1")         # 
    client.connect(broker, port)               # connecting to broker
    client.on_connect = on_connect             # checking connection
    publish(client, content_from_file)         # publishing msg to topic
    client.disconnect()

if __name__ == '__main__':
    #print(os.getcwd())
    #print(os.listdir())
    #read_data_from_file()
    
    main()
    

    # content_from_file = read_data_from_file()
    # print(content_from_file)
    
    


    #client.connect("m2m.eclipse.org", 1883, 60)

    #client.loop_forever()

