import pandas as pd
import numpy as np
from FileModel.file_operation import FileOperation
from Preprocessing.preprocessing import Preprocessor
from Logger import AppLogger
from PredictionValidation.pred_raw_validation import PredictionDataValidation


class Predict:

    def __init__(self,path):
        self.prediction_file = 'Prediction_FileFromDB/InputFile.csv'
        self.file_object = open("Prediction_Logs/predict.txt", 'a+')
        self.logger = AppLogger()
        self.pred_data_val = PredictionDataValidation(path)

    def predictionFromModel(self):
        '''
        Description: This methods predicts the labels using the ML algorithm and save that to the output file
        :return: Final Prediction Output CSV
        :failure: Raise Exception
        '''
        try:
            self.file_object = open("Prediction_Logs/predict.txt", 'a+')

            # Deletes the existing prediction file from the last run
            self.pred_data_val.deletePredictionFile()

            self.logger.log(self.file_object,'Start of Prediction')

            # Storing the CSV file in pandas dataframe
            X = pd.read_csv(self.prediction_file)
            self.logger.log(self.file_object, 'Data load succesfully inside the dataframe')

            preprocessor = Preprocessor()

            # Check if missing values are present in the dataset
            # is_null_present, cols_with_missing_values = preprocessor.is_null_present(data)

            # # if missing values are there, replace them appropriately.
            # if (is_null_present):
            #     data = preprocessor.impute_missing_values(data, cols_with_missing_values)  # missing value imputation


            file_loader = FileOperation()
            kmeans = file_loader.load_model('KMeans')

            # Predicting the clusters for the Prediction data
            clusters = kmeans.predict(X)

            # Create a new column in the dataset consisting of the corresponding cluster assignments.
            X['clusters'] = clusters

            # Getting the unique clusters
            clusters=X['clusters'].unique()

            #  Finding the best ML algorithm for the individual cluster
            result = []
            for i in clusters:
                # Filter the data for the one cluster
                cluster_data= X[X['clusters']==i]

                cluster_data = cluster_data.drop(['clusters'],axis=1)

                # Scaling the X data
                scaled_cluster_data = preprocessor.scale_numerical_columns(cluster_data)

                # Finding the correct ML model with respect to its cluster number
                model_name = file_loader.find_correct_model_file(i)

                # Load that model in the memory
                model = file_loader.load_model(model_name)
                print(scaled_cluster_data, model)

                # Use the model above for the prediction
                prediction = model.predict(scaled_cluster_data)
                cluster_data['Predictions'] = prediction

                result.append(pd.DataFrame(cluster_data))


            final = result
            # final = pd.DataFrame(result)
            # final = pd.DataFrame(list(zip(result)),columns=['Predictions'])
            path="Prediction_Output_File/FinalPredictions.csv"

            # Converting the prediction into the csv format
            final.to_csv("Prediction_Output_File/FinalPredictions.csv",header=True,mode='a+') #appends result to prediction file

            self.logger.log(self.file_object,'End of Prediction')
            return path

        except Exception as e:
            self.file_object = open("Prediction_Logs/predict.txt", 'a+')
            self.logger.log(self.file_object, 'Error occured while running the prediction!! Error:: %s' % e)
            raise 'predict.py.predictionFromModel: ' + str(e)

        finally:
            self.file_object.close()