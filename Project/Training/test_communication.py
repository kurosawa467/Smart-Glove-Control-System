import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import os
import csv
import errno
import datetime
import pandas

MQTT_ADDRESS = '192.168.178.100'
MQTT_USER = 'mosquitto'
MQTT_PASSWORD = 'mosquitto'
GLOVE_TOPIC = '/esp32/glove'
dim = 50
direction = 1
encoding = 'utf-8'
gesture = 'gesture'
header = ["timestamp", "flex_1", "flex_2", "flex_3", "flex_4", "IMU_status", "yaw", "pitch", "row"]
start_time = 0
sensor_data = []
filename_prefix = 'gesture_'
filename_index = 0
message_index = 0

def on_connect(client, userdata, flags, rc):
  print('Connected with ESP32, result: ' + str(rc))
  client.subscribe(GLOVE_TOPIC)
  print(start_time)

def on_message(client, userdata, msg):
  global start_time
  global message_index
  global filename_index
  print('Message topic: ' + msg.topic + ', message payload: ' + str(msg.payload))
  raw_message = str(msg.payload)
  message = raw_message[raw_message.index('=>') + 2:].rstrip("'")
  tokens = message.split(',')

  # Here decides when to start recording gesture
  if True:
    if message_index == 0:
      print('Start to recognize gesture')
    if message_index < 24:
      write_to_matrix(tokens)
      message_index += 1
    if message_index == 24:
      get_gesture_prediction(filename_index)
      message_index = 0
      filename_index += 1

def write_to_matrix(tokens):
  current_time = (datetime.datetime.now() - start_time).total_seconds() * 1000
  row = [current_time]
  row += tokens
  sensor_data.append(row)

def write_to_csv():
  dataframe = pandas.DataFrame(sensor_data, columns = header)
  dataframe.to_csv('user/gesture_' + filename_index + '.csv', header = True)
  gesture = get_machine_learning_prediction()
  

def get_machine_learning_prediction(filename):
  gesture = ''

def get_gesture_prediction(tokens):
  write_to_csv(tokens)
  gesture = get_machine_learning_prediction('user/gesture_' + filename_index + '.csv')
  command = ''

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
