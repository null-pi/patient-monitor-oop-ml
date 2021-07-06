# importing necessary library
from flask import Flask, render_template, request, redirect, url_for
import json
from PatientMonitoring import Display, MonitorManager, Table
from MachineLearning import ML

# defining app name
app = Flask(__name__)
app.secret_key = 'sldjf;akdfai2039u4nnskf03r9efj934r'

# global variable to be used
display = None
monitor_manager = None
table = None
ml = None
ml_score_vitals = -1
ml_score_p_value = -1
ml_vitals = None
ml_p_value = None
cholesterol = 0
blood_pressure = 0

'''
the login page of the webapp
'''
@app.route('/')
def login():
    # calling all global variables
    global display
    global monitor_manager
    global table
    global ml
    global ml_score_vitals
    global ml_score_p_value

    # whether to flag error or help message
    show = 'no'
    if request.args.get('show'):
        show = 'yes'

    # changing the variables to the initial state
    display = None
    monitor_manager = None
    table = None
    ml = None
    ml_score = -1

    # opening the page
    return render_template('login.htm', show=show)

'''
the main page after a practitioner logs in
'''
@app.route('/home', methods=['GET', 'POST'])
def home():
    global display
    global monitor_manager

    # checks what type of request was made, and service them accordingly
    if request.method == 'POST':
        try:
            # removing monitor from display
            data = json.loads(request.form['json'])         # retrieves data sent to this page
            monitor_manager = None
            display.remove_monitor()
            
            patients = display.show_all_patients(0)         # displays from start to a certain number
            num = display.num_selected                      # total number of selected patients
            selected = display.selected()

            # redirect to the /home/0 for showing all patients
            return render_template('home.htm', patients=patients['Patients'], num=num, selected=selected)
        except KeyError:
            # creating Display object for global usage
            # and maximum entry per page
            display = Display()

            # checks whether patient exist or not
            check = display.login(request.form['login'])

            # if practitioner is valid, show all patients
            if check:
                patients = display.show_all_patients(0)     # displays from start to a certain number
                num = display.num_selected                  # total number of selected patients
                selected = display.selected()

                # opening the page
                return render_template('home.htm', patients=patients['Patients'], num=num, selected=selected)
            else:
                # show the login page, if the practitioner is invalid
                return redirect(url_for('login', show='yes'))
    else:
        patients = display.show_all_patients(0)             # displays from start to a certain number
        num = display.num_selected                          # total number of selected patients
        selected = display.selected()                       # select the selected patients
        # opening the page
        return render_template('home.htm', patients=patients['Patients'], num=num, selected=selected)
        
'''
the page when user wants to see more patients
creates new page of patients for seeing

parameters:
page    - current page number
'''
@app.route('/home/<page>', methods=['GET', 'POST'])
def new_home(page):
    global display

    # checks request type
    if request.method == 'POST':
        data = json.loads(request.form['json'])             # retrieves data sent to this page
        page = int(page)

        # add selected patient, if it does not exist
        display.selected_patients(data['Selected'])
        # command to remove any existing selected patient
        display.removed_patients(data['Removed'])

        num = display.num_selected                          # displays total selected patient
        # checks whether all patients are shown
        if page > display.page:
            display.next_page()                             # if all patients are shown, collect new patients

        patients = display.show_all_patients(int(page))     # displays all patient for that page    
        selected = display.selected()                       # select the selected patients
        if len(patients['Patients']) > 0:
            # opening the page
            return render_template('home.htm', patients=patients['Patients'], num=num, selected=selected)
        else:
            return redirect(url_for('new_home', page = page - 1))
    else:
        alert = None
        if request.args.get('alert'):
            alert = 'alert'

        num = display.num_selected                          # displays total selected patient
        patients = display.show_all_patients(int(page))     # displays all patient for that page
        selected = display.selected()                       # select the selected patients
        # opening the page
        return render_template('home.htm', patients=patients['Patients'], num=num, alert = alert, selected=selected)

'''
shows the page for monitoring patients
'''
@app.route('/monitor_manager', methods=['GET', 'POST'])
def create_monitor_manager():
    global display
    global monitor_manager
    global cholesterol
    global blood_pressure

    if request.method == 'POST':
        data = json.loads(request.form['json'])             # retrieve data from request

        frequency = data['Frequency']                       # frequency of refresh
        systolic = data['Systolic']                         # systolic value
        diastolic = data['Diastolic']                       # diastolic value
        cholesterol = data['Cholesterol']                   # whether cholesterol values should be shown
        blood_pressure = data['Blood_Pressure']             # whether blood pressure values should be shown

        if monitor_manager == None:
            # add selected patient, if it does not exist
            display.selected_patients(data['Selected'])
            # command to remove any existing selected patient
            display.removed_patients(data['Removed'])

            # monitor manager is created
            monitor_manager = display.create_monitor_manager(frequency, systolic, diastolic)
            # getting data for creating monitor
            patients = monitor_manager.create_monitor()

            # opening the page
            return render_template('monitor_manager.htm', patients=patients['Patients'], frequency=frequency, cholesterol=cholesterol, blood_pressure=blood_pressure, systolic=systolic, diastolic=diastolic)
        else:
            show = None                                         # initialising variable
            # checks whether relevant data is sent
            if data['Removed'] != '':
                patient = json.loads(data['Removed'])
                patients = monitor_manager.remove_patient(patient['ID'], patient['Name'])
            elif data['Search'] != '':
                # returns whether the searched patient is found
                show = monitor_manager.search(data['Search'])

            monitor_manager.frequency = frequency               # frequency of monitor manager is updated
            monitor_manager.systolic = systolic                 # systolic value of monitor manager is updated
            monitor_manager.diastolic = diastolic               # diastolic value of monitor manager is updated
            patients = monitor_manager.refresh()

            # checks whether search is done or not
            if show != 'no' and show != None:
                # opening the page
                return render_template('monitor_manager.htm', patients=patients['Patients'], frequency=frequency, cholesterol=cholesterol, blood_pressure=blood_pressure, systolic=monitor_manager.systolic, diastolic=monitor_manager.diastolic)
            else:
                # opening the page
                return render_template('monitor_manager.htm', patients=patients['Patients'], frequency=frequency, show=show, cholesterol=cholesterol, blood_pressure=blood_pressure, systolic=monitor_manager.systolic, diastolic=monitor_manager.diastolic)
    else:
        try:
            patients = monitor_manager.refresh()
            # opening the page
            return render_template('monitor_manager.htm', patients=patients['Patients'], frequency=monitor_manager.frequency, cholesterol=cholesterol, blood_pressure=blood_pressure, systolic=monitor_manager.systolic, diastolic=monitor_manager.diastolic)
        except AttributeError:
            return redirect(url_for('new_home', page = 0, alert = 'alert'))

'''
finding the full info of a patient
'''
@app.route('/results', methods=['GET', 'POST'])
def searchPatient():
    global monitor_manager
    global ml_vitals
    global ml_p_value
    global ml_score_vitals
    global ml_score_p_value

    if request.method == 'POST':
        level = 'na'
        ml_score = None
        data = json.loads(request.form['json'])
        patient = monitor_manager.show_patient(data['ID'])
        p_value = [patient['Race'], patient['Ethnicity'], patient['Gender'], patient['Age']]
        
        #getting predicted cholesterol data
        if data['ML']:
            if ml == None:
                ml_vitals = ML()
                ml_score_vitals = ml_vitals.model('vitals')
                level_vitals = ml_vitals.know(p_id=data['ID'])
                if level_vitals == None:
                    ml_p_value = ML()
                    ml_score_p_value = ml_p_value.model('p_value')
                    level_p_value = ml_p_value.know(value=p_value)
                    level = level_p_value
                    ml_score = ml_score_p_value
                else:
                    level = level_vitals
                    ml_score = ml_score_vitals
            else:
                level_vitals = ml_vitals.know(p_id=data['ID'])
                if level_vitals == None:
                    level_p_value = ml_p_value.know(value=p_value)
                    level = level_p_value
                    ml_score = ml_score_p_value
                else:
                    level = level_vitals
                    ml_score = ml_score_vitals

        return render_template('results.htm', patient=patient, level=level, score=ml_score)

'''
showing a table containing latest data of patients containing high systolic blood pressure
'''
@app.route('/table', methods=['GET', 'POST'])
def create_table():
    global table

    if request.method == 'POST':
        data = json.loads(request.form['json'])                 # retrieve data from request
        frequency = data['Frequency']                           # frequency of monitor manager is updated

        if table == None:
            p_ids = data['ID']                                  # list of patient ids
            p_names = data['Name']                              # list of patient names
            table = Table(p_ids, p_names, frequency)            # create table
        else:
            # updating frequency of both table and monitor_manager 
            table.frequency = frequency
            monitor_manager.frequency = frequency

        patients = table.create_table()
        return render_template('table.htm', patients=patients, frequency=frequency)
    else:
        patients = table.create_table()
        frequency = table.frequency
        return render_template('table.htm', patients=patients, frequency=frequency)

if __name__ == "__main__":
    app.run()