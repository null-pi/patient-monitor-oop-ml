#import necessary library
import requests
import json
import math
from .patient import Patient
from .monitor_manager import MonitorManager
from datetime import datetime, timedelta
import time

class Display():
    def __init__(self):
        self.__hp_id = -1                       #Health Practitoner ID
        #url for searching
        self.__search = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/Encounter?_sort=-date&_count=200&_include=Encounter:patient&practitioner.identifier=http://hl7.org/fhir/sid/us-npi|'
        self.__patients = []                    #all patients under the health practitioner
        self.__next = None                      #next url to use
        self.__entry_per_page = 10
        self.__selected_patients = []           #all selected patient

    #method for the health practitioner id
    @property
    def id(self):
        return self.__hp_id

    #method for finding current page number
    @property
    def page(self):
        return math.floor(len(self.__patients) / self.__entry_per_page) - 1

    #total number of selected patient
    @property
    def num_selected(self):
        return len(self.__selected_patients)

    #id of selected patient
    def selected(self):
        ids = []
        for patient in self.__selected_patients:
            ids.append(patient['ID'])

        if len(ids) > 0:
            return ids
        else:
            return None

    '''
    login as Health Practitioner

    parameters:
    hp_id   - health practitioner identifier

    returns:
    check   - boolean value
    '''
    def login(self, hp_id):
        url = self.__search + hp_id
        check = self.get_data(url)
        self.__hp_id = hp_id

        return check

    '''
    goes to the next page

    parameters:
    page    - specific page to go to
    '''
    def next_page(self):
        self.get_data(self.__next)

    '''
    create a monitor manager for handling monitor

    parameters:
    frequency   - frequency of the monitor update

    return:
    the created monitor manager
    '''
    def create_monitor_manager(self, frequency, x, y):
        #appending patients that are selected
        selected_patients = []

        #getting patient for specific id
        i = 0
        while i < len(self.__selected_patients):
            j = 0
            while j < len(self.__patients):
                if self.__patients[j].id == self.__selected_patients[i]['ID']:
                    selected_patients.append(self.__patients[j])
                    j = len(self.__patients)
                j += 1
            i += 1

        #creating new monitor manager
        return MonitorManager(self.__hp_id, selected_patients, frequency, x, y)

    '''
    adds patient to the selected patient list

    parameters:
    value   - value of the selected patient
    '''
    def selected_patients(self, value):
        for data in value:
            data = json.loads(data)
            self.__selected_patients.append(data)

    '''
    removes patient to the selected patient list

    parameters:
    value   - value of the removed patient
    '''
    def removed_patients(self, value):
        for data in value:
            data = json.loads(data)
            self.__selected_patients.remove(data)

    '''
    remove monitor
    '''
    def remove_monitor(self):
        self.__selected_patients = []

    '''
    retrieving patient data from the url,
    and adds patient into definite page number

    parameters:
    url     - url for searching
    page    - page number where info will be shown
    search  - whether this is a search criteria
    '''
    def get_data(self, url):
        #retrieving data from the data sent from url
        data = requests.get(url).json()

        #checks whether it reached the end
        if len(data['link']) == 1:
            return False
        else:
            #creates all patients under the health practitioner
            for entry in data['entry']:
                if entry['resource']['resourceType'] == 'Patient':
                    #getting patient related data
                    patient_id = entry['resource']['id']

                    genetics = entry['resource']['extension']
                    race = genetics[0]['extension'][1]['valueString']
                    ethnicity = genetics[1]['extension'][1]['valueString']

                    surname = entry['resource']['name'][0]['family']
                    name_list = entry['resource']['name'][0]['given']
                    name = ''
                    for i in range(len(name_list)):
                        name += name_list[i]

                    gender = entry['resource']['gender']

                    marital_status = entry['resource']['maritalStatus']['text']

                    birthday = entry['resource']['birthDate']
                    birthday = datetime.strptime(birthday, '%Y-%m-%d')
                    age = int((datetime.now() - birthday) / timedelta(days=365))
                    age = str(age)

                    address_list = entry['resource']['address'][0]
                    city = address_list['city']
                    state = address_list['state']
                    country = address_list['country']
                    #patient related data retrieval done

                    #creating new Patient object
                    patient = Patient(patient_id, name, surname, birthday, age, gender, marital_status, city, state, country, race, ethnicity)

                    #adds patient to the end of the list
                    i = 0
                    duplicate = False
                    while i < len(self.__patients):
                        if patient.id == self.__patients[i].id:
                            duplicate = True
                            i = len(self.__patients)
                        i += 1

                    if not duplicate:
                        self.__patients.append(patient)

            self.__next = data['link'][1]['url']
            url = self.__next
            return True

    '''
    shows all patient's basic info between two indexes

    parameters:
    start   - start of the list of patient's info to be shown
    end     - end of the list of patient's info to be shown

    returns:
    data    - json data of the patients to be shown
    '''
    def show_all_patients(self, start):
        data = {}
        data['Patients'] = []

        if start == -1:
            end = len(self.__patients)
            start = end - 1
        else:
            start *= self.__entry_per_page
            end = start + self.__entry_per_page

        for i in range(start, end):
            if i < len(self.__patients):
                data['Patients'].append(self.__patients[i].show_basic_info)

        return data