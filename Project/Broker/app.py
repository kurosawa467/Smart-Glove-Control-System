from enum import Enum
import serial
from serial import Serial, SerialException
import logging
import queue
import time
import csv

class SensorMessageQueue:
    queue = queue.Queue()
    
    def __init__(self):
        time.sleep(0.0001)

    def pushNewMessage(self, message, client):
        SensorMessageQueue.queue.put(message)
        #print('Queue size is ' + str(SensorMessageQueue.queue.qsize()))
        print('Message has been pushed into queue')
        smartGloveControlSystem = SmartGloveControlSystem()
        smartGloveControlSystem.handle_queue(client)

class SmartGloveControlSystem:
    selected_device = 0
    # IoT device command, placeholders for now
    subscribing_topics = ['/esp8266/1.1','/esp8266/1.2','/esp8266/2.1', '/esp8266/2.2', 'JS_APP']

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
            print('Message is corrupted, sensor stats indicator missing')
            return

        # Strip message overhead before the => indicator (if any)
        message = raw_message[raw_message.index('=>') + 2:].rstrip("'")

        # Might need to process ack, if we have one

        # Check if correct amount of sensor stats are included in the message
        if message.count(',') != 7:
            print('Message is corrupted, not correct amount of stats included')
            return

        tokens = message.split(',')
        print(tokens)
        imuStatus = int(tokens[4])
        yaw = float(tokens[5])
        pitch = float(tokens[6])
        roll = float(tokens[7])

        #ledDim = int(100 * (roll + 180) / 360)
        ledDim = int(-200 * (roll - 180) / 360)
        if ledDim > 100:
            if ledDim >150:
                ledDim = 0
            else:
                ledDim = 100
        #color = int(16 * (pitch + 180) / 360) % 8
                
        color = int((pitch * 4)/70) +4
        if color <0: color = 0
        if color >8: color = 8
        outgoing_message = str(color) + ' ' + str(ledDim)
        print(outgoing_message)
        # topic to be modified
        flex_1_1 = int(float(tokens[0]))
        flex_1_2 = int(float(tokens[1]))
        flex_2_1 = int(float(tokens[2]))
        flex_2_2 = int(float(tokens[3]))
        if flex_1_1:
            client.publish('/esp8266/1.1', outgoing_message)
        if flex_1_2:
            client.publish('/esp8266/1.2', outgoing_message)
        if flex_2_1:
            client.publish('/esp8266/2.1', outgoing_message)
        if flex_2_2:
            client.publish('/esp8266/2.2', outgoing_message)
        client.publish('JS_APP', outgoing_message)
        
        timestamp = time.monotonic()#time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
        print(timestamp)
        f = open("data.txt", "a")
        f.write("{0},{1},{2},{3},{4}\n".format(timestamp,imuStatus,yaw,pitch,roll))
        f.close()
        
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
