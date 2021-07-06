import requests
from datetime import datetime, timedelta
import pandas as pd

class DataCollection():
    def __init__(self):
        self.__observation_url = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/Observation?_sort=-date&_count='
        self.__patient_url = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/Patient/'
        self.__value_url = self.__observation_url + '200&code=2093-3'
        self.__next = None
        self.__vitals = []
        self.__p_value = []

    '''
    collecting required data

    parameters:
    decision    - decision whether to check vitals or patient values
    '''
    def data_collection(self, decision):
        if self.__next == None:
            url = self.__value_url
        else:
            url = self.__next

        response = requests.get(url)
        check = True
        if response.status_code == 200 and check:
            response = response.json()

            for entry in response['entry']:
                p_id = entry['resource']['subject']['reference'][8:]

                row = self.get_value(p_id, decision)

                chol = entry['resource']['valueQuantity']['value'] / 38.67
                if chol > 5.2:
                    row.append('High')
                else:
                    row.append('Normal')

                if decision == 'vitals':
                    self.__vitals.append(row)
                else:
                    self.__p_value.append(row)

            if len(response['link']) > 1:
                self.__next = response['link'][1]['url']
            else:
                check = False

        if decision == 'vitals':    
            df = pd.DataFrame(self.__vitals, columns = ['Triglyceride (mmol/L)', 'BMI (kg/m2)', 'Diastolic (mm[Hg])', 'Systolic (mm[Hg])', 'Cholesterol Level'])
            df.to_csv('vitals.csv', index = False)
        else:
            df = pd.DataFrame(self.__p_value, columns = ['Race', 'Ethnicity', 'Gender', 'Age', 'Cholesterol Level'])
            df.to_csv('p_value.csv', index = False)

    '''
    getting required value of a patient

    parameters:
    p_id        - patient id
    decision    - decision whether to check vitals or patient values

    returns:
    list of necessary values
    '''
    def get_value(self, p_id, decision):
        if decision == 'vitals':
            try:
                tri_url = self.__observation_url + '1&code=2571-8&patient._id=' + str(p_id)
                tri_response = requests.get(tri_url).json()
                tri_data = tri_response['entry'][0]['resource']['valueQuantity']['value'] / 88.57
                
                bmi_url = self.__observation_url + '1&code=39156-5&patient._id=' + str(p_id)
                bmi_response = requests.get(bmi_url).json()
                bmi_data = bmi_response['entry'][0]['resource']['valueQuantity']['value']

                blood_url = self.__observation_url + '1&code=55284-4&patient._id=' + str(p_id)
                blood_response = requests.get(blood_url).json()
                blood_data = blood_response['entry'][0]['resource']['component']
                diastolic = blood_data[0]['valueQuantity']['value']
                systolic = blood_data[1]['valueQuantity']['value']

                return [tri_data, bmi_data, diastolic, systolic]
            except KeyError:
                return None
        else:
            patient_url = self.__patient_url + str(p_id)
            patient_response = requests.get(patient_url).json()
            genetics = patient_response['extension']
            race = genetics[0]['extension'][1]['valueString']
            ethnicity = genetics[1]['extension'][1]['valueString']

            gender = patient_response['gender']

            birthday = patient_response['birthDate']
            birthday = datetime.strptime(birthday, '%Y-%m-%d')
            age = int((datetime.now() - birthday) / timedelta(days=365))
            age = str(age)

            return [race, ethnicity, gender, age]