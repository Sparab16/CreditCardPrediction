import os

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from Logger import App_Logger

class Preprocessor:
    '''
    This class shall be used to clean and transform the data before the training.
    '''

    def __init__(self):
        self.current_directory = os.getcwd()
        self.file_object = open(self.current_directory + '/Preprocessing.txt', 'a+')
        self.logger = App_Logger()

    def separate_label_feature(self, data, label_column_name):
        '''
        Description: This method separates the features and a label columns
        :param data: Pandas Dataframe
        :param label_column_name: Target column name to be given
        :return: Returns two dataframes, one containing the features and other is labels
        :failure: Raise Exception
        '''
        try:
            self.file_object = open(self.current_directory + '/Preprocessing.txt', 'a+')
            self.logger.log(self.file_object,'Entered the separate_label_feature method of the Preprocessor class')

            # Drop the target column
            self.X = data.drop(labels = label_column_name, axis = 1)

            # Filter the target column
            self.Y = data[label_column_name]

            self.logger.log(self.file_object, 'Label separation succesfull.')
            return self.X, self.Y

        except Exception as e:
            self.file_object = open(self.current_directory +  '/Preprocessing.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred {}'.format(e))
            raise 'preprocessing.py.separateLabelFeatures: ' + str(e)
        finally:
            self.file_object.close()

    def is_null_present(self, data):
        '''
        Description: This method checks whether there are null values present in the dataset
        :param data: Pandas Dataframe
        :return: True if the null values present, else False. If the null values present also returns
                the name of the columns for which null values are present
        :failure: Raise Exception
        '''
        try:
            self.file_object = open(self.current_directory + '/Preprocessing.txt', 'a+')
            self.logger.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')

            self.cols_with_missing_values = []
            self.cols = data.columns

            # Check for the count of the nulls
            self.null_counts = data.isna().sum()
            for i in range(len(self.null_counts)):
                if self.null_counts[i] > 0:
                    self.cols_with_missing_values.append(self.cols[i])

            self.logger.log(self.file_object,'Finding missing values is a success. Exited the is_null_present method of the Preprocessor class')
            return self.null_counts, self.cols_with_missing_values
        except Exception as e:
            self.file_object = open(self.current_directory + '/Preprocessing.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred {}'.format(str(e)))
            raise 'preprocessing.py.is_null_present: ' + str(e)
        finally:
            self.file_object.close()

    def scale_numerical_columns(self, data):
        '''
        Description: This method scales the numerical values using the Standard Scaler
        :param data: Pandas Dataframe
        :return: Scaled Dataframe
        :failure: Raise Exception
        '''
        try:
            self.file_object = open(self.current_directory + '/Preprocessing.txt', 'a+')
            self.logger.log(self.file_object,'Entered the scale_numerical_columns method of the Preprocessor class')

            num_df = data.select_dtypes(include=['int64']).copy()
            scaler = StandardScaler()
            scaled_df = scaler.fit_transform(num_df)
            scaled_df = pd.DataFrame(data=scaled_df, columns=num_df.columns)
            self.logger.log(self.file_object, 'scaling for numerical values successful. Exited the scale_numerical_columns method of the Preprocessor class')
            return scaled_df

        except Exception as e:
            self.file_object = open(self.current_directory + '/Preprocessing.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred {}'.format(str(e)))
            raise 'preprocessing.py.scale_numerical_columns: '+ str(e)
        finally:
            self.file_object.close()