#import necessary classes
from .monitor import Monitor
from .patient import Patient
from .body_vitals import BodyVitals
import requests
from datetime import datetime, timedelta

class MonitorManager():
    def __init__(self, hp_id, selected_patients, frequency, systolic, diastolic):
        self.__monitor = []                           #contains all monitors in monitor manager
        self.__hp_id = hp_id                            #health practitioner id
        self.__search = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/Encounter?_sort=-date&_count=1&_include=Encounter:patient&practitioner.identifier=http://hl7.org/fhir/sid/us-npi|'
        self.__selected_patients = selected_patients    #selected patients who will be in monitor
        self.__frequency = frequency               #frequency of refresh
        self.__table = {'CHOLESTEROL': '', 'BLOOD_PRESSURE': ''}
        self.__systolic = systolic
        self.__diastolic = diastolic

    #monitor's frequency
    @property
    def frequency(self):
        return self.__frequency

    #setting monitor's frequency
    @frequency.setter
    def frequency(self, value):
        self.__frequency = value

    @property
    def systolic(self):
        return self.__systolic

    @property
    def diastolic(self):
        return self.__diastolic

    @systolic.setter
    def systolic(self, value):
        self.__systolic = value

    @diastolic.setter
    def diastolic(self, value):
        self.__diastolic = value

    '''
    show full profile of a patient

    parameters:
    patient_id  - id of the patient

    returns:
    data of the full profile of the patient
    '''
    def show_patient(self, patient_id):
        data = None
        i = 0
        while i < len(self.__selected_patients):
            if patient_id == self.__selected_patients[i].id:
                data = self.__selected_patients[i].show_profile
                i = len(self.__selected_patients)
            
            i += 1

        return data

    '''
    creating monitor for showing cholesterol data

    returns:
    data of the cholesterol data of all selected patients
    '''
    def create_monitor(self):
        #separating patient id and name into different lists
        patient_id = []
        for patient in self.__selected_patients:
            patient_id.append(patient.id)

        #creating cholesterol monitor
        for body_vital in BodyVitals:
            monitor = Monitor(body_vital, patient_id)
            self.__monitor.append(monitor)
            self.__table[body_vital.name] = monitor.create()
            
        return self.create_table()

    '''
    adding new patient to the monitor

    parameters:
    patient - adding a specific patient

    returns:
    cholesterol data of all the selected patient
    '''
    def add_patient(self, patient):
        #searching for duplicate patients
        duplicate = False
        i = 0
        while i < len(self.__selected_patients):
            if self.__selected_patients[i].id == patient.id:
                duplicate = True
                i = len(self.__selected_patients)
            i += 1

        #if no duplicate is visible, add the patient to the monitor
        if not duplicate:
            self.__selected_patients.append(patient)

            #'add' is refering to addition for notifying other monitors
            return self.notify(patient.id, 'add')

        return None

    '''
    removing patient from monitor

    parameters:
    patient_id  - id of the patient
    name        - name of the patient

    returns:
    cholesterol data of the remaining patient
    '''
    def remove_patient(self, patient_id, name):
        i = 0
        while i < len(self.__selected_patients):
            if self.__selected_patients[i].id == patient_id:
                self.__selected_patients.pop(i)
                i = len(self.__selected_patients)

            i += 1

        return self.notify(patient_id, 'rem')

    '''
    refresh monitors on their specific frequency

    returns:
    cholesterol data of all the selected patient
    '''
    def refresh(self):
        for monitor in self.__monitor:
            self.__table[monitor.body_vital_name] = monitor.create()

        return self.create_table()        

    '''
    notifying the monitor

    parameters:
    p_id        - id of the patient
    name        - name of the patient
    decision    - decision whether to add or remove

    returns:
    cholesterol data of all the selected patient
    '''
    def notify(self, p_id, decision):
        for monitor in self.__monitor:
            self.__table[monitor.body_vital_name] = monitor.update(p_id, decision)

        return self.create_table()

    def create_table(self):
        transfer = []
        cholesterol = False
        blood_pressure = False

        for patient in self.__selected_patients:
            data = {'ID': patient.id, 'Name': patient.name}
            if self.__table['CHOLESTEROL'] != '':
                data['Chol_Value'] = self.__table['CHOLESTEROL'][patient.id]['Value']
                data['Chol_Unit'] = self.__table['CHOLESTEROL'][patient.id]['Unit']
                data['Chol_Time'] = self.__table['CHOLESTEROL'][patient.id]['Time']
                data['Chol_Avg'] = self.__table['CHOLESTEROL'][patient.id]['Average']
                cholesterol = True

            if self.__table['BLOOD_PRESSURE'] != '':
                data['Systolic'] = self.__table['BLOOD_PRESSURE'][patient.id]['Systolic']
                data['Diastolic'] = self.__table['BLOOD_PRESSURE'][patient.id]['Diastolic']
                data['Pressure_Time'] = self.__table['BLOOD_PRESSURE'][patient.id]['Time']
                data['Pressure_Unit'] = self.__table['BLOOD_PRESSURE'][patient.id]['Unit']
                blood_pressure = True

            transfer.append(data)

        table = {'Patients': transfer}

        return table

    '''
    search patient based on value
    and puts it in the front of the page

    parameters:
    value   - search parameter

    returns:
    "yes" or "no"
    '''
    def search(self, value):
        url = self.__search + self.__hp_id + '&patient'         #root url to search the patient
        #seeing if the given value can be transformed into integer
        try:
            value = int(value)                        #changing the value into int
            search = url + '._id=' + str(value)            #url to search for patients

            #getting patient id from sent data
            data = requests.get(search).json()
            if data['total'] == 0:
                #set patient id to None
                return 'no'
            else:
                #verifying the patient is found
                self.create_patient(data)
                return 'yes'
        except ValueError:
            search = url + '.given:exact=' + value        #url for searching the patient
            
            #retrieving given name from sent data
            data = requests.get(search).json()
            if data['total'] == 0:
                #if for given name no patient is found
                search = url + '.family:exact=' + value

                #retrieving family name from sent data
                data = requests.get(search).json()
                if data['total'] != 0:
                    #verifying the patient is found
                    self.create_patient(data)
                    return 'yes'
                else:
                    return 'no'
            else:
                #verifying the patient is found
                self.create_patient(data)
                return 'yes'

    '''
    create patient based on the response

    parameters:
    data    - response given by the url
    '''
    def create_patient(self, data):
        #getting patient related data
        patient_id = data['entry'][1]['resource']['id']

        genetics = data['entry'][1]['resource']['extension']
        race = genetics[0]['extension'][1]['valueString']
        ethnicity = genetics[1]['extension'][1]['valueString']

        surname = data['entry'][1]['resource']['name'][0]['family']
        name_list = data['entry'][1]['resource']['name'][0]['given']
        name = ''
        for i in range(len(name_list)):
            name += name_list[i]

        gender = data['entry'][1]['resource']['gender']

        marital_status = data['entry'][1]['resource']['maritalStatus']['text']

        birthday = data['entry'][1]['resource']['birthDate']
        birthday = datetime.strptime(birthday, '%Y-%m-%d')
        age = int((datetime.now() - birthday) / timedelta(days=365))
        age = str(age)

        address_list = data['entry'][1]['resource']['address'][0]
        city = address_list['city']
        state = address_list['state']
        country = address_list['country']

        #creating new Patient object
        patient = Patient(patient_id, name, surname, birthday, age, gender, marital_status, city, state, country, race, ethnicity)

        #adding patient to the monitor
        self.add_patient(patient)