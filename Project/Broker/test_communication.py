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
index = 0
filename = ''
gesture = 'gesture'
header = ["timestamp", "flex_1", "flex_2", "flex_3", "flex_4", "IMU_status", "yaw", "pitch", "row"]
start_time = 0
sensor_data = []

def on_connect(client, userdata, flags, rc):
  global filename
  print('Connected with ESP32, result: ' + str(rc))
  client.subscribe(GLOVE_TOPIC)
  filename = input("Filename: ")
  print(start_time)

def on_message(client, userdata, msg):
  global filename
  global index
  global start_time
  print('Message topic: ' + msg.topic + ', message payload: ' + str(msg.payload))
  raw_message = str(msg.payload)
  message = raw_message[raw_message.index('=>') + 2:].rstrip("'")
  tokens = message.split(',')
  if start_time == 0:
    start_time = datetime.datetime.now()
  current_time = (datetime.datetime.now() - start_time).total_seconds() * 1000
  print(current_time)
  row = [current_time]
  row += tokens
  sensor_data.append(row)
  if current_time > 2000:
    dataframe = pandas.DataFrame(sensor_data, columns = header)
    dataframe.to_csv(gesture + '/' + filename, header = True)

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
