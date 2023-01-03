function check_ddn(ddn,input){
    console.log(input)
    console.log(ddn);
    document.getElementById("submitter").disabled=true;
    const date = new Date();
    let age = 0;
    let annee = date.getFullYear();
    let mois = date.getMonth();
    let ddn_year = "";
    let ddn_month = "";
    for(i=0;i<7;i++){
        if (i<4){
        ddn_year += ddn[i];
        }
        if (i>4){
            ddn_month += ddn[i];
        }
    }
    ddn_month = parseInt(ddn_month);
    if (ddn_month>=mois){ddn_month=0;} //on ne considère pas le jour ici (on laisse une certaine marge)
    else{ddn_month=-1;} 
    ddn_year = parseInt(ddn_year);
    age = (annee-ddn_year)+ddn_month;
    if (age >= 18){
        document.getElementById("submitter").disabled=false;
        
    }
    else{alert("vous devez avoir plus de 18 ans");}    
}