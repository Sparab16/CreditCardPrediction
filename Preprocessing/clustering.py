import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from Logger import App_Logger
from FileModel.file_operation import FileOperation

class KMeansClustering:
    '''
    This class shall be used to divide the data into clusters before training the model
    '''

    def __init__(self):
        self.current_directory = os.getcwd()
        self.file_object = open('PreprocessorLogs/Clustering.txt', 'a+')
        self.logger = App_Logger()

    def elbow_plot(self, data):
        '''
        Description: This methods decides the optimum number of clusters to the file.
        :param data: Pandas Dataframe
        :return: number of clusters needed
        :failure: Raise Exception
        '''

        try:
            self.file_object = open('PreprocessorLogs/Clustering.txt', 'a+')
            self.logger.log(self.file_object, 'Entered the elbow_plot method of the KMeansClustering class')
            wcss=[] # initializing an empty list

            for i in range(1, 11):
                # Initializing the kmeans object
                kmeans = KMeans(n_clusters=i, init='k-means++',random_state=42)
                kmeans.fit(data)
                wcss.append(kmeans.inertia_)

            plt.plot(range(1, 11), wcss)
            plt.title('The Elbow Plot')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            #plt.show()
            plt.savefig('K_Means_ElbowPlot/K-Means_Elbow.PNG') # saving the elbow plot locally

            # finding the value of the optimum cluster programmatically
            self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            self.logger.log(self.file_object, 'The optimum number of clusters are {}'.format(str(self.kn.knee)))
            self.logger.log(self.file_object, 'Existing the elbow plot method')
            return self.kn.knee

        except Exception as e:
            self.file_object = open('PreprocessorLogs/Clustering.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred {}'.format(str(e)))
            raise 'clustering.py.elbow_plot: ' + str(e)
        finally:
            self.file_object.close()

    def create_clusters(self, data, no_clusters):
        '''
        Description: Create a new dataframe consisting of the cluster information.
        :param data: Pandas Dataframe
        :param no_clusters: Number of clusters provided
        :return: A dataframe with cluster column added
        :failure: Raise Exception
        '''
        try:
            self.file_object = open('PreprocessorLogs/Clustering.txt', 'a+')
            self.logger.log(self.file_object, 'Entered the create_clusters method of the KMeansClustering class')

            kmeans = KMeans(n_clusters=no_clusters, init='k-means++', random_state=42)

            # Divide the data into clusters
            y_kmeans = kmeans.fit_predict(data)

            # Saving the fitted model
            file_operations = FileOperation()
            file_operations.save_model(kmeans, 'KMeans')

            data['Cluster'] = y_kmeans
            self.logger.log(self.file_object, 'succesfully created '+str(self.kn.knee)+ 'clusters. Exited the create_clusters method of the KMeansClustering class')

            return data

        except Exception as e:
            self.file_object = open('PreprocessorLogs/Clustering.txt', 'a+')
            self.logger.log(self.file_object, 'Error Occurred {}'.format(str(e)))
            raise 'clustering.py.create_clusters: ' + str(e)
        finally:
            self.file_object.close()