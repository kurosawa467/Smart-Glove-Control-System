import matplotlib.pyplot as plt
import pandas
import numpy as np
import glob

header = ["yaw_0", "yaw_1", "yaw_2", "yaw_3", "yaw_4", "yaw_5", "yaw_6", "yaw_7", "yaw_8", "yaw_9",
          "yaw_10", "yaw_11", "yaw_12", "yaw_13", "yaw_14", "yaw_15", "yaw_16", "yaw_17", "yaw_18", "yaw_19",
          "yaw_20", "yaw_21", "yaw_22", "yaw_23", "yaw_24", "yaw_25", "yaw_26", "yaw_27", "yaw_28", "yaw_29",
          "pitch_0", "pitch_1", "pitch_2", "pitch_3", "pitch_4", "pitch_5", "pitch_6", "pitch_7", "pitch_8", "pitch_9",
          "pitch_10", "pitch_11", "pitch_12", "pitch_13", "pitch_14", "pitch_15", "pitch_16", "pitch_17", "pitch_18", "pitch_19",
          "pitch_20", "pitch_21", "pitch_22", "pitch_23", "pitch_24", "pitch_25", "pitch_26", "pitch_27", "pitch_28", "pitch_29",
          "row_0", "row_1", "row_2", "row_3", "row_4", "row_5", "row_6", "row_7", "row_8", "row_9",
          "row_10", "row_11", "row_12", "row_13", "row_14", "row_15", "row_16", "row_17", "row_18", "row_19",
          "row_20", "row_21", "row_22", "row_23", "row_24", "row_25", "row_26", "row_27", "row_28", "row_29", "gesture"]
target = np.array(["left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left",
                   "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left",
                   "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left",
                   "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left",
                   "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left",
                   "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left",
                   "left", "left", "left", "left", "left", "left", "left", "left", "left", "left",
                   "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right",
                   "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right",
                   "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right",
                   "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right",
                   "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right",
                   "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right",
                   "right", "right", "right", "right", "right", "right", "right", "right", "right", "right",
                   "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock",
                   "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock",
                   "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock",
                   "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock",
                   "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock",
                   "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock",
                   "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock", "clock",
                   "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull",
                   "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull",
                   "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull",
                   "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull",
                   "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull",
                   "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull",
                   "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull", "pull"])

sensor_data_matrix = np.zeros([520, 90])

def read_data_from_csv(gesture, index_offset):
    index = 0 + 130 * index_offset
    for file in glob.glob("./" + gesture + "/*.csv"):
        sensor_data = pandas.read_csv(file, header = 0)
        row = np.concatenate((np.array(sensor_data['yaw']).T,
                              np.array(sensor_data['pitch']).T,
                              np.array(sensor_data['row']).T), axis = 0)
        sensor_data_matrix[index, :] = row
        index += 1

read_data_from_csv("left", 0)
read_data_from_csv("right", 1)
read_data_from_csv("clock", 2)
read_data_from_csv("pull", 3)

target_array = target.reshape(520, 1)
sensor_data = np.append(sensor_data_matrix, target_array, axis = 1)


dataframe = pandas.DataFrame(sensor_data, columns = header)
dataframe.to_csv('all_data.csv', header = True)