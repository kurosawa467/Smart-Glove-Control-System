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
from sklearn.tree import export_graphviz
import pydot
import os

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

        # hardcoded target for gesture labeling. left swiping is 1, right swiping is 2
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
        SVMModel.classifier_linear.fit(X_train, y_train)
        y_prediction = SVMModel.classifier_linear.predict(X_test)
        print("SVM linear kernel accuracy is ", metrics.accuracy_score(y_test, y_prediction))
        
        # SVM poly
        SVMModel.classifier_poly.fit(X_train, y_train)
        y_prediction = SVMModel.classifier_poly.predict(X_test)
        print("SVM poly kernel accuracy is ", metrics.accuracy_score(y_test, y_prediction))
        
        # SVM rbf
        SVMModel.classifier_rbf.fit(X_train, y_train)
        y_prediction = SVMModel.classifier_rbf.predict(X_test)
        print("SVM rbf kernel accuracy is ", metrics.accuracy_score(y_test, y_prediction))
        
        # SVM sigmoid
        SVMModel.classifier_sigmoid.fit(X_train, y_train)
        y_prediction = SVMModel.classifier_sigmoid.predict(X_test)
        print("SVM sigmoid kernel accuracy is ", metrics.accuracy_score(y_test, y_prediction))
        
        # Random Forest
        train_features, test_features, train_labels, test_labels = train_test_split(SVMModel.sensor_data_matrix, target, 
                                                                                    test_size = 0.3, random_state = 42)
        
        # Normal tree
        rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
        rf.fit(train_features, train_labels)
        predictions = rf.predict(test_features)
        errors = abs(predictions - test_labels)
        print('Random forest mean absolute error is: ', round(np.mean(errors), 2))
        mape = 100 * (errors / test_labels)
        accuracy = 100 - np.mean(mape)
        print('Random forest accuracy is :', round(accuracy, 2), '%')

        # Small tree
        rf_small = RandomForestRegressor(n_estimators = 10, max_depth = 3, random_state = 42)
        rf_small.fit(train_features, train_labels)
        predictions = rf_small.predict(test_features)
        errors = abs(predictions - test_labels)
        print('Random forest small tree mean absolute error is: ', round(np.mean(errors), 2))
        mape = 100 * (errors / test_labels)
        accuracy = 100 - np.mean(mape)
        print('Random forest small tree accuracy is :', round(accuracy, 2), '%')

        # filename = 'svm_model.sav'
        # pickle.dump(SVMModel.classifier, open(filename, 'wb'))
        
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
