import sys
import os
import time
import paho.mqtt.client as mqtt

import math

# python3 botcontrol.py localhost 1883 abotcmd1 1.0 30.0 path.txt


# collecting params from input
broker = sys.argv[1]
port = int(sys.argv[2])
topic = sys.argv[3]

speed = float(sys.argv[4])
angle_speed = float(sys.argv[5])
file_path = sys.argv[6]

coords = []     # массив координат
lengths = []    # array of lengths beetwen points
road_time = []    # time of moving between points
angles = [0]    # list of angles between points


def check():
    print("Argv params:")
    print(f'ip: {ip}')
    print(f'port: {port}')
    print(f'topic: {topic}')
    print(f'speed: {speed}')
    print(f'angle speed: {angle_speed}')
    print(f'file with path: {file_path}')

    for i in range(1, len(coords)):
        print('-' * 60)
        print(f'mooving from: {coords[i - 1]} to {coords[i]}')
        if angles[i - 1] > 180:
            print(f'len: {lengths[i - 1]} | angle: {abs(360 - angles[i - 1])} | time: {road_time[i - 1]} | RIGHT')
        else:
            print(f'len: {lengths[i - 1]} | angle: {angles[i - 1]} | time: {road_time[i - 1]} | LEFT')


# mqtt connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected with res code {str(rc)}")
    print(f"Subscribed on topic: {topic}")


def publish(client, msg):
    res = client.publish(topic, msg)
    if res[0]:
        print(f"Failed to send msg to topic {topic}")
    else:
        print(f"Sending msg: {msg} | to topic {topic}")


# reading points from file 
if not os.path.exists(file_path):
    print('File not found')
else:
    with open(file_path) as file:
        lines = file.readlines()


# calculating distance between curr point and next
def calculate_length(start, destiny):   
    return round(((destiny[0] - start[0]) ** 2 + (destiny[1] - start[1]) ** 2) ** 0.5, 3)

# transforming coordinates into 2x list
for coord in lines:
    coords.append([float(i) for i in coord.split()])


# calculate lengths between all points 
for i in range(1, len(coords)):
    lengths.append(calculate_length(coords[i - 1], coords[i]))


# calculates angle between 2 points
def calculate_angle(start, destiny, prev_angle=0):
    if start[0] == 0: # change start pos of bot to (1, 0)
        start[0] = 1.0
    if destiny[0] == 0:
        destiny[0] = 1.0

    x1, y1 = start
    x2, y2 = destiny
    inner = x1 * x2 + y1 * y2

    if x2 == 0 and y2 == 0: # if mooving to (0, 0)
        return abs(prev_angle - 180)

    mod_of_vectors = math.sqrt(x1 ** 2 + y1 ** 2) * math.sqrt(x2 ** 2 + y2 ** 2)
    angle = inner / mod_of_vectors
    return math.degrees(math.acos(angle)) + prev_angle


# calculates all angles between all points
def calculate_all_angles():
    for i in range(1, len(coords)):
        angles.append(calculate_angle(coords[i - 1], coords[i], angles[i - 1]))
    del angles[0]

calculate_all_angles()


# calculating time between points (movement forward and angle changing)
for i in range(len(lengths)):
    time_move_straight = round(lengths[i] / speed, 3)
    time_change_angle = round(angles[i] / angle_speed, 3)

    road_time.append([time_move_straight, time_change_angle, round(time_move_straight + time_change_angle, 3)])
    # [[move_time, rotate_time, all_time], ...]


# sending commands to mqtt topic
def send_cmd(cmd, client, val=0):
    if cmd == "forward":
        msg = '{"cmd": "forward", "val": "' + str(val) + '"}'
        publish(client, msg)
        #print(msg)
        time.sleep(val) 
    if cmd == "back":
        msg = '{"cmd": "back", "val": "' + str(val) + '"}'
        publish(client, msg)
        time.sleep(val) 
    if cmd == "left":
        msg = '{"cmd": "left", "val": "' + str(val) + '"}'
        publish(client, msg)
        time.sleep(val) 
    if cmd == "right":
        msg = '{"cmd": "right", "val": "' + str(val) + '"}'
        publish(client, msg)
        time.sleep(val) 
    if val == 0:
        msg = '{"cmd": "stop"}'
        publish(client, msg)



def main():
    client = mqtt.Client('bot_control_1')
    client.connect(broker, port)
    client.on_connect = on_connect
    print('^'*80)

    for i in range(1, len(road_time)):
        
        #sending commands to rotate
        if angles[i - 1] > 180:
            send_cmd('right', client, road_time[i][1])
        else:
            send_cmd('left', client, road_time[i][1])

        #sending cmd to move
        if angles[i - 1] < 2.5: # if angle too small then back 
            send_cmd('back', client, road_time[i][0])
        else:
            send_cmd('forward', client, road_time[i][0])

        #cmd to stop
        send_cmd('stop', client)

    client.disconnect()


if __name__ == '__main__':

    main()
