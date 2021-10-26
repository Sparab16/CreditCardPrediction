import shutil
import sqlite3
import os
import csv
from Logger import App_Logger

class Database_Operation:
    '''
    Description: This class shall be used for handling all the sqlite operation.
    '''

    def __init__(self):
        self.path = 'Prediction_Database'
        self.good_file_path = 'Prediction_Raw_Files_Validated/Good_Raw'
        self.current_directory = os.getcwd()
        self.file_object = open('Logs/Database_Operation.txt', 'a+')
        self.logger = App_Logger()

    def createTableDb(self, db_name, col_names):
        '''
        Description: This method creates a table in the given database which will be used to insert the good raw data
                    after validation
        :param db_name: Name of the database that's to be created
        :param col_names: Name of the columns
        :return: None
        :failure: Raise Exception
        '''
        connection = None
        try:
            self.file_object = open('Logs/Database_Operation.txt', 'a+')
            connection = self.dataBaseConnection(db_name)
            cursor = connection.cursor()

            # Check if the database already exists
            cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name ='Good_Raw_Data'")
            if cursor.fetchone()[0] == 1:
                self.logger.log(self.file_object, 'Tables created successfully!')
                self.logger.log(self.file_object, 'Closed {} database succesfully'.format(db_name))

            # If the database not exists
            else:
                for key in col_names.keys():
                    type = col_names[key]

                    # Check if the table exists, if yes then add the columns to the table
                    # else create the table
                    try:
                        connection.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))
                    except:
                        connection.execute('CREATE TABLE Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))

                self.logger.log(self.file_object, 'Tables Created Succesfully!')
                self.logger.log(self.file_object, 'Closed {} database succesfully'.format(db_name))

        except Exception as e:
            self.file_object = open('Logs/Database_Operation.txt', 'a+')
            self.logger.log(self.file_object, 'Error while creating the table in db {}'.format(str(e)))
            raise 'database.py.CreateTableDb: '+ str(e)

        finally:
            if connection is not None:
                connection.close()
            self.logger.log(self.file_object, 'Closed {} database succesfully'.format(db_name))
            self.file_object.close()

    def dataBaseConnection(self, db_name):
        '''
        Description: This method creates the database with the given name and if database already exists then opens up
                    the connection to that Database Prediction
        :param db_name: Name of the database that's to be created
        :return: Connection to the database
        :failure: Raise Exception
        '''
        try:
            conn = sqlite3.connect(self.path + db_name + '.db')
            self.file_object = open('Logs/Database_Operation.txt', 'a+')
            self.logger.log(self.file_object, 'DatabasePrediction {} opened successfully'.format(db_name))
            return conn
        except Exception as e:
            self.file_object = open('Logs/Database_Operation.txt', 'a+')
            self.logger.log(self.file_object, 'Error while connecting to the database {}'.format(str(e)))
            raise 'database.py.databaseConnection: ' + str(e)
        finally:
            self.file_object.close()

    def insertIntoDatabase(self, db_name):
        '''
        Description: This method inserts the Validated data into the sqlite database
        :param db_name: Name of database to insert the data
        :return: None
        :failure: Raise Exception
        '''
        connection = None
        try:
            self.file_object = open('Logs/Database_Operation.txt', 'a+')
            connection = self.dataBaseConnection(db_name)
            training_file = [_ for _ in os.listdir(self.good_file_path)]

            for file_name in training_file:
                with open(self.good_file_path + '/' + file_name) as file:
                    # Skipping the header row
                    next(file)

                    reader = csv.reader(file, delimiter = '\n')
                    for line in enumerate(reader):
                        for list in line[1]:
                            try:
                                connection.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list)))
                                self.logger.log(self.file_object, 'File loaded succesfully {}'.format(file_name))
                                connection.commit()
                            except Exception as e:
                                raise e

        except Exception as e:
            self.file_object = open('Logs/Database_Operation.txt', 'a+')
            self.logger.log(self.file_object, 'Error while creating table {}'.format(str(e)))
            connection.rollback()
            raise 'database.py.InsertIntoTheDatabase: ' + str(e)
        finally:
            if connection is not None:
                connection.close()
            self.file_object.close()

    def selectingDataFromDbIntoCSV(self, db_name):
        '''
        Description: This method exports the data in GoodData table as a csv file in a given location
        :param db_name: Name of the database to export the data
        :return: None
        :failure: Raise Exception
        '''
        connection = None
        try:
            self.file_object = open('Logs/Database_Operation.txt', 'a+')
            self.fileFromDb = 'Prediction_FileFromDB/'
            self.file_name = 'InputFile.csv'

            connection = self.dataBaseConnection(db_name)
            cursor = connection.cursor()

            sqlSelect = "SELECT * FROM Good_Raw_Data"
            cursor.execute(sqlSelect)
            results = cursor.fetchall()

            # Get the headers
            headers = [desc[0] for desc in cursor.description]

            # Make the CSV output directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # Open CSV file for writing
            with open(self.fileFromDb + self.file_name, 'w', newline='') as file:
                csvFile = csv.writer(file, delimiter = ',', lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerow(results)
            file.close()
            self.logger.log(self.file_object, 'File Exported Succesfully')

        except Exception as e:
            self.file_object = open('Logs/Database_Operation.txt', 'a+')
            self.logger.log(self.file_object, 'File Exporting Failed {}'.format(str(e)))
            raise e
        finally:
            if connection is not None:
                connection.close()
            self.file_object.close()