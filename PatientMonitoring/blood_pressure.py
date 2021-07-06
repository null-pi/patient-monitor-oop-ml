# import necessary classes
import requests
from .body_vitals_factory import BodyVitalsFactory

class BloodPressure(BodyVitalsFactory):
    def __init__(self, p_id):
        self.__p_id = p_id  #list of selected patient id

        #url for searching
        self.__search = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/Observation?code=55284-4&_sort=-date&_count='

    '''
    showing the body vitals data for the selected patients

    returns:
    blood pressure data of the selected patient
    '''
    def create_vitals(self):
        details = {}

        for i in range(len(self.__p_id)):
            url = self.__search + '1&patient=' + self.__p_id[i]

            data = requests.get(url).json()

            if data['total'] > 0:
                time = data['entry'][0]['resource']['effectiveDateTime']
                time = time[:10] + ' ' + time[11:]
                blood_data = data['entry'][0]['resource']['component']
                diastolic = blood_data[0]['valueQuantity']['value']
                systolic = blood_data[1]['valueQuantity']['value']
                unit = blood_data[0]['valueQuantity']['unit']

                details[self.__p_id[i]] = {'Systolic': systolic, 'Diastolic': diastolic, 'Unit': unit, 'Time': time}
            else:
                details[self.__p_id[i]] = {'Systolic': 'unavailable', 'Diastolic': 'unavailable', 'Unit': '', 'Time': 'unavailable'}

        return details

    '''
    creating table for the lastest observation for patients with high systolic pressure

    returns:
    latest blood pressure data of patients with high systolic pressure
    '''
    def create_table(self):
        details = {}

        for i in range(len(self.__p_id)):
            url = self.__search + '5&patient=' + self.__p_id[i]
            details[self.__p_id[i]] = []
            data = requests.get(url).json()

            if data['total'] > 0:
                for item in data['entry']:
                    time = item['resource']['effectiveDateTime']
                    time = time[:10] + ' ' + time[11:]
                    systolic = item['resource']['component'][1]['valueQuantity']['value']
                    unit = item['resource']['component'][1]['valueQuantity']['unit']

                    #sorting blood pressure value by time
                    if len(details[self.__p_id[i]]) > 0:
                        j = 0
                        while j < len(details[self.__p_id[i]]):
                            if time < details[self.__p_id[i]][j]['Time']:
                                details[self.__p_id[i]].insert(j, {'Systolic': systolic, 'Unit': unit, 'Time': time})
                                j = len(details[self.__p_id[i]])
                            j += 1
                    else:
                        details[self.__p_id[i]].append({'Systolic': systolic, 'Unit': unit, 'Time': time})

        return details