from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
import os
from Logger import AppLogger

class ModelFinder:
    '''
    This class shall be used to find the model with best accuracy and AUC Score.
    '''

    def __init__(self):
        self.current_directory = os.getcwd()
        self.file_object = open('Training_Logs/ModelFinder.txt', 'a+')
        self.logger = AppLogger()
        self.gnb = GaussianNB()
        self.xgb = XGBClassifier(objective='binary:logistic', n_jobs=-1)

    def get_best_params_xgboost(self, train_x, train_y):
        '''
        Description: get the parameters for XGBoost Algorithm which give the best accuracy.
                                                     Use Hyper Parameter Tuning.
        :param train_x: Feature Dataset
        :param train_y: Label Dataset
        :return: The model with best parameters
        :failure: Raise Exception
        '''
        try:
            self.file_object = open('Training_Logs/ModelFinder.txt', 'a+')
            self.logger.log(self.file_object,'Entered the get_best_params_for_xgboost method of the Model_Finder class')

            # initializing with different combination of parameters
            self.param_grid_xgboost = {
                "n_estimators": [50, 100, 130],
                "max_depth": range(3, 11, 1),
                "random_state": [0, 50, 100]

            }

            # Creating an object of the Grid Search class
            self.grid = GridSearchCV(XGBClassifier(objective='binary:logistic'), self.param_grid_xgboost, verbose=3,
                                     cv=2, n_jobs=-1)

            # Finding the best parameters
            self.grid.fit(train_x, train_y)

            # extracting the best parameters
            self.random_state = self.grid.best_params_['random_state']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']

            # creating a new model with the best parameters
            self.xgb = XGBClassifier(random_state=self.random_state, max_depth=self.max_depth,n_estimators= self.n_estimators, n_jobs=-1 )
            # training the mew model
            self.xgb.fit(train_x, train_y)
            self.logger.log(self.file_object,
                                   'XGBoost best params: ' + str(
                                       self.grid.best_params_) + '. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            return self.xgb

        except Exception as e:
            self.file_object = open('Training_Logs/ModelFinder.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred {}'.format(str(e)))
            raise e
        finally:
            self.file_object.close()

    def get_best_params_naive_bayes(self, train_x, train_y):
        '''
        Description: get the parameters for the Naive Bayes's Algorithm which give the best accuracy.
                     Use Hyper Parameter Tuning.
        :param train_x: Feature Dataset
        :param train_y: Label Dataset
        :return: The model with best parameters
        :failure: Raise Exception
        '''
        try:
            self.file_object = open('Training_Logs/ModelFinder.txt', 'a+')
            self.logger.log(self.file_object,'Entered the get_best_params_for_naive_bayes method of the Model_Finder class')

            # initializing with different combination of parameters
            self.param_grid = {"var_smoothing": [1e-9, 0.1, 0.001, 0.5, 0.05, 0.01, 1e-8, 1e-7, 1e-6, 1e-10, 1e-11]}

            # Creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.gnb, param_grid=self.param_grid, cv=3, verbose=3)

            # finding the best parameters
            self.grid.fit(train_x, train_y)

            # extracting the best parameters
            self.var_smoothing = self.grid.best_params_['var_smoothing']

            # creating a new model with the best parameters
            self.gnb = GaussianNB(var_smoothing=self.var_smoothing)
            # training the mew model
            self.gnb.fit(train_x, train_y)
            self.logger.log(self.file_object,'Naive Bayes best params: ' + str(self.grid.best_params_) +
                            '. Exited the get_best_params_for_naive_bayes method of the Model_Finder class')

            return self.gnb


        except Exception as e:
            self.file_object = open('Training_Logs/ModelFinder.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred {}'.format(str(e)))
            raise e
        finally:
            self.file_object.close()

    def get_best_model(self, train_x, train_y, test_x, test_y):
        '''
        Description: Finds out the model which has the best AUC score.
        :param train_x: Feature Training Dataset
        :param train_y: Label Training Dataset
        :param test_x: Feature Testing Dataset
        :param test_y: Label Testing Dataset
        :return: The best model name and the object of it
        :failure: Raise Exception
        '''

        try:
            self.file_object = open('Training_Logs/ModelFinder.txt', 'a+')
            self.logger.log(self.file_object,'Entered the get_best_model method of the Model_Finder class')

            # Create the best model for XGBoost
            xgboost = self.get_best_params_xgboost(train_x, train_y)
            prediction_xgboost = xgboost.predict(test_x) # Predictions on the test data

            # Calculating the roc_auc score
            xgboost_score = roc_auc_score(test_y, prediction_xgboost)
            self.file_object = open('Training_Logs/ModelFinder.txt', 'a+')
            self.logger.log(self.file_object, 'AUC for XGBoost: ' + str(xgboost_score))

            # Create the best model for Naive Bayes
            naive_bayes = self.get_best_params_naive_bayes(train_x, train_y)
            prediction_naive_bayes = naive_bayes.predict(test_x)

            # Calculating the roc_auc score
            naive_bayes_score = roc_auc_score(test_y, prediction_naive_bayes)
            self.file_object = open('Training_Logs/ModelFinder.txt', 'a+')
            self.logger.log(self.file_object, 'AUC for RF:' + str(naive_bayes_score))

            # Comparing the two models with their score
            if (naive_bayes_score < xgboost_score):
                return 'XGBoost', xgboost
            else:
                return 'NaiveBayes', naive_bayes

        except Exception as e:
            self.file_object = open('Training_Logs/ModelFinder.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred {}'.format(str(e)))
            raise e
        finally:
            self.file_object.close()