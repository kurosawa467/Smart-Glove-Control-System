import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import os
import csv
import errno
import datetime
import pandas
from training import SVMModel

MQTT_ADDRESS = '192.168.178.100'
MQTT_USER = 'mosquitto'
MQTT_PASSWORD = 'mosquitto'
GLOVE_TOPIC = '/esp32/glove'
dim = 50
direction = 1
encoding = 'utf-8'
gesture = 'gesture'
header = ["timestamp", "yaw", "pitch", "row"]
start_time = 0
sensor_data = []
filename_prefix = 'gesture_'
filename_index = 0
message_index = 0
svmModel = None
gesture_mode = False

def on_connect(client, userdata, flags, rc):
  global svmModel
  global start_time
  print('Connected with ESP32, result: ' + str(rc))
  client.subscribe(GLOVE_TOPIC)
  if start_time == 0:
    start_time = datetime.datetime.now()
  print(start_time)
  svmModel = SVMModel()
  accuracy = svmModel.training()
  print('SVM model is ready, initial accuracy is ' + str(accuracy))


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
  if not gesture_mode:
      if hand==15:
          gesture_mode = True

  if gesture_mode:
    if message_index == 0:
      print('Start to recognize gesture')
      sensor_data = []
    if message_index < 30:
      write_to_matrix(tokens[5:8])
      message_index += 1
    if message_index == 30:
      gesture = get_gesture_prediction()
      print(gesture)
      command = ''
      if hand == 1:
          if gesture == 1:
              command = 'next device'
          elif gesture == 0:
              command = 'previous device'
      elif hand == 3:
          if gesture == 1:
              command = 'next color'
          elif gesture == 0:
              command = 'previous color'
      print('Recognized command is: ' + command)
      message_index = 0
      filename_index += 1
      gesture_mode = False

def write_to_matrix(tokens):
  global sensor_data
  current_time = (datetime.datetime.now() - start_time).total_seconds() * 1000
  row = [current_time]
  row += tokens
  sensor_data.append(row)

def write_to_csv():
  dataframe = pandas.DataFrame(sensor_data, columns = header)
  dataframe.to_csv('user/gesture_' + str(filename_index) + '.csv', header = True)

def get_machine_learning_prediction():
  return svmModel.get_gesture_prediction('user/gesture_' + str(filename_index) + '.csv')

def get_gesture_prediction():
  write_to_csv()
  return get_machine_learning_prediction()

#hand position is decoded as 4 bit using the pinkie finger as the most significant bit
def get_finger_positions(fingers):
  hand = (1 if int(float(fingers[0])) <= 40 else 0) + (2 if int(float(fingers[1])) <= 40 else 0) + (4 if int(float(fingers[2])) <= 40 else 0) + (8 if int(float(fingers[3])) <= 40 else 0)
  return hand


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
