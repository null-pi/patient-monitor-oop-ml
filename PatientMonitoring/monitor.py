#import necessary classes
from .body_vitals_factory import BodyVitalsFactory

class Monitor():
    def __init__(self, body_vital, patient_id):
        self.__patient_id = patient_id          #list of id of all selected patient
        #self.__patient_name = patient_name      #list of names of all selected patient

        #search for the specific body vital
        self.__body_vital = body_vital.value  #the body vital shown by monitor
        self.__body_vital_name = body_vital.name
                

    @property
    def body_vital_name(self):
        return self.__body_vital_name

    '''
    show body vitals data

    returns:
    body vitals data of the selected patient
    '''
    def create(self):
        obj = self.__body_vital(self.__patient_id)
        data = obj.create_vitals()

        return data

    '''
    update the monitor based on notification

    returns:
    body vitals data of the selected patient
    '''
    def update(self, p_id, decision):
        #update when addition of patient happens
        if decision == 'add':
            self.__patient_id.append(p_id)
            data = self.create()

        #update when removal of a patient happens
        elif decision == 'rem':
            i = 0
            while i < len(self.__patient_id):
                if p_id == self.__patient_id[i]:
                    self.__patient_id.pop(i)
                    i = len(self.__patient_id)
                i += 1

            data = self.create()

        return data