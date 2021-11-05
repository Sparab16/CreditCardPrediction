import os
import shutil


class MakeDirs:
    """
    This class will be used to create the directory which are needed to run the program
    """

    def __init__(self):
        self.current_path = os.getcwd()
        self.func_list = [self.create_models, self.create_file_from_db, self.create_raw_files_validated,
                          self.create_log_files, self.create_batch_files, self.create_output_file,
                          self.create_kmeans]
        self.current_index = -1
        self.last_index = len(self.func_list)

    def create_models(self):
        """
        This method will create the empty model directory.
        """
        model_path = self.current_path + '/models'
        if os.path.exists(model_path):
            shutil.rmtree(model_path)

        os.makedirs(model_path)

    def create_file_from_db(self):
        """
        This method will create the Prediction and Training folders to store the csv file for the input
        """
        prediction_path = self.current_path + '/Prediction_FileFromDB'
        training_path = self.current_path + '/Training_FileFromDB'

        if os.path.exists(prediction_path):
            shutil.rmtree(prediction_path)

        os.makedirs(prediction_path)

        if os.path.exists(training_path):
            shutil.rmtree(training_path)

        os.makedirs(training_path)

    def create_raw_files_validated(self):
        """
        This method will create the Prediction and Training raw folders to store the good file for the input
        """
        prediction_path = self.current_path + '/Prediction_Raw_Files_Validated'
        training_path = self.current_path + '/Training_Raw_Files_Validated'

        if os.path.exists(prediction_path):
            shutil.rmtree(prediction_path)

        os.makedirs(prediction_path)

        if os.path.exists(training_path):
            shutil.rmtree(training_path)

        os.makedirs(training_path)

    def create_log_files(self):
        """
        This method will create the Prediction and Training log files to store logs of the program
        """
        prediction_path = self.current_path + '/Training_Logs'
        training_path = self.current_path + '/Prediction_Logs'

        if os.path.exists(prediction_path):
            shutil.rmtree(prediction_path)

        os.makedirs(prediction_path)

        if os.path.exists(training_path):
            shutil.rmtree(training_path)

        os.makedirs(training_path)

    def create_batch_files(self):
        """
        This method will create the Prediction and Training batch files for the model training and prediction
        """
        prediction_path = self.current_path + '/Training_Batch_Files'
        training_path = self.current_path + '/Prediction_Batch_files'

        if os.path.exists(prediction_path):
            shutil.rmtree(prediction_path)

        os.makedirs(prediction_path)

        if os.path.exists(training_path):
            shutil.rmtree(training_path)

        os.makedirs(training_path)

    def create_output_file(self):
        """
        This method will create the Prediction output file
        """
        prediction_path = self.current_path + '/Prediction_Output_File'

        if os.path.exists(prediction_path):
            shutil.rmtree(prediction_path)

        os.makedirs(prediction_path)

    def create_kmeans(self):
        """
        This method will create the Kmeans folder to store the elbow plot
        """
        k_means_path = self.current_path + '/K_Means_ElbowPlot'

        if os.path.exists(k_means_path):
            shutil.rmtree(k_means_path)

        os.makedirs(k_means_path)

    def __iter__(self):
        return self

    def __next__(self):
        # Iterate over the functions and return the function definition to call
        self.current_index += 1
        if self.current_index < self.last_index:
            return self.func_list[self.current_index]
        else:
            raise StopIteration


make_dir_obj = MakeDirs()

# Iterate over the function of the class and make the class objects
for func in make_dir_obj:
    func()
