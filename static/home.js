var selectedPatient = [];           //array of patients selected during a session
var removedPatient = [];            //array of patients removed during a session
var num_patients = 0;               //total number of patients

/*
showing next page
*/
function next(page_name, characters){
    let url = window.location.href; //getting current url address
    let char = url.slice(characters);       //getting current page number
    let page = '';
    
    //getting definite page number
    if (char){
        let i = 0;
        while (i < char.length){
            if (char[i] != '?'){
                page += char[i];
            }
            else{
                i = char.length
            }
            i += 1
        }
    }
    else{
        page = 0;                   //set page = 0 for completely new page
    }

    if (page){
        page = parseInt(page)
    }
    page++;                         //going to next page

    //create JSON file for communicating with flask
    let data = JSON.stringify({'Selected': selectedPatient, 'Removed': removedPatient});

    submission(page_name, page, data)
}

/*
show previous page
*/
function previous(page_name, characters){
    let url = window.location.href; //getting current url address
    let char = url.slice(characters);       //getting current page number
    let page = '';
    
    //finding specific page number
    if (char){
        let i = 0;
        while (i < char.length){
            if (char[i] != '?'){
                page += char[i];
            }
            else{
                i = char.length
            }
            i += 1
        }
        page = parseInt(page);  

        //dont go to previous pages, if first page is found
        if (page > 0){
            page--;

            //storing data for communicating with the flask
            let data = JSON.stringify({'Selected': selectedPatient, 'Removed': removedPatient});

            submission(page_name, page, data)
        }
    }
}

/*
toggling checkbox
*/
function toggle(id, name, surname){
    //getting checkbox and it's label by id
    let checkbox = document.getElementById(id);
    let label = document.getElementById(name);

    //toggle value and label, and add or remove patient
    if (checkbox.value == 'off'){
        add(id, name, surname);     //when toggle is turned on, add patient
        checkbox.value = 'on';
        label.innerHTML = 'Remove';
    }
    else{
        remove(id, name, surname);  //when toggle is turned off, remove patient
        checkbox.value = 'off';
        label.innerHTML = 'Add';
    }
}

/*
adding a patient to the selectedPatient
*/
function add(id, name, surname){
    //change the data to JSON
    data = JSON.stringify({'ID': id, 'Name': name + ' ' + surname})
    num_patients++;
    selectedPatient.push(data);
}

/*
adding patient to the removedPatient
*/
function remove(id, name, surname){
    //changing data to JSON
    data = JSON.stringify({'ID': id, 'Name': name + ' ' + surname})
    num_patients--;
    removedPatient.push(data);
}

/*
creating manager with the selected patient and definite frequency
*/
function create_manager(num){
    if (num + num_patients == 0){
        //if no patient is selected flag alert
        window.alert("At least one patient need to be selected");
    }
    else{
        //storing data for communicating with the flask
        let frequency = document.getElementById('frequency').value;
        frequency = parseInt(frequency);
        let cholesterol = document.getElementById('cholesterol').checked;
        if (cholesterol){
            cholesterol = 1
        }
        else{
            cholesterol = 0
        }
        let blood_pressure = document.getElementById('blood_pressure').checked;
        if (blood_pressure){
            blood_pressure = 1
        }
        else{
            blood_pressure = 0
        }

        let systolic = document.getElementById("systolic").value;
        systolic = parseInt(systolic);
        if (isNaN(systolic)){
            window.alert('Limit of Systolic Blood Pressure should be a number');
        }

        let diastolic = document.getElementById("diastolic").value;
        diastolic = parseInt(diastolic);
        if (isNaN(diastolic)){
            window.alert('Limit of Systolic Blood Pressure should be a number');
        }

        if (cholesterol == 0 && blood_pressure == 0){
            window.alert('At least one body vitals need to be selected');
        }
        else if (isNaN(frequency)){
            window.alert('Frequency should be a number');
        }
        else{
            let data = JSON.stringify({'Selected': selectedPatient, 'Removed': removedPatient, 'Frequency': frequency, 'Cholesterol': cholesterol, 'Blood_Pressure': blood_pressure, 'Systolic': systolic, 'Diastolic': diastolic});
            submission('monitor_manager', '', data)
        }
    }
}