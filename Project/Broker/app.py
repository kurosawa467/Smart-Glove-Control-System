from enum import Enum
import serial
from serial import Serial, SerialException
import logging
import queue
import time
import datetime
import numpy as np
import pickle


class SensorMessageQueue:
    queue = queue.Queue()

    def __init__(self):
        time.sleep(0.0001)

    def pushNewMessage(self, message, client):
        SensorMessageQueue.queue.put(message)
        # print('Queue size is ' + str(SensorMessageQueue.queue.qsize()))
        #print('Message has been pushed into queue')
        smartGloveControlSystem = SmartGloveControlSystem()
        smartGloveControlSystem.handle_queue(client)


def evaluate_finger(finger):
    return 1 if int(float(finger)) <= 50 else 0


# returns cleaned message #Todo raise error
def process_message(raw_message):
    # This is a placeholder format of the message
    # =>[float flex_1],[float flex_2],[float flex_3],[float flex_4],[float IMU_Quat],[float IMU_x],[float IMU_y],[float IMU_z]
    if raw_message.count('=') != 1 or raw_message.count('>') != 1:
        print('Message is corrupted, sensor stats indicator missing')
        return

    # Strip message overhead before the => indicator (if any)
    message = raw_message[raw_message.index('=>') + 2:].rstrip("'")

    # Check if correct amount of sensor stats are included in the message
    if message.count(',') != 7:
        print('Message is corrupted, not correct amount of stats included')
        return

    return message.split(',')


def get_finger_positions(fingers):
    hand = evaluate_finger(fingers[0]) + 2 * evaluate_finger(fingers[1]) + 4 * evaluate_finger(
        fingers[2]) + evaluate_finger(fingers[3])
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


class SmartGloveControlSystem:
    start_time = 0
    message_index = 0
    gesture_mode = 1
    sensor_data = []
    selected_device = 0
    offered_topics = ['/esp8266/1.1', '/esp8266/1.2', '/esp8266/2.1', '/esp8266/2.2', 'JS_APP']
    model = ''

    def __init__(self):
        # raw_data_buffer stores raw data directly parsed from sensor data
        self.raw_data_buffer = []
        self.gesture_buffer = []
        self.logger = logging.getLogger('Home')
        self.model = pickle.load(open('random_forest_small.sav', 'rb'))
        self.start_time = datetime.datetime.now()

    # TODO: is this used?
    def start_looping(self):
        self.handle_queue()

    def handle_message(self, raw_message, client):
        tokens = process_message(raw_message)

        command = self.get_command(tokens)
        if command == 'next device':
            self.selected_device = (self.selected_device + 1) % self.offered_topics.len
        elif command == 'previous device':
            self.selected_device = (self.selected_device - 1) % self.offered_topics.len
        elif command == 'next color':
            client.publish(self.offered_topics[self.selected_device], "1")
        elif command == 'previous color':
            client.publish(self.offered_topics[self.selected_device], "2")
        elif command == 'lower brightness':
            client.publish(self.offered_topics[self.selected_device], "3")
        elif command == 'higher brightness':
            client.publish(self.offered_topics[self.selected_device], "4")

    # TODO: is this used?
    def handle_queue(self, client):
        queue = SensorMessageQueue.queue
        #print('Checking message queue')

        if queue.qsize():
            pass
            #self.logger.info('Message queued, start processing')
            #print('Message found, started procesing')
        else:
            pass
            #self.logger.info('Message queue is empty')
            #print('Message queue is empty')
            return

        while not queue.empty():
            message = queue.get()
            self.handle_message(message, client)

    def get_command(self, tokens):
        hand = 0
        if self.gesture_mode == 1:
            hand = get_finger_positions(tokens[:4])
            if hand == 1 or hand == 3:
                self.gesture_mode = 2
        if self.gesture_mode == 3:
            hand = get_finger_positions(tokens[:4])
            if hand == 15:
                self.gesture_mode = 1

        if self.gesture_mode == 2:
            if self.message_index == 0:
                print('Start to recognize gesture')
                hand = get_finger_positions(tokens[:4])
                print("hand start ", hand)
                sensor_data = []
            if self.message_index < 30:
                print(self.message_index)
                self.write_to_matrix(tokens[5:8])
                self.message_index += 1
            if self.message_index == 30:
                print('check')
                start_time = datetime.datetime.now()
                gesture = self.get_gesture_prediction()
                end_time = datetime.datetime.now()
                rf_time = (end_time - start_time).total_seconds()
                print("time", rf_time)
                print("hand end", hand)
                command = ''
                if hand == 1:
                    if gesture == 1:
                        command = 'next device'
                    elif gesture == 2:
                        command = 'previous device'
                    else:
                        command = 'gesture unrecognized'
                elif hand == 3:
                    if gesture == 1:
                        command = 'next color'
                    elif gesture == 2:
                        command = 'previous color'
                    elif gesture == 3:
                        command = 'lower brightness'
                    elif gesture == 4:
                        command = 'higher brightness'
                    else:
                        command = 'gesture unrecognized'
                else:
                    command = 'gesture unrecognized'
                print('Recognized command is: ' + command)
                message_index = 0
                gesture_mode = 3

                return command

    def write_to_matrix(self, tokens):
        current_time = (datetime.datetime.now() - self.start_time).total_seconds() * 1000
        row = [current_time]
        row += tokens
        self.sensor_data.append(row)

    def get_gesture_prediction(self):
        self.matrix_transpose_and_flatten()
        prediction = self.get_machine_learning_prediction()
        return evaluated_prediction(prediction)

    def matrix_transpose_and_flatten(self):
        self.sensor_data_matrix = np.concatenate(np.array(self.sensor_data).transpose())[30:]
        print(self.sensor_data_matrix[:30])
        self.sensor_data = []

    def get_machine_learning_prediction(self):
        user_sensor_data_matrix = []
        user_sensor_data_matrix.append(self.sensor_data_matrix)
        # print("user_sensor_data_matrix", user_sensor_data_matrix)
        prediction = self.model.predict(user_sensor_data_matrix)
        return prediction[0]

    def dim_LED(self, roll):
        ledDim = int(-200 * (roll - 180) / 360)
        if ledDim > 100:
            if ledDim > 150:
                ledDim = 0
            else:
                ledDim = 100
        return ledDim

    def get_color(self, pitch):
        color = int((pitch * 4) / 70) + 4
        if color < 0: color = 0
        if color > 8: color = 8

        return color
