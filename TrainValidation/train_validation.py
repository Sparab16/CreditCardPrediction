import os
from TrainValidation.raw_train_validation import Raw_Train_Validation
from TrainValidation.data_transform_training import Data_Transform
from DatabaseTraining.database import Database_Operation
from Logger import AppLogger

class Train_Validation:
    def __init__(self, path):
        self.raw_data = Raw_Train_Validation(path)
        self.data_transform = Data_Transform()
        self.database = Database_Operation()
        self.current_directory = os.getcwd()
        self.file_object = open('Training_Logs/Train_Validation_Log.txt', 'a+')
        self.logger = AppLogger()

    def train_validation(self):
        '''
        Description: This method will act as helper method to call respective methods for validation of the data
        :return: None
        :failure: Raise Exception
        '''
        try:
            self.logger.log(self.file_object, 'Start of the validation on files for training')

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
            self.database.createTableDb('Training', col_names)
            self.logger.log(self.file_object, "Table creation Completed!!")

            # 8. Inserting the data into the table
            self.logger.log(self.file_object, "Insertion of Data into Table started!!!!")
            self.database.insertIntoDatabase('Training')
            self.logger.log(self.file_object, "Insertion in Table completed!!!")
            self.logger.log(self.file_object, "Deleting Good Data Folder!!!")

            # 9. Deleting the good data folder after loading files in table
            self.raw_data.deleteExistingTrainFolder()
            self.logger.log(self.file_object, "Good_Data folder deleted!!!")

            self.logger.log(self.file_object, "Validation Operation completed!!")
            self.logger.log(self.file_object, "Extracting csv file from table")

            # 10. Exporting the data in table to csv file
            self.database.selectingDataFromDbIntoCSV('Training')
        except Exception as e:
            self.file_object = open('Training_Logs/Train_Validation_Log.txt', 'a+')
            self.logger.log(self.file_object, 'Error in Validation {}'.format(str(e)))
            raise 'train_validation.train_validation: '+ str(e)
        finally:
            self.file_object.close()