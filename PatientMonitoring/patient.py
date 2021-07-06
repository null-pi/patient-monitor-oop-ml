class Patient():
    def __init__(self, p_id, name, surname, birthday, age, gender, marital_status, city, state, country, race, ethnicity):
        self.__p_id = p_id
        self.__name = name
        self.__surname = surname
        self.__birthday = birthday
        self.__age = age
        self.__gender = gender
        self.__marital_status = marital_status
        self.__city = city
        self.__state = state
        self.__country = country
        self.__race = race
        self.__ethnicity = ethnicity

    #id of the patient
    @property
    def id(self):
        return self.__p_id

    #name of the patient
    @property
    def name(self):
        return self.__name + ' ' + self.__surname

    #show full profile of the patient
    @property
    def show_profile(self):
        profile = {}
        profile['Patient_ID'] = self.__p_id
        profile['Name'] = self.__name
        profile['Surname'] = self.__surname
        profile['Birthday'] = self.__birthday
        profile['Age'] = self.__age
        profile['Gender'] = self.__gender
        profile['Marital_Status'] = self.__marital_status
        profile['City'] = self.__city
        profile['State'] = self.__state
        profile['Country'] = self.__country
        profile['Race'] = self.__race
        profile['Ethnicity'] = self.__ethnicity

        return profile

    #show basic info of the patient
    @property
    def show_basic_info(self):
        basic_info = {}
        basic_info['Patient_ID'] = self.__p_id
        basic_info['Name'] = self.__name
        basic_info['Surname'] = self.__surname

        return basic_info