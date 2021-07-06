var patient_ids = [];

/*
deleting monitor
*/
function deleteMonitor(){
    let data = JSON.stringify({'Delete': 'yes'})

    submission('home', '', data)
}

/*
removing a patient from monitor
*/
function eradicate(id, name, surname){
    let frequency = document.getElementById('frequency').value;

    // getting body vitals value
    let vitals = body_vitals()
    cholesterol = vitals[0]
    blood_pressure = vitals[1]

    // getting pressure value
    let pressure = pressure_limit();
    systolic = pressure[0];
    diastolic = pressure[1];
    let removed = JSON.stringify({'ID': id, 'Name': name + ' ' + surname});
    let data = JSON.stringify({'Removed': removed, 'Frequency': frequency, 'Cholesterol': cholesterol, 'Blood_Pressure': blood_pressure, 'Systolic': systolic, 'Diastolic': diastolic});

    submission('monitor_manager', '', data);
}

/*
updating the page
*/
function update(){ 
    //storing data for communicating with the flask
    let frequency = document.getElementById('frequency').value;
    let vitals = body_vitals()
    cholesterol = vitals[0]
    blood_pressure = vitals[1]
    let pressure = pressure_limit();
    systolic = pressure[0];
    diastolic = pressure[1];

    if (cholesterol == 0 && blood_pressure == 0){
        window.alert('At least one body vitals need to be selected');
    }
    let data = JSON.stringify({'Removed': '', 'Search': '', 'Frequency': frequency, 'Cholesterol': cholesterol, 'Blood_Pressure': blood_pressure, 'Systolic': systolic, 'Diastolic': diastolic});
    
    submission('monitor_manager', '', data);
}

/*
printing the details of the patient
*/
function print(id){
    let data = JSON.stringify({'ID': id, 'ML': 0});
    
    submission('results', '', data);
}

/*
searching for a patient
*/
function search(){
    //storing data for communicating with the flask
    let search = document.getElementById('search').value;
    let frequency = document.getElementById('frequency').value;
    frequency = parseInt(frequency);
    if (isNaN(frequency)){
        window.alert('Frequency should be a number');
    }

    let vitals = body_vitals();
    cholesterol = vitals[0];
    blood_pressure = vitals[1];
    let pressure = pressure_limit();
    systolic = pressure[0];
    diastolic = pressure[1];
    let data = JSON.stringify({'Selected': '', 'Removed': '', 'Search': search, 'Frequency': frequency, 'Cholesterol': cholesterol, 'Blood_Pressure': blood_pressure, 'Systolic': systolic, 'Diastolic': diastolic});
    
    submission('monitor_manager', '', data)
}

/*
creating table for table page
*/
function table(){
    // judging validation of frequenct
    let frequency = document.getElementById('frequency').value;
    frequency = parseInt(frequency);
    if (isNaN(frequency)){
        window.alert('Frequency should be a number');
    }

    // getting pressure values
    let pressure = pressure_limit();
    let systolic = pressure[0];

    // getting required data
    let high = document.getElementById('high').innerHTML;
    let patients = JSON.parse(high);
    let patients_id = [];
    let patients_name = [];

    for(let i = 0; i < patients.length; i++){
        if (patients[i]['Systolic'] != 'unavailable' && patients[i]['Systolic'] >= systolic){
            patients_id.push(patients[i]['ID']);
            patients_name.push(patients[i]['Name']);
        }
    }

    let data = JSON.stringify({'ID': patients_id, 'Name': patients_name, 'Frequency': frequency});
    submission('table', '', data);
}

/*
getting body vitals checked values
*/
function body_vitals(){
    // check whether cholesterol button is checked
    let cholesterol = document.getElementById('cholesterol').checked;
    if (cholesterol){
        cholesterol = 1
    }
    else{
        cholesterol = 0
    }

    // check whether blood pressure button is checked
    let blood_pressure = document.getElementById('blood_pressure').checked;
    if (blood_pressure){
        blood_pressure = 1
    }
    else{
        blood_pressure = 0
    }

    return [cholesterol, blood_pressure]
}

/*
getting systolic and diastolic pressure values
*/
function pressure_limit(){
    // checking whether systolic pressure value is given
    let systolic = document.getElementById("systolic").value;
    systolic = parseInt(systolic);
    if (isNaN(systolic)){
        window.alert('Limit of Systolic Blood Pressure should be a number');
    }

    // checking whether diastolic pressure value is given
    let diastolic = document.getElementById("diastolic").value;
    diastolic = parseInt(diastolic);
    if (isNaN(diastolic)){
        window.alert('Limit of Systolic Blood Pressure should be a number');
    }

    return [systolic, diastolic]
}

/*
creating column chart using google charts
*/
function column_chart(patient_data, cholesterol){
    if(cholesterol == 1){
        // creating 2D array from json file
        let array = [['Patient Name', 'Cholesterol Value']];
        let patient = JSON.parse(patient_data);
        for(let i = 0; i < patient.length; i++){
            if(patient[i]['Chol_Value'] != 'unavailable'){
                array.push([patient[i]['Name'], patient[i]['Chol_Value']]);
            }
        }

        // getting data for proper visualisation
        let data = google.visualization.arrayToDataTable(array);
    
        // creating desired view
        let view = new google.visualization.DataView(data);
        view.setColumns([0, 1, {
            calc: "stringify",
            sourceColumn: 1,
            type: "string",
            role: "annotation" },
        ]);

        // defining options of the graph
        let options = {
            title: "Cholesterol Value of Patients",
            legend: { position: "none" },
            vAxis: { minValue: 0},
        };

        let chart = new google.visualization.ColumnChart(document.getElementById("chol_chart"));
        chart.draw(view, options);
    }
}