import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import threading

MQTT_ADDRESS = '192.168.178.100'
MQTT_USER = 'mosquitto'
MQTT_PASSWORD = 'mosquitto'
MQTT_TOPIC_BUTTON_SUB = '/esp32/button'
MQTT_TOPIC_FLEX_SUB = '/esp32/flex'
MQTT_TOPIC_BUTTON_PUB = '/esp8266/button'
MQTT_TOPIC_FLEX_PUB = '/esp8266/flex'

def on_connect(client, userdata, flags, rc):
  print('Connected with ESP32, result: ' + str(rc))
  client.subscribe(MQTT_TOPIC_BUTTON_SUB)
  client.subscribe(MQTT_TOPIC_FLEX_SUB)

def on_message(client, userdata, msg):
  print('Message topic: ' + msg.topic + ', message payload: ' + str(msg.payload))
#   client.publish('button', '1 Button is pushed')
 
  if msg.topic == MQTT_TOPIC_BUTTON_SUB:
      if client.publish(MQTT_TOPIC_BUTTON_PUB, '1: Button pushed - From Broker'):
          print('Published button message to esp8266')
      else:
          print('Button message failed to be published to esp8266')
  elif msg.topic == MQTT_TOPIC_FLEX_SUB:
      if client.publish(MQTT_TOPIC_FLEX_PUB, '0: Flex sensor is bent - From Broker'):
          print('Published flex sensor message to esp8266')
      else:
          print('Flex sensor message failed to be published to esp8266')
  else:
      print('Message cannot be recognized.')
   

def main():
  #mqtt_client = mqtt.Client('ESP32')
  mqtt_client = mqtt.Client()
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
  mqtt_client.on_connect = on_connect
  mqtt_client.on_message = on_message

  mqtt_client.connect(MQTT_ADDRESS, 1883)
  mqtt_client.loop_forever()

if __name__ == '__main__':
  print('main function')
  main()