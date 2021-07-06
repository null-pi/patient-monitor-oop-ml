# import necessary classes
import requests
from .body_vitals_factory import BodyVitalsFactory

class Cholesterol(BodyVitalsFactory):
    def __init__(self, p_id):
        self.__p_id = p_id  #list of selected patient id

        #url for searching
        self.__search = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/Observation?code=2093-3&_sort=-date&_count=1&patient='

    '''
    showing the body vitals data for the selected patients

    returns:
    cholesterol data of the selected patient
    '''
    def create_vitals(self):
        details = {}
        value_list = []

        for i in range(len(self.__p_id)):
            url = self.__search + self.__p_id[i]

            data = requests.get(url).json()

            if data['total'] > 0:
                time = data['entry'][0]['resource']['effectiveDateTime']
                time = time[:10] + ' ' + time[11:]
                value = data['entry'][0]['resource']['valueQuantity']['value']
                unit = data['entry'][0]['resource']['valueQuantity']['unit']

                details[self.__p_id[i]] = {'Value': value, 'Unit': unit, 'Time': time}
                value_list.append(value)
            else:
                details[self.__p_id[i]] = {'Value': 'unavailable', 'Unit': '', 'Time': 'unavailable'}
                value_list.append('unavailable')

        avg = self.average(value_list)
        
        for p_id in self.__p_id:
            details[p_id]['Average'] = avg

        return details

    '''
    finding average of all the values

    parameters:
    value   - list of all cholesterol value

    returns:
    average value of the cholesterol values
    '''
    def average(self, values):
        calculated = False
        if len(values) > 1:
            total = 0
            length = 0
            for value in values:
                if not value == 'unavailable':
                    total += value
                    length += 1
                    calculated = True

        if calculated:
            return total / length
        else:
            return 10000