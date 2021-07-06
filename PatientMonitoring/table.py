#importing necessary libraries
import requests
from .blood_pressure import BloodPressure

class Table():
    def __init__(self, p_ids, p_names, frequency):
        self.__p_ids = p_ids                        # list of patient ids
        self.__p_names = p_names                    # list of patient names
        self.__frequency = frequency                # frequency

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        self.__frequency = value

    '''
    creating table

    returns:
    blood pressure data of the selected patient
    '''
    def create_table(self):
        #blood pressure values
        details = BloodPressure(self.__p_ids).create_table()
        patients = []

        for i in range(len(self.__p_ids)):
            patients.append({'ID': self.__p_ids[i], 'Name': self.__p_names[i], 'Value': details[self.__p_ids[i]]})

        return patients
