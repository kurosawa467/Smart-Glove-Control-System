import glob
import pandas
import numpy as np
from pandas.io.clipboards import read_clipboard
from pandas.io.parsers import read_csv
from itertools import chain
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle
import datetime

class SVMModel:
    sensor_data_matrix = np.zeros([400, 90])
    classifier_linear = svm.SVC(kernel = 'linear')
    classifier_poly = svm.SVC(kernel = 'poly')
    classifier_rbf = svm.SVC(kernel = 'rbf')
    classifier_sigmoid = svm.SVC(kernel = 'sigmoid')

    def get_gesture_prediction(self, filename):
        sensor_data = pandas.read_csv(filename, header = 0)
        row = np.concatenate((np.array(sensor_data['yaw']).T,
                              np.array(sensor_data['pitch']).T,
                              np.array(sensor_data['row']).T), axis = 0)
        user_sensor_data_matrix = np.zeros([1, 90])
        user_sensor_data_matrix[0, :] = row
        prediction = SVMModel.classifier.predict(user_sensor_data_matrix)
        print(prediction[0])
        return prediction[0]

    def training(self):
        self.read_data_from_csv("left", 0)
        self.read_data_from_csv("right", 1)
        self.read_data_from_csv("clock", 1)
        self.read_data_from_csv("counter", 1)

        # hardcoded target for gesture labeling. left swiping is 1, right swiping is 2, clockwise circle is 3, counter-clockwise circle is 4
        target = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                           2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                           2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                           2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                           2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                           3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                           3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                           3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                           3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                           3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                           4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                           4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                           4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                           4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                           4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])

        X_train, X_test, y_train, y_test = train_test_split(SVMModel.sensor_data_matrix, target, test_size=0.3, random_state=42)
        # SVM linear
        SVM_linear_start_time = datetime.datetime.now()
        SVMModel.classifier_linear.fit(X_train, y_train)
        y_prediction = SVMModel.classifier_linear.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, y_prediction)
        SVM_linear_end_time = datetime.datetime.now()
        SVM_linear_time = (SVM_linear_end_time - SVM_linear_start_time).total_seconds()
        print("SVM linear kernel accuracy is:", round(accuracy * 100, 4), '%')
        print("SVM linear kernel takes ", round(SVM_linear_time, 4), "seconds")
        print()
        
        # SVM rbf
        SVM_non_linear_start_time = datetime.datetime.now()
        SVMModel.classifier_rbf.fit(X_train, y_train)
        y_prediction = SVMModel.classifier_rbf.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, y_prediction)
        SVM_non_linear_end_time = datetime.datetime.now()
        SVM_non_linear_time = (SVM_non_linear_end_time - SVM_non_linear_start_time).total_seconds()
        print("SVM non-linear (rbf) kernel accuracy is:", round(accuracy * 100, 4), '%')
        print("SVM non-linear kernel takes ", round(SVM_non_linear_time, 4), "seconds")
        print()
        
        # Random Forest
        train_features, test_features, train_labels, test_labels = train_test_split(SVMModel.sensor_data_matrix, target, 
                                                                                    test_size = 0.3, random_state = 42)
        
        # Normal tree
        random_forest_start_time = datetime.datetime.now()
        rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
        rf.fit(train_features, train_labels)
        predictions = rf.predict(test_features)
        errors = abs(predictions - test_labels)
        mape = 100 * (errors / test_labels)
        accuracy = 100 - np.mean(mape)
        random_forest_end_time = datetime.datetime.now()
        random_forest_time = (random_forest_end_time - random_forest_start_time).total_seconds()
        print('Random forest mean absolute error is:', round(np.mean(errors), 2))
        print('Random forest accuracy is:', round(accuracy, 4), '%')
        print("Random forest takes ", round(random_forest_time, 4), "seconds")
        print()

        # Small tree
        random_forest_small_start_time = datetime.datetime.now()
        rf_small = RandomForestRegressor(n_estimators = 50, max_depth = 3, random_state = 42)
        rf_small.fit(train_features, train_labels)
        predictions = rf_small.predict(test_features)
        errors = abs(predictions - test_labels)
        mape = 100 * (errors / test_labels)
        accuracy = 100 - np.mean(mape)
        random_forest_small_end_time = datetime.datetime.now()
        random_forest_small_time = (random_forest_small_end_time - random_forest_small_start_time).total_seconds()
        print('Random forest small tree mean absolute error is:', round(np.mean(errors), 2))
        print('Random forest small tree accuracy is:', round(accuracy, 4), '%')
        print("Random forest small tree takes ", round(random_forest_small_time, 4), "seconds")
        print()

        rf_filename = 'random_forest.sav'
        pickle.dump(rf, open(rf_filename, 'wb'))
        
        rf_small_filename = 'random_forest_small.sav'
        pickle.dump(rf_small, open(rf_small_filename, 'wb'))
        
        #loaded_model = pickle.load(open(filename, 'rb'))
        #y_prediction2 = loaded_model.predict(X_test)
        #print("Accuracy is ", metrics.accuracy_score(y_test, y_prediction2))
        return metrics.accuracy_score(y_test, y_prediction)

    def read_data_from_csv(self, gesture, index_offset):
        index = 0 + 100 * index_offset
        for file in glob.glob("/home/pi/smart-glove-control-system/Project/Training/" + gesture + "/*.csv"):
            sensor_data = pandas.read_csv(file, header = 0)
            row = np.concatenate((np.array(sensor_data['yaw']).T,
                                  np.array(sensor_data['pitch']).T,
                                  np.array(sensor_data['row']).T), axis = 0)
            SVMModel.sensor_data_matrix[index, :] = row
            index += 1
    
    
def main():
    print('main()')
    svmModel = SVMModel()
    accuracy = svmModel.training()
    
if __name__ == "__main__":
    main()
