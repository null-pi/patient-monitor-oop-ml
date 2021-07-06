function ml(p_id){
    let data = JSON.stringify({'ID': p_id, 'ML': 'show'});

    submission('results', '', data);
}