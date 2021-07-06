function update(){
    //storing data for communicating with the flask
    let frequency = document.getElementById('frequency').value;
    frequency = parseInt(frequency);
    if (isNaN(frequency)){
        window.alert('Frequency should be a number');
    }
    else{
        let data = JSON.stringify({'Frequency': frequency});
    
        submission('table', '', data);
    }
}


// second update
//
//function insert_canvas(canvas_name, name, data){
//var ctx = document.getElementById(canvas_name).getContext('2d');
//var myChart = new Chart(ctx, {
//    type: 'line',
//    data: {
//        labels: [1,2,3,4,5],
//        datasets: [{
//            label: name,
//            data: data,
//        }]
//    },
//    options: {
//        scales: {
//            yAxes: [{
//                ticks: {
//                    beginAtZero: false
//                }
//            }]
//        }
//    }
//});
//}
function add_canvas(id,name,details){
const ctx = document.getElementById(id).getContext('2d');
        const chart = new Chart(ctx, {
        // The type of chart we want to create: Bar graph

        type: 'line',

        // The data for our dataset
        data: {
            labels: [1,2,3,4,5],
            datasets: [{
                label: name,
                borderColor: 'rgb(0, 99, 132)',
                hoverBackgroundColor:'purple',
                responsive: true,
                data: details
            }]
        },

        // Configuration options go here
        options: {
        fill : false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
        }
        });
}

function pressure_list(){
    var raw_data = $(".table").text();
    var raw_array = raw_data.split("\n");
    var filtered_array = raw_array.filter(el =>{return el.trim()});
    filtered_array = filtered_array.slice(16,);
    total_count = filtered_array.length / 11;
//    var name_list = ;

    for (i = 0; i < total_count; i++)
    {
//    0,7,14,21,28
        var details = [];
        var start = i * 11;
        var end = start + 11;
        var temp = filtered_array.slice(start, end);
        var name = temp[0].trimLeft();
        var pressure1 = temp[1].trimLeft();
//    console.log(pressure1);
        pressure1 = pressure1.slice(0,pressure1.length - 7)
        pressure1 = parseFloat(pressure1);
        details.push(pressure1);
    var pressure2 = temp[3].trimLeft();
    pressure2 = pressure2.slice(0,pressure2.length - 7)
    pressure2 = parseFloat(pressure2);
//    console.log(pressure2);
    details.push(pressure2);
    var pressure3 = temp[5].trimLeft();
    pressure3 = pressure3.slice(0,pressure3.length - 7)
    pressure3 = parseFloat(pressure3);
    details.push(pressure3);
    var pressure4 = temp[7].trimLeft();
    pressure4 = pressure4.slice(0,pressure4.length - 7)
    pressure4 = parseFloat(pressure4);
    details.push(pressure4);
    var pressure5 = temp[9].trimLeft();
    pressure5 = pressure5.slice(0,pressure5.length - 7)
    pressure5 = parseFloat(pressure5);
    details.push(pressure5);
//    details.push(pressure5);
    var tag = '<canvas id="'+ i +'" height="300" width="450"></canvas>';
    $("#myCanvas").append(tag);
    var id = i;
    add_canvas(id,name,details);

    }
}

window.addEventListener('load', function () {
  pressure_list();
})
