import glob
import pandas
import numpy as np
from pandas.io.clipboards import read_clipboard
from pandas.io.parsers import read_csv
from itertools import chain
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.svm import SVR
import pickle
import datetime

class SVMModel:
    sensor_data_matrix = np.zeros([400, 90])
    classifier_linear = svm.SVC(kernel = 'linear')
    classifier_rbf = svm.SVC(kernel = 'rbf')

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
        self.read_data_from_csv("clock", 2)
        self.read_data_from_csv("counter", 3)

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
        
        # Classification
        # Logistic Regression

        LR_classifier = LogisticRegression(random_state = 42, max_iter=1000)
        LR_classifier.fit(X_train, y_train)
        LR_start_time = datetime.datetime.now()
        y_prediction = LR_classifier.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, y_prediction)
        LR_end_time = datetime.datetime.now()
        LR_time = (LR_end_time - LR_start_time).total_seconds()
        print("Classification algorithms")
        print("Logistic Regression accuracy is", round(accuracy * 100, 4), '%')
        print("Logistic Regression takes", round(LR_time, 4), "seconds")
        print()

        # Decision Tree Classifier

        DTC_classifier = DecisionTreeClassifier(random_state = 42)
        DTC_classifier.fit(X_train, y_train)
        DTC_start_time = datetime.datetime.now()
        y_prediction = DTC_classifier.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, y_prediction)
        DTC_end_time = datetime.datetime.now()
        DTC_time = (DTC_end_time - DTC_start_time).total_seconds()
        print("Decision Tree Classifier accuracy is", round(accuracy * 100, 4), '%')
        print("Decision Tree Classifier takes", round(DTC_time, 4), "seconds")
        print()
        
        dtc_filename = 'dtc.sav'
        pickle.dump(DTC_classifier, open(dtc_filename, 'wb'))
        
        # KNeighbors Classifier
        KNC_classifier = KNeighborsClassifier()
        KNC_classifier.fit(X_train, y_train)
        KNC_start_time = datetime.datetime.now()
        y_prediction = KNC_classifier.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, y_prediction)
        KNC_end_time = datetime.datetime.now()
        KNC_time = (KNC_end_time - KNC_start_time).total_seconds()
        print("KNeighbors Classifier accuracy is", round(accuracy * 100, 4), '%')
        print("KNeighbors Classifier takes", round(KNC_time, 4), "seconds")
        print()
        
        # Linear Discriminant Analysis
        LDA_classifier = LinearDiscriminantAnalysis()
        LDA_classifier.fit(X_train, y_train)
        LDA_start_time = datetime.datetime.now()
        y_prediction = LDA_classifier.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, y_prediction)
        LDA_end_time = datetime.datetime.now()
        LDA_time = (LDA_end_time - LDA_start_time).total_seconds()
        print("Linear Discriminant Analysis accuracy is", round(accuracy * 100, 4), '%')
        print("Linear Discriminant Analysis takes", round(LDA_time, 4), "seconds")
        print()
        
        # Gaussian NB

        GNB_classifier = GaussianNB()
        GNB_classifier.fit(X_train, y_train)
        GNB_start_time = datetime.datetime.now()
        y_prediction = GNB_classifier.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, y_prediction)
        GNB_end_time = datetime.datetime.now()
        GNB_time = (GNB_end_time - GNB_start_time).total_seconds()
        print("Gaussian NB accuracy is", round(accuracy * 100, 4), '%')
        print("Gaussian NB takes", round(GNB_time, 4), "seconds")
        print()
        
        # SVM linear

        SVMModel.classifier_linear.fit(X_train, y_train)
        SVM_linear_start_time = datetime.datetime.now()
        y_prediction = SVMModel.classifier_linear.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, y_prediction)
        SVM_linear_end_time = datetime.datetime.now()
        SVM_linear_time = (SVM_linear_end_time - SVM_linear_start_time).total_seconds()
        print("SVM linear kernel accuracy is", round(accuracy * 100, 4), '%')
        print("SVM linear kernel takes", round(SVM_linear_time, 4), "seconds")
        print()
        
        # SVM rbf

        SVMModel.classifier_rbf.fit(X_train, y_train)
        SVM_non_linear_start_time = datetime.datetime.now()
        y_prediction = SVMModel.classifier_rbf.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, y_prediction)
        SVM_non_linear_end_time = datetime.datetime.now()
        SVM_non_linear_time = (SVM_non_linear_end_time - SVM_non_linear_start_time).total_seconds()
        print("SVM non-linear (rbf) kernel accuracy is", round(accuracy * 100, 4), '%')
        print("SVM non-linear kernel takes", round(SVM_non_linear_time, 4), "seconds")
        print()
        
        # Regression
        print("Regression algorithms")
        train_features, test_features, train_labels, test_labels = train_test_split(SVMModel.sensor_data_matrix, target, 
                                                                                    test_size = 0.3, random_state = 42)
        # Linear Regression

        LR_regression = LinearRegression()
        LR_regression.fit(train_features, train_labels)
        LR_start_time = datetime.datetime.now()
        predictions = LR_regression.predict(test_features)
        errors = abs(predictions - test_labels)
        mape = 100 * (errors / test_labels)
        accuracy = 100 - np.mean(mape)
        LR_end_time = datetime.datetime.now()
        LR_time = (LR_end_time - LR_start_time).total_seconds()
        print("Linear Regression accuracy is", round(accuracy, 4), '%')
        print("Linear Regression takes", round(SVM_non_linear_time, 4), "seconds")
        print()
        
        # Polynomial Regression
        # PR_start_time = datetime.datetime.now()
        # poly = PolynomialFeatures(degree = 4)
        # PR_regression = LinearRegression()
        # train_features_poly = poly.fit_transform(train_features)
        # PR_regression.fit(train_features_poly, train_labels)
        # test_features_poly = poly.fit_transform(test_features)
        # predictions = PR_regression.predict(test_features_poly)
        # errors = abs(predictions - test_labels)
        # mape = 100 * (errors / test_labels)
        # accuracy = 100 - np.mean(mape)
        # PR_end_time = datetime.datetime.now()
        # PR_time = (PR_end_time - PR_start_time).total_seconds()
        # print("Polynomial Regression accuracy is", round(accuracy, 4), '%')
        # print("Polynomial Regression takes", round(PR_time, 4), "seconds")
        # print()
        
        # SVR Linear
        # SVR_Linear_start_time = datetime.datetime.now()
        # SVR_Linear_regression = SVR(kernel = 'linear', C = 100, gamma = 0.01, epsilon = .1)
        # features_scaler = StandardScaler()
        # labels_scaler = StandardScaler()
        # scaled_features = features_scaler.fit_transform(train_features)
        # scaled_labels = train_labels.ravel()
        # SVR_Linear_regression.fit(scaled_features, scaled_labels)
        # predictions = SVR_Linear_regression.predict(test_features)
        # predictions = labels_scaler.inverse_transform(predictions)
        # errors = abs(predictions - test_labels)
        # mape = 100 * (errors / test_labels)
        # accuracy = 100 - np.mean(mape)
        # SVR_Linear_end_time = datetime.datetime.now()
        # SVR_Linear_time = (SVR_Linear_end_time - SVR_Linear_start_time).total_seconds()
        # print("SVR Linear kernel accuracy is", round(accuracy, 4), '%')
        # print("SVR Linear kernel takes", round(SVR_Linear_time, 4), "seconds")
        # print()
        
        # SVR RBF
        # SVR_RBF_start_time = datetime.datetime.now()
        # SVR_RBF_regression = SVR(kernel = 'rbf')
        # SVR_RBF_regression.fit(train_features, train_labels)
        # predictions = SVR_RBF_regression.predict(test_features)
        # errors = abs(predictions - test_labels)
        # mape = 100 * (errors / test_labels)
        # accuracy = 100 - np.mean(mape)
        # SVR_RBF_end_time = datetime.datetime.now()
        # SVR_RBF_time = (SVR_RBF_end_time - SVR_RBF_start_time).total_seconds()
        # print("SVR rbf kernel accuracy is", round(accuracy, 4), '%')
        # print("SVR rbf kernel takes", round(SVR_Linear_time, 4), "seconds")
        # print()
        
        # Decision Tree Regressor

        DTR_regression = SVR(kernel = 'rbf')
        DTR_regression.fit(train_features, train_labels)
        DTR_start_time = datetime.datetime.now()
        predictions = DTR_regression.predict(test_features)
        errors = abs(predictions - test_labels)
        mape = 100 * (errors / test_labels)
        accuracy = 100 - np.mean(mape)
        DTR_end_time = datetime.datetime.now()
        DTR_time = (DTR_end_time - DTR_start_time).total_seconds()
        print("Decision Tree Regressor accuracy is", round(accuracy, 4), '%')
        print("Decision Tree Regressor takes", round(DTR_time, 4), "seconds")
        print()
        
        rf_filename = 'decision_tree_regressor.sav'
        pickle.dump(DTR_regression, open(rf_filename, 'wb'))
        
        # Random Forest     
        # Normal tree

        rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
        rf.fit(train_features, train_labels)
        random_forest_start_time = datetime.datetime.now()
        predictions = rf.predict(test_features)
        errors = abs(predictions - test_labels)
        mape = 100 * (errors / test_labels)
        accuracy = 100 - np.mean(mape)
        random_forest_end_time = datetime.datetime.now()
        random_forest_time = (random_forest_end_time - random_forest_start_time).total_seconds()
        # print('Random forest mean absolute error is', round(np.mean(errors), 2))
        print('Random forest accuracy is', round(accuracy, 4), '%')
        print("Random forest takes", round(random_forest_time, 4), "seconds")
        print()

        # Small tree

        rf_small = RandomForestRegressor(n_estimators = 50, max_depth = 3, random_state = 42)
        rf_small.fit(train_features, train_labels)
        random_forest_small_start_time = datetime.datetime.now()
        predictions = rf_small.predict(test_features)
        errors = abs(predictions - test_labels)
        mape = 100 * (errors / test_labels)
        accuracy = 100 - np.mean(mape)
        random_forest_small_end_time = datetime.datetime.now()
        random_forest_small_time = (random_forest_small_end_time - random_forest_small_start_time).total_seconds()
        # print('Random forest small tree mean absolute error is', round(np.mean(errors), 2))
        print('Random forest small tree accuracy is', round(accuracy, 4), '%')
        print("Random forest small tree takes", round(random_forest_small_time, 4), "seconds")
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
        for file in glob.glob("./" + gesture + "/*.csv"):
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
