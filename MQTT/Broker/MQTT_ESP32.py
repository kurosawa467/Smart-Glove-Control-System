import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import threading

from time import sleep

MQTT_ADDRESS = '192.168.178.100'
MQTT_USER = 'mosquitto'
MQTT_PASSWORD = 'mosquitto'
MQTT_TOPIC_BUTTON = 'button'
MQTT_TOPIC_MOTION = 'motion'

def on_connect(client, userdata, flags, rc):
  print('Connected with ESP32, result: ' + str(rc))

def on_message(client, userdata, msg):
  print('Message topic: ' + msg.topic + ', message payload: ' + str(msg.payload))
  client.publish('button', '1 Button is pushed')
  
#  if msg.topic == 'button':
#      client.publish('button', '1 Button is pushed')
#  elif msg.topic == 'motion':
#      client.publish('motion', '0 Motion is detected')
#  else:
#      print('Message cannot be recognized.')
    

def main():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(8, GPIO.OUT, initial = GPIO.LOW)
  mqtt_client = mqtt.Client('ESP32')
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
  mqtt_client.on_connect = on_connect
  mqtt_client.on_message = on_message

  mqtt_client.connect(MQTT_ADDRESS, 1883)
  mqtt_client.loop_forever()

if __name__ == '__main__':
  print('main function')
  main()
