import glob
import pandas
import numpy as np
from pandas.io.clipboards import read_clipboard
from pandas.io.parsers import read_csv
from itertools import chain
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split

class SVMModel:
    sensor_data_matrix = np.zeros([100, 90] )
    classifier = svm.SVC(kernel = 'linear')

    def get_gesture_prediction(self, filename):
        sensor_data = pandas.read_csv(filename, header = 0)
        row = np.concatenate((np.array(sensor_data['yaw']).T,
                              np.array(sensor_data['pitch']).T,
                              np.array(sensor_data['row']).T), axis = 0)
        user_sensor_data_matrix = np.zeros([1, 90])
        user_sensor_data_matrix[0, :] = row
        prediction = SVMModel.classifier.predict(user_sensor_data_matrix)
        return prediction[0]

    def training(self):
        self.read_data_from_csv("left", 0)
        self.read_data_from_csv("right", 1)

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

        X_train, X_test, y_train, y_test = train_test_split(SVMModel.sensor_data_matrix, target, test_size=0.3, random_state=57)
        SVMModel.classifier.fit(X_train, y_train)
        y_prediction = SVMModel.classifier.predict(X_test)

        print("Accuracy is ", metrics.accuracy_score(y_test, y_prediction))
        return metrics.accuracy_score(y_test, y_prediction)

    def read_data_from_csv(self, gesture, index_offset):
        index = 0 + 50 * index_offset
        for file in glob.glob("/home/pi/smart-glove-control-system/Project/Training/" + gesture + "/*.csv"):
            sensor_data = pandas.read_csv(file, header = 0)
            row = np.concatenate((np.array(sensor_data['yaw']).T,
                                  np.array(sensor_data['pitch']).T,
                                  np.array(sensor_data['row']).T), axis = 0)
            SVMModel.sensor_data_matrix[index, :] = row
            index += 1
    
def main():
    print('main()')
    SVMModel.training()
    
if __name__ == "__main__":
    main()
