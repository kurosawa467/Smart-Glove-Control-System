import glob
import pandas
import numpy as np
from pandas.io.clipboards import read_clipboard
from pandas.io.parsers import read_csv
from itertools import chain
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split

sensor_data_matrix = np.zeros([100, 184])

def read_data_from_csv(gesture, index_offset):
    index = 0 + 50 * index_offset
    for file in glob.glob("Project/Training/" + gesture + "/*.csv"):
        # sensor_data = pandas.read_csv(file, header = 0, index_col = "timestamp")
        sensor_data = pandas.read_csv(file, header = 0)
        sensor_data = sensor_data[0:23]
        # print(sensor_data)
        # print(np.array(sensor_data['flex_1']).T)
        row = np.concatenate((np.array(sensor_data['flex_1']).T,
                              np.array(sensor_data['flex_2']).T,
                              np.array(sensor_data['flex_3']).T,
                              np.array(sensor_data['flex_4']).T,
                              np.array(sensor_data['IMU_status']).T,
                              np.array(sensor_data['yaw']).T,
                              np.array(sensor_data['pitch']).T,
                              np.array(sensor_data['row']).T), axis = 0)
        sensor_data_matrix[index, :] = row
        index += 1
        # gesture_sensor_data = gesture_sensor_data.apply(pandas.to_numeric, errors = 'coerce')
        # gesture_sensor_data = gesture_sensor_data[0:23]
        # print(gesture_sensor_data['flex_1'].to_numpy())
        # flattened_gesture_sensor_data = gesture_sensor_data['flex_1'].to_numpy().flatten()
        # # print(len(flattened_gesture_sensor_data))
        # sensor_data_matrix.append(flattened_gesture_sensor_data)


# testing period, only "gesture" and "noise"

# read sensor data from two directories
read_data_from_csv("gesture", 0)
read_data_from_csv("noise", 1)

# print(read_data_from_csv("gesture"))
# print(glob.glob("MQTT/*/"))

# hardcoded target for gesture labeling. "gesture" is 1, "noise" is 0
target = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
# print(len(target))

# X_train, X_test, y_train, y_test = train_test_split(sensor_data_matrix, target, test_size=0.3, random_state=48)
X_train, X_test, y_train, y_test = train_test_split(sensor_data_matrix, target, test_size=0.3, random_state=57)
print(X_test)
print(len(X_test))
print(len(X_test[0]))
classifier = svm.SVC(kernel='linear')
classifier.fit(X_train, y_train)
y_prediction = classifier.predict(X_test)

print("Accuracy is ", metrics.accuracy_score(y_test, y_prediction))

class SVMModel:
    classifier = svm.SVC(kernel = 'linear')

    def get_gesture_prediction():
        print('')