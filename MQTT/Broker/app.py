from enum import Enum
import serial
from serial import Serial, SerialException
import logging
import queue
import time

class SensorMessageQueue:
    queue = queue.Queue()
    
    def __init__(self):
        time.sleep(0.0001)

    def pushNewMessage(self, message):
        SensorMessageQueue.queue.put(message)
        print('Queue size is ' + str(SensorMessageQueue.queue.qsize()))
        print('Message has been pushed into queue')
        smartGloveControlSystem = SmartGloveControlSystem()
        smartGloveControlSystem.handle_queue()

class SmartGloveControlSystem:
    # IoT device command, placeholders for now
    class IoTTopic(Enum):
        LED_1_ANALOG_TOPIC = '/esp8266/1.1'
        LED_1_DIGITAL_TOPIC = '/esp8266/1.2'
        LED_2_ANALOG_TOPIC = '/esp8266/2.1'
        LED_2_DIGITAL_TOPIC = '/esp8266/2.2'

    def __init__(self):
        # raw_data_buffer stores raw data directly parsed from sensor data
        self.raw_data_buffer = []
        self.gesture_buffer = []
        self.logger = logging.getLogger('Home')

    def start_looping(self):
        self.handle_queue()
   
    def handle_message(self, raw_message, client):
        # This is a placeholder format of the message
        # =>[float flex_1],[float flex_2],[float flex_3],[float flex_4],[float IMU_Quat],[float IMU_x],[float IMU_y],[float IMU_z]
        if raw_message.count('=') != 1 or raw_message.count('>') != 1:
            self.logger.debug('Message is corrupted, sensor stats indicator missing')
            return

        # Strip message overhead before the => indicator (if any)
        message = raw_message[raw_message.index('=>') + 2:].rstrip()

        # Might need to process ack, if we have one

        # Check if correct amount of sensor stats are included in the message
        if message.count(',') != 7:
            self.logger.debug('Message is corrupted, not correct amount of stats included')
            return

        tokens = message.split(',')
        print(tokens)
        roll = float(tokens[7])
        pitch = float(tokens[6])
        ledDim = int(100 * (roll + 180) / 360)
        color = int(16 * (pitch + 180) / 360) % 8
        outgoing_message = str(color) + str(ledDim)
        # topic to be modified
        topic_1_1 = int(tokens[0])
        topic_1_2 = int(tokens[1])
        topic_2_1 = int(tokens[2])
        topic_2_2 = int(tokens[3])
        if topic_1_1:
            client.publish(self.IoTTopic.LED_1_ANALOG_TOPIC, outgoing_message)
        if topic_1_2:
            client.publish(self.IoTTopic.LED_1_DIGITAL_TOPIC, outgoing_message)
        if topic_2_1:
            client.publish(self.IoTTopic.LED_2_ANALOG_TOPIC, outgoing_message)
        if topic_2_2:
            client.publish(self.IoTTopic.LED_2_DIGITAL_TOPIC, outgoing_message)
        
    def handle_queue(self, client):
        queue = SensorMessageQueue.queue
        print('Checking message queue')
        
        if queue.qsize():
            self.logger.info('Message queued, start processing')
            print('Message found, started procesing')
        else:
            self.logger.info('Message queue is empty')
            print('Message queue is empty')
            return

        while not queue.empty():
            message = queue.get()
            self.handle_message(message, client)
