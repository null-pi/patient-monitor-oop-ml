#importing necessary library
import pandas as pd
import numpy as np
from .models import Models
from .data_collection import DataCollection

class ML():
    def __init__(self):
        self.__classifier = None                    #classifier object for predicting value
        self.__scores = None                        #score of the model
        self.__ct = None                            #transformer for categorical data
        self.__collector = DataCollection()         #data collector

    '''
    selecting the best model

    parameters:
    file        - file name

    returns:
    classifier  - machine learning model
    scores      - accuracy of the model
    '''
    def model(self, file):
        found = True
        while found:
            try:
                data = pd.read_csv(file + '.csv')
                found = False
            except FileNotFoundError:
                self.__collector.data_collection(file)   #collecting data

        model = Models(data)                                #creating accurate model
        classifier = model.classifier                       #getting the classifer
        scores = model.scores                               #getting the accuracy score
        ct = model.ct

        #check whether a valid classifier is found
        if classifier != None:
            self.__classifier = classifier
            self.__scores = scores
            self.__ct = ct
        else:
            #loop until valid classifier is found
            while classifier == None:
                found = True
                while found:
                    try:
                        data = pd.read_csv(file + '.csv')
                        found = False
                    except FileNotFoundError:
                        self.__collector.data_collection(file)   #collecting data

                model = Models(data)
                classifier = model.classifier
                scores = model.scores
                ct = model.ct
                self.__classifier = classifier
                self.__scores = scores
                self.__ct = ct

        return self.__scores

    '''
    knowing the cholesterol level value

    parameters:
    p_id    - patient id
    value   - patient values

    returns:
    cholesterol level value
    '''
    def know(self, p_id=None, value=None):
        #check which model to implement
        if value == None:
            #implements model built from vitals
            value = self.__collector.get_value(p_id, 'vitals')
            if value == None:
                return None
            else:
                value = [value]
        elif p_id == None:
            #implements model built from patient values
            value = np.reshape(value, (1, len(value)))
            found = True
            while found:
                try:
                    value = np.array(self.__ct.transform(value))
                    found = False
                except ValueError:
                    self.__collector.data_collection('p_value')
                    self.select_model('p_value')

        level = self.__classifier.predict(value)
        return level[0]