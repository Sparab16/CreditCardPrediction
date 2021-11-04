import os

from PredictionValidation.pred_raw_validation import PredictionDataValidation
from PredictionValidation.data_transform_prediction import DataTransformPredict
from DatabasePrediction.database import Database_Operation
from Logger import AppLogger

class PredictionValidation:

    def __init__(self, path):
        self.raw_data = PredictionDataValidation(path)
        self.data_transform = DataTransformPredict()
        self.database = Database_Operation()
        self.current_directory = os.getcwd()
        self.file_object = open("Prediction_Logs/PredictionValidation.txt", 'a+')
        self.logger = AppLogger()

    def prediction_validation(self):
        '''
        Description: This method will act as helper method to call respective methods for validation of the data
        :return: None
        :failure: Raise Exception
        '''
        try:
            self.logger.log(self.file_object,'Start of Validation on files for prediction!!')

            # Extracting values from the prediction schema
            length_date_stamp, length_time_stamp, col_names, no_columns = self.raw_data.valuesFromSchema()

            # 1. Validating the file name with regex pattern
            filename_regex = self.raw_data.fileRegex()

            # 2. Validating the file name of prediction files
            self.raw_data.validateFile(filename_regex, length_date_stamp, length_time_stamp)

            # 3. Validating the columns name in the file
            self.raw_data.validateColumnLength(no_columns)

            # 4. Validating if the any column has the missing values
            self.raw_data.validateMissingValues()

            self.logger.log(self.file_object, 'Raw Data Validation Complete!!')

            # 5. Start the data transformation
            self.logger.log(self.file_object, 'Starting Data Transformation')

            # 6. Replacing the blank values with the 'null' values to insert in the database table
            self.data_transform.replaceMissingWithNull()
            self.logger.log(self.file_object, 'Data Transformation is Completed')

            # 7. Creating the DatabaseTraining with the given name, if present open the connection.
            self.logger.log(self.file_object, 'Creating Training DatabaseTraining and tables on the basis of the given schema')
            self.database.createTableDb('Prediction', col_names)
            self.logger.log(self.file_object, "Table creation Completed!!")

            # 8. Inserting the data into the table
            self.logger.log(self.file_object, "Insertion of Data into Table started!!!!")
            self.database.insertIntoDatabase('Prediction')
            self.logger.log(self.file_object, "Insertion in Table completed!!!")
            self.logger.log(self.file_object, "Deleting Good Data Folder!!!")

            # 9. Deleting the good data folder after loading files in table
            self.raw_data.deleteExistingTrainFolder()
            self.logger.log(self.file_object, "Good_Data folder deleted!!!")

            self.logger.log(self.file_object, "Validation Operation completed!!")
            self.logger.log(self.file_object, "Extracting csv file from table")

            # 10. Exporting the data in table to csv file
            self.database.selectingDataFromDbIntoCSV('Prediction')

        except Exception as e:
            self.file_object = open('Prediction_Logs/Prediction_Validation.txt', 'a+')
            self.logger.log(self.file_object, 'Error in Validation {}'.format(str(e)))
            raise 'prediction_validation.py.prediction_validation: '+ str(e)
        finally:
            self.file_object.close()