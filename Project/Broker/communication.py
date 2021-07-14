import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from app import SensorMessageQueue, SmartGloveControlSystem

MQTT_ADDRESS = '192.168.178.27'
MQTT_USER = 'mosquitto'
MQTT_PASSWORD = 'mosquitto'
GLOVE_TOPIC = '/esp32/glove'
dim = 50
direction = 1
encoding = 'utf-8'
control_system = ''

def on_connect(client, userdata, flags, rc):
  print('Connected with ESP32, result: ' + str(rc))
  client.subscribe(GLOVE_TOPIC)
  control_system = SmartGloveControlSystem()

def on_message(client, userdata, msg):
  print('Message topic: ' + msg.topic + ', message payload: ' + str(msg.payload))
  SensorMessageQueue().pushNewMessage(str(msg.payload), client)
  control_system.handle_queue(client)

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
