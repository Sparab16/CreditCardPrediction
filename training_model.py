from sklearn.model_selection import train_test_split
from Logger import AppLogger
import numpy as np
import pandas as pd
import os
from Preprocessing.preprocessing import Preprocessor
from Preprocessing.clustering import KMeansClustering
from ModelFinder.model_finder import ModelFinder
from FileModel.file_operation import FileOperation

class TrainModel:

    def __init__(self):
        self.training_file = 'Training_FileFromDB/InputFile.csv'
        self.current_directory = os.getcwd()
        self.file_object = open("Training_Logs/TrainingModel.txt", 'a+')
        self.logger = AppLogger()

    def trainingModel(self):
        '''
        Description: This method is used for training the model
        :return: None
        :failure: Raise Exception
        '''
        try:
            self.file_object = open("Training_Logs/TrainingModel.txt", 'a+')
            self.logger.log(self.file_object, 'Storing the data from csv file to pandas dataframe')

            # 1. Storing the CSV file in pandas dataframe
            dataset = pd.read_csv(self.training_file)
            self.logger.log(self.file_object, 'Data load succesfully inside the dataframe')

            # 2. Data preprocessing
            preprocessor = Preprocessor()

            # 3. Create separate features and labels
            X, Y = preprocessor.separate_label_feature(dataset, 'default payment next month')

            # # 4. Checking for the missing values
            # is_null_present, cols_with_missing_values = preprocessor.is_null_present(X)

            # 5. Applying the clustering approach to divide the dataset into predefined clusters
            kmeans = KMeansClustering()

            # 6. Find out the optimum number of clusters using the elbow method
            no_clusters = kmeans.elbow_plot(X)

            # 7. Divide the data into the clusters
            X = kmeans.create_clusters(X, no_clusters)

            # 8. Create a new column in the dataset consisting of the corresponding cluster assignments.
            X['Labels'] = Y

            # 9. Getting the unique clusters
            list_clusters = X['Cluster'].unique()

            # 10. Finding the best ML algorithm for the individual cluster
            for i in list_clusters:
                # Filter the data for the one cluster
                cluster_data = X[X['Cluster'] == i]

                cluster_features = cluster_data.drop(['Labels','Cluster'], axis=1)
                cluster_label = cluster_data['Labels']

                # Splitting the data into training and test set for each cluster one by one
                X_train, X_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1/3,random_state=355)

                # Use the scaling technique to scale the data in some definite boundries
                train_x = preprocessor.scale_numerical_columns(X_train)
                test_x = preprocessor.scale_numerical_columns(X_test)

                # Find the best ML model for that cluster
                model_finder = ModelFinder()

                # Getting the best model for each of the clusters
                best_model_name, best_model = model_finder.get_best_model(train_x, y_train, test_x, y_test)

                # Saving the model to the directory
                file_operations = FileOperation()
                file_operations.save_model(best_model, best_model_name + str(i))

            # logging the successful Training
            self.logger.log(self.file_object, 'Successful End of Training')

        except Exception as e:
            self.file_object = open("Training_Logs/TrainingModel.txt", 'a+')
            self.logger.log(self.file_object, 'Error Occurred {}'.format(str(e)))
            raise 'training_model.py.trainingModel: ' + str(e)

        finally:
            self.file_object.close()