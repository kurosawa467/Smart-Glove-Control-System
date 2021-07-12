import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import os
import csv
import errno
import datetime
import pandas
from training import SVMModel
import numpy as np
import pickle

MQTT_ADDRESS = '192.168.178.100'
MQTT_USER = 'mosquitto'
MQTT_PASSWORD = 'mosquitto'
GLOVE_TOPIC = '/esp32/glove'
IoT_TOPIC = ['/device1', '/device2', '/device3']
dim = 50
direction = 1
encoding = 'utf-8'
gesture = 'gesture'
header = ["timestamp", "yaw", "pitch", "row"]
sensor_data = []
sensor_data_matrix = []
filename_prefix = 'gesture_'
filename_index = 0
message_index = 0
start_time = 0
rf = None
rf_small = None
decision_tree_regressor = None
gesture_mode = 1

def on_connect(client, userdata, flags, rc):
    global rf
    global rf_small
    global decision_tree_regressor
    global start_time
    print('Connected with ESP32, result: ' + str(rc))
    client.subscribe(GLOVE_TOPIC)
    rf = pickle.load(open('random_forest.sav', 'rb'))
    rf_small = pickle.load(open('random_forest.sav', 'rb'))
    decision_tree_regressor = pickle.load(open('decision_tree_regressor.sav', 'rb'))
    print('machine learning models ready')
    start_time = datetime.datetime.now()
    print()


def on_message(client, userdata, msg):
    global start_time
    global message_index
    global filename_index
    global gesture_mode
    global sensor_data
    # print('Message topic: ' + msg.topic + ', message payload: ' + str(msg.payload))
    raw_message = str(msg.payload)
    message = raw_message[raw_message.index('=>') + 2:].rstrip("'")
    tokens = message.split(',')

    hand = get_finger_positions(tokens[:4])

    # Here decides when to start recording gesture
    if gesture_mode == 1:
        if hand == 1 or hand == 3:
            gesture_mode = 2
    if gesture_mode == 3:
        if hand == 15:
            gesture_mode = 1

    if gesture_mode == 2:
        if message_index == 0:
            print('Start to recognize gesture')
            print("hand start ", hand)
            sensor_data = []
        if message_index < 30:
            write_to_matrix(tokens[5:8])
            message_index += 1
        if message_index == 30:
            start_time = datetime.datetime.now()
            gesture = get_gesture_prediction()
            end_time = datetime.datetime.now()
            rf_time = (end_time - start_time).total_seconds()
            print("time", rf_time)
            hand = get_finger_positions(tokens[:4])
            print("hand end", hand)
            command = ''
            if hand == 1:
                if gesture == 1:
                    print("1 1")
                    command = 'next device'
                elif gesture == 2:
                    command = 'previous device'
                else:
                    print("1 3")
                    command = 'gesture unrecognized'
            elif hand == 3:
                if gesture == 1:
                    command = 'next color'
                elif gesture == 2:
                    command = 'previous color'
                elif gesture == 3:
                    command = 'higher brightness'
                elif gesture == 4:
                    command = 'lower brightness'
                else:
                    print("2 5")
                    command = 'gesture unrecognized'
            else:
                print("3 0")
                command = 'gesture unrecognized'
            print('Recognized command is: ' + command)
            message_index = 0
            filename_index += 1
            gesture_mode = 3

def write_to_matrix(tokens):
    global sensor_data
    current_time = (datetime.datetime.now() - start_time).total_seconds() * 1000
    row = [current_time]
    row += tokens
    sensor_data.append(row)
  
def matrix_transpose_and_flatten():
    global sensor_data
    global sensor_data_matrix
    sensor_data_matrix = np.concatenate(np.array(sensor_data).transpose())[30:]
    print(sensor_data_matrix[:30])
    sensor_data = []
  

def write_to_csv():
    dataframe = pandas.DataFrame(sensor_data, columns = header)
    dataframe.to_csv('user/gesture_' + str(filename_index) + '.csv', header = True)

def get_machine_learning_prediction():
    global sensor_data_matrix
    global decision_tree_regressor
    user_sensor_data_matrix = []
    user_sensor_data_matrix.append(sensor_data_matrix)
    sensor_data_matrix = []
    # print("user_sensor_data_matrix", user_sensor_data_matrix)
    prediction = decision_tree_regressor.predict(user_sensor_data_matrix)
    return prediction[0]

def get_gesture_prediction():
    matrix_transpose_and_flatten()
    prediction = get_machine_learning_prediction()
    return evaluated_prediction(prediction)

#hand position is decoded as 4 bit using the pinkie finger as the most significant bit
def get_finger_positions(fingers):
    hand = (1 if int(float(fingers[0])) <= 50 else 0) + (2 if int(float(fingers[1])) <= 50 else 0) + (4 if int(float(fingers[2])) <= 50 else 0) + (8 if int(float(fingers[3])) <= 50 else 0)
    return hand

def evaluated_prediction(prediction):
    gesture = 0
    print("prediction", prediction)
    if prediction >= 0.7 and prediction <= 1.3:
        gesture = 1
    elif prediction >= 1.7 and prediction <= 2.3:
        gesture = 2
    elif prediction >= 2.7 and prediction <= 3.3:
        gesture = 3
    elif prediction >= 3.7 and prediction <= 4.3:
        gesture = 4
    else:
        gesture = 0
    print("gesture", gesture)
    return gesture


def main(): 
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()

if __name__ == '__main__':
    print('main function')
    main()
