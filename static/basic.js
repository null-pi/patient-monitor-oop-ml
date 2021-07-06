function submission(page_name, page, data){
    //remove any previous forms with id 'form'
    if (document.getElementById('form') != null){
        let form = document.getElementById('form');
        document.removeChild(form);
    }

    //creating form for postinf the communicated data
    let form = document.createElement("form");
    let input = document.createElement("input");

    //where to post the data
    form.method = 'POST';
    form.action = 'http://localhost:5000/' + page_name + String(page);
    form.style.display = 'none';
    form.id = 'form'

    //data is entered
    input.type = "text";
    input.name = "json";
    input.value = data;

    //data is passed 
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

function autoRefresh(frequency, page_name){
    setTimeout(function(){
        window.location.href = "http://localhost:5000/" + page_name;
    }, parseInt(frequency) * 1000);
}