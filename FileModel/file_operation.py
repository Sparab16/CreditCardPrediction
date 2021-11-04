import pickle
import os
import shutil
from Logger import AppLogger

class FileOperation:
    '''
    This class shall be used to save the model after training
    '''

    def __init__(self):
        self.current_directory = os.getcwd()
        self.file_object = open('Training_Logs/FileOperations.txt', 'a+')
        self.logger = AppLogger()
        self.model_directory = 'models/'

    def save_model(self, model, filename):
        '''
        Description: Save the model file to the given directory
        :param model: Trained Model
        :param filename: Name of the file to be used
        :return: None
        :failure: Raise Exception
        '''
        try:
            self.file_object = open('Training_Logs/FileOperations.txt', 'a+')
            self.logger.log(self.file_object, 'Entered the save_model method of the File_Operation class')

            path = os.path.join(self.model_directory + filename)

            # If previous model directory exists then remove it
            if os.path.isdir(path):
                shutil.rmtree(self.model_directory)

            # Create the directory with that path
            os.makedirs(path)

            # Saving the model
            with open(path + '/' + filename + '.sav', 'wb') as file:
                pickle.dump(model, file)

            self.logger.log(self.file_object,'Model File '+filename+' saved. Exited the save_model method of the Model_Finder class')

        except Exception as e:
            self.file_object = open('Training_Logs/FileOperations.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred {}'.format(str(e)))
            raise 'file_operations.py.save_model: '+ str(e)
        finally:
            self.file_object.close()

    def load_model(self, filename):
        '''
        Description: Loads the ML model into the memory
        :param filename: Name of the model to be loaded
        :return: Model loaded in the memory
        :failure: Raise Exception
        '''
        try:
            self.file_object = open('Training_Logs/FileOperations.txt', 'a+')
            self.logger.log(self.file_object, 'Entered the load_model method of the File_Operation class')

            with open(self.model_directory + filename + '/' + filename + '.sav', 'rb') as model:
                self.logger.log(self.file_object,'Model File ' + filename + ' loaded. Exited the load_model method of the Model_Finder class')
                return pickle.load(model)

        except Exception as e:
            self.file_object = open('Training_Logs/FileOperations.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred {}'.format(str(e)))
            raise 'file_operations.py.load_model: ' + str(e)

        finally:
            self.file_object.close()

    def find_correct_model_file(self, cluster_number):
        '''
        Description: Selects the correct model based on the cluster number
        :param cluster_number: Cluster number to use for finding the best model
        :return: Model File
        :failure: Raise Exception
        '''
        try:
            self.file_object = open('Training_Logs/FileOperations.txt', 'a+')
            self.logger.log(self.file_object,'Entered the find_correct_model_file method of the File_Operation class')

            # Iterate through the all the model files
            for file in os.listdir(self.model_directory):
                if (file.find(str(cluster_number)) != -1):
                    self.logger.log(self.file_object,'Exited the find_correct_model_file method of the Model_Finder class.')
                    return file.split('.')[0]

        except Exception as e:
            self.file_object = open('Training_Logs/FileOperations.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred {}'.format(str(e)))
            raise 'file_operations.py.find_correct_model_file: ' + str(e)

        finally:
            self.file_object.close()