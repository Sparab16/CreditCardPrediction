import os
import json
import re
import shutil
import pandas as pd
from Logger import App_Logger


class Raw_Train_Validation:
    '''
    Description: This class is used for handling all the valition on the raw training data.
    '''

    def __init__(self, path):
        self.directory = path
        self.schema_path = 'schema_training.json'
        self.current_directory = os.getcwd()
        self.file_object = open(self.current_directory + '/Raw_Train_Validation.txt', 'a+')
        self.logger = App_Logger()

    def deleteExistingTrainFolder(self):
        '''
        Description: This method deletes the directory made to store the training data once it is inserted into the
                    DatabaseTraining. Once the files are loaded in the DB, deleting the directory ensures space optimization.
        :return: None
        :failure: Raise Exception
        '''
        try:
            path = 'Training_Raw_Files_Validated/'
            if os.path.isdir(path + 'Good_Raw/'):
                shutil.rmtree(path + 'Good_Raw/')
                self.file_object = open(self.current_directory + 'Raw_Train_Validation.txt', 'a+')
                self.logger.log(self.file_object, 'Good Raw directory is deleted successfully')
        except Exception as e:
            self.file_object = open(self.current_directory + 'Raw_Train_Validation.txt', 'a+')
            self.logger.log(self.file_object, 'Error while deleting directory {}'.format(str(e)))
            raise 'raw_train_validation.deleteExistingTrainFolder: '+ str(e)
        finally:
            self.file_object.close()

    def createDirectoryTrainFolder(self):
        '''
        Description: This method creates directories to store the data after validating the training data.
        :return: None
        :failure: Raise Exception
        '''
        try:
            path = os.path.join("Training_Raw_Files_Validated/", "Good_Raw")
            if not os.path.isdir(path):
                os.mkdir(path)
        except Exception as e:
            self.file_object = open(self.current_directory + 'Raw_Train_Validation.txt', 'a+')
            self.logger.log(self.file_object, 'Error while creating directory {}'.format(str(e)))
            self.file_object.close()
            raise 'raw_train_validation.createDirectoryTrainFolder: ' + str(e)

    def valuesFromSchema(self):
        '''
        Description: This method will extract all the information from the pre-defined schema file
        :return: length_date_stamp, length_time_stamp, col_names, no_columns
        :failure: Raise Exception
        '''
        try:
            # Open the schema file for reading the values
            self.file_object = open(self.current_directory + 'Raw_Train_Validation.txt', 'a+')
            self.logger.log(self.file_object, 'Opening the schema file for reading operation')
            with open(self.schema_path) as schema_file:
                schema = json.load(schema_file)
                schema_file.close()

            length_date_stamp = schema['LengthOfDateStampInFile']
            length_time_stamp = schema['LengthOfTimeStampInFile']
            col_names = schema['ColName']
            no_columns = schema['NumberofColumns']

            self.logger.log(self.file_object, 'LengthOfDate = {}, LengthOfTime = {}, NumberOfColumns = {}'
                            .format(length_date_stamp, length_time_stamp, no_columns))

            return length_date_stamp, length_time_stamp, col_names, no_columns

        except Exception as e:
            self.file_object = open(self.current_directory + 'Raw_Train_Validation.txt', 'a+')
            self.logger.log(self.file_object, str(e))
            raise e
        finally:
            self.file_object.close()

    def fileRegex(self):
        '''
        Description: This method contains the regex based on the filename given the 'schema' file.
                    This regex can be used to validate the filename of the training data.
        :return: Regex Pattern
        :failure: None
        '''
        file_regex = "[creditCardFraud]+[_]+[\d_]+[\d]+\.csv"
        return file_regex

    def validateFile(self, regex, length_date_stamp, length_time_stamp):
        '''
        Description: This function validates the name of the training csv file as per the given regex pattern
                    is used to do the validation. If the validation is not successful, the file will not be used
                    as the input for the training ML model
        :param regex: Regular Expression pattern for the filename
        :param length_date_stamp: Date when the file is created
        :param length_time_stamp: Time when the file is created
        :return: None
        :Failure: Raise Exception
        '''
        try:
            # Delete the directories for good data folder if the last run was not succesful and folders are not deleted
            self.deleteExistingTrainFolder()

            # Create the new directory
            self.createDirectoryTrainFolder()

            # Iterate over through the training files for validation
            training_files = [_ for _ in os.listdir(self.directory)]

            self.file_object = open(self.current_directory + 'Raw_Train_Validation.txt', 'a+')

            for filename in training_files:
                if (re.match(regex, filename)):
                    split_at_dot = re.split('.csv', filename)
                    split_at_dot = re.split('_', split_at_dot[0])

                    # Validation of length of date and length of time
                    if len(split_at_dot[1]) == length_date_stamp and len(split_at_dot[2]) == length_time_stamp:
                        shutil.copy('Training_Batch_Files/' + filename, 'Training_Raw_Files_Validated/Good_Raw')
                    else:
                        self.logger.log(self.file_object, 'Invalid File Name!! {}'.format(filename))
                else:
                    self.logger.log(self.file_object, 'Invalid File Name!! {}'.format(filename))

        except Exception as e:
            self.file_object = open(self.current_directory + 'Raw_Train_Validation.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred while validating the filenames {}'.format(str(e)))
            raise 'raw_train_validation.validateFile: ' + str(e)

        finally:
            self.file_object.close()

    def validateColumnLength(self, no_columns):
        '''
        Description: This function validates the number of columns in the csv file.
        :param no_columns: Number of columsn expected
        :return: None
        :failure: Raise Exception
        '''
        try:
            self.file_object = open(self.current_directory + 'Raw_Train_Validation.txt', 'a+')
            self.logger.log(self.file_object, 'Column length validation started')

            for file_name in os.listdir('Training_Raw_Files_Validated/Good_Raw/'):
                csv = pd.read_csv('Training_Raw_Files_Validated/Good_Raw/' + file_name)
                if csv.shape[1] != no_columns:
                    shutil.rmtree('Training_Raw_Files_Validated/Good_Raw/' + file_name)
                    self.logger.log(self.file_object, 'Invalid column length for the file {}'.format(file_name))
            self.logger.log(self.file_object, 'Column Length Validation is completed')

        except Exception as e:
            self.file_object = open(self.current_directory + 'Raw_Train_Validation.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred in Validating columns length {}'.format(str(e)))
            raise 'raw_train_validation.validateColumnLength: ' + str(e)
        finally:
            self.file_object.close()

    def validateMissingValues(self):
        '''
        Description: This function validates if any column in the csv file has all values missing.
                    If all the values are missing, the file can be deleted from the Good Raw folder
        :return: None
        :failure: Raise Exception
        '''
        try:
            self.file_object = open(self.current_directory + 'Raw_Train_Validation.txt', 'a+')
            self.logger.log(self.file_object, 'Missing Values Validation Started')

            for file_name in os.listdir('Training_Raw_Files_Validated/Good_Raw/'):
                csv = pd.read_csv('Training_Raw_Files_Validated/Good_Raw/' + file_name)
                missing = False

                for col_name in csv:
                    # Checking if there are any missing values
                    if (len(csv[col_name]) - csv[col_name].count()) == len(csv[col_name]):
                        missing = True
                        shutil.rmtree('Training_Raw_Files_Validated/Good_Raw/' + file_name)
                        self.logger.log(self.file_object, 'Invalid column length for the file {}'.format(file_name))
                        break
                if not missing:
                    csv.rename(columns = {"Unnamed : 0": "Wafer"}, inplace=True)
                    csv.to_csv("Training_Raw_Files_Validated/Good_Raw/" + file_name, index=None, header=True)

        except Exception as e:
            self.file_object = open(self.current_directory + 'Raw_Train_Validation.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred while Validating the missing values {}'.format(str(e)))
            raise 'raw_train_validation.validateMissingValues: ' + str(e)
        finally:
            self.file_object.close()















