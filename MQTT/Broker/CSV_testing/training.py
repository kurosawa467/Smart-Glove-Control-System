import glob
import pandas
import numpy as np
from pandas.io.clipboards import read_clipboard
from pandas.io.parsers import read_csv
from itertools import chain
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split


sensor_data_matrix = []


def read_data_from_csv(gesture):
    for file in sorted(glob.glob("MQTT/Broker/CSV_testing/" + gesture + "/*.csv")):
        gesture_sensor_data = pandas.read_csv(file, header = 0, index_col = "timestamp")
        gesture_sensor_data = gesture_sensor_data.apply(pandas.to_numeric, errors = 'coerce')
        gesture_sensor_data = gesture_sensor_data[0:23]
        print(gesture_sensor_data['flex_1'].to_numpy())
        flattened_gesture_sensor_data = gesture_sensor_data['flex_1'].to_numpy().flatten()
        # print(len(flattened_gesture_sensor_data))
        sensor_data_matrix.append(flattened_gesture_sensor_data)


# testing period, only "gesture" and "noise"

# read sensor data from two directories
read_data_from_csv("gesture")
read_data_from_csv("noise")

# print(read_data_from_csv("gesture"))
# print(glob.glob("MQTT/*/"))

# hardcoded target for gesture labeling. "gesture" is 1, "noise" is 0
target = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
# print(len(target))

# X_train, X_test, y_train, y_test = train_test_split(sensor_data_matrix, target, test_size=0.3, random_state=46)
X_train, X_test, y_train, y_test = train_test_split(sensor_data_matrix, target, test_size=0.3, random_state=46)
classifier = svm.SVC(kernel='linear')
classifier.fit(X_train, y_train)
y_prediction = classifier.predict(X_test)

print("Accuracy is ", metrics.accuracy_score(y_test, y_prediction))
