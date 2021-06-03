from enum import Enum
import serial
from serial import Serial, SerialException
import logging
from queue import Queue
import time

class SensorMessageQueue:
    def __init__(self):
        time.sleep(0.1)

    def pushNewMessage(self, message):
        self.queue.put(message)

class SmartGloveControlSystem:
    # IoT device command, placeholders for now
    class IoTCommand(Enum):
        turn_on_LED_1 = 0
        turn_on_LED_2 = 1
        turn_on_LED_3 = 2
        turn_off_LED_1 = 3
        turn_off_LED_2 = 4
        turn_off_LED_3 = 5

    def __init__(self):
        # raw_data_buffer stores raw data directly parsed from sensor data
        self.raw_data_buffer = []
        self.gesture_buffer = []
        self.logger = logging.getLogger('Home')

    def start_looping(self):
        self.handle_queue()
    
    def handle_message(self, raw_message):

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
        self.logger.debug(tokens)
    
    def handle_queue(self):
        queue = SensorMessageQueue.queue
        if queue.qsize():
            self.logger.info('Message queued, start processing')
        else:
            self.logger.info('Message queue is empty')
            return

        for message in queue:
            message = queue.get()
            self.logger.debug(message)
            self.handle_message(message)

def main():
    while True:
        time.sleep(1)
        SmartGloveControlSystem.handle_queue()

if __name__ == '__main__':
  print('main function started')
  main()
