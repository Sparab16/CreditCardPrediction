import os
import pandas as pd
from Logger import App_Logger

class DataTransformPredict:

    '''
    Description: This class is used for transforming/scaling the raw training data before loading it in the database.
    '''

    def __init__(self):
        self.good_raw_data_path = 'Prediction_Raw_Files_Validated/Good_Raw'
        self.current_directory = os.getcwd()
        self.file_object = open(self.current_directory + '/Data_Transform_Prediction.txt', 'a+')
        self.logger = App_Logger()

    def replaceMissingWithNull(self):
        '''
        Description: This method replaces the missing values in the columns with "NULL" to store in the table.
        :return: None
        :failure: Raise Exception
        '''
        try:
            self.file_object = open(self.current_directory + 'Data_Transform_Prediction.txt', 'a+')
            training_file = [_ for _ in os.listdir(self.good_raw_data_path)]
            for file_name in training_file:
                data = pd.read_csv(self.good_raw_data_path + '/' + file_name)
                data.to_csv(self.good_raw_data_path + '/' + file_name, index=None, header=True)
                self.logger.log(self.file_object, 'Quotes Added Successfully!! {}'.format(file_name))
        except Exception as e:
            self.file_object = open(self.current_directory + 'Data_Transform_Prediction.txt', 'a+')
            self.logger.log(self.file_object, 'Data Transformation failed because {}'.format(str(e)))
            raise e
        finally:
            self.file_object.close()