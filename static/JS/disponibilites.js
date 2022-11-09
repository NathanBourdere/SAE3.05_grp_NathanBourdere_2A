function supprimerDispo(idBouton) {
    let div;
    let ulBouton;

    if (window.confirm("Êtes-vous sûr ?")) {
        if (idBouton.slice(0,2) === "BP") {
            div = document.getElementById("periodes");
        }else{
            div = document.getElementById("dates_spe");
        }
    }
    for (let enfant of div.children) {
        if (enfant.children[enfant.children.length-1].children[0].id === idBouton) {
            ulBouton = enfant;
            break;
        }
    }
    ulBouton.remove();
}

function ajouterDispoPeriode() { 
    const periodes = document.getElementById("periodes");
    const ul = document.createElement("ul");
    let idBoutonDernierUL;

    if (periodes.children.length > 0) {
        const dernierUL = periodes.children[periodes.children.length-1];
        const boutonDernierUL = dernierUL.children[dernierUL.children.length-1].children[0];
        idBoutonDernierUL = boutonDernierUL.id;
    }else {
        idBoutonDernierUL = "BP0";
    }

    ul.innerHTML = `<li><select name="jour_semaine"><option value="">Jour de la semaine</option><option value="lundi">Lundi</option><option value="mardi">Mardi</option><option value="mercredi">Mercredi</option><option value="jeudi">Jeudi</option><option value="vendredi">Vendredi</option><option value="samedi">Samedi</option></select></li><li>de</li><li><select name="heure_debut"><option value="">Heure de début</option><option value="8">8h</option><option value="9">9h</option><option value="10">10h</option><option value="11">11h</option><option value="12">12h</option><option value="13">13h</option><option value="14">14h</option><option value="15">15h</option><option value="16">16h</option><option value="17">17h</option><option value="18">18h</option></select></li><li>à</li><li><select name="heure_fin"><option value="">Heure de fin</option><option value="8">8h</option><option value="9">9h</option><option value="10">10h</option><option value="11">11h</option><option value="12">12h</option><option value="13">13h</option><option value="14">14h</option><option value="15">15h</option><option value="16">16h</option><option value="17">17h</option><option value="18">18h</option></select></li><li><button id="BP${parseInt(idBoutonDernierUL.slice(-1))+1}" onclick="supprimerDispo('BP${parseInt(idBoutonDernierUL.slice(-1))+1}')">Supprimer</button></li>`
    periodes.appendChild(ul);
    
}

function ajouterDispoDate() {
    const datesSpe = document.getElementById("dates_spe");
    const ul = document.createElement("ul");
    let idBoutonDernierUL;

    if (datesSpe.children.length !== 0) {
        const dernierUL = datesSpe.children[datesSpe.children.length-1];
        const boutonDernierUL = dernierUL.children[dernierUL.children.length-1].children[0];
        idBoutonDernierUL = boutonDernierUL.id;
    }else{
        idBoutonDernierUL = "BD0";
    }

    ul.innerHTML = `<li><input type="date"></li><li>de</li><li><select name="heure_debut"><option value="">Heure de début</option><option value="8">8h</option><option value="9">9h</option><option value="10">10h</option><option value="11">11h</option><option value="12">12h</option><option value="13">13h</option><option value="14">14h</option><option value="15">15h</option><option value="16">16h</option><option value="17">17h</option><option value="18">18h</option></select></li><li>à</li><li><select name="heure_fin"><option value="">Heure de fin</option><option value="8">8h</option><option value="9">9h</option><option value="10">10h</option><option value="11">11h</option><option value="12">12h</option><option value="13">13h</option><option value="14">14h</option><option value="15">15h</option><option value="16">16h</option><option value="17">17h</option><option value="18">18h</option></select></li><li><button id="BD${parseInt(idBoutonDernierUL.slice(-1))+1}" onclick="supprimerDispo('BD${parseInt(idBoutonDernierUL.slice(-1))+1}')">Supprimer</button></li>`
    datesSpe.appendChild(ul);
}

function verifierDates(date) {
    // Renvoie true si les dates renseignées est bonne. False sinon.
    let res = true;
    const dateAujourdhui = new Date();

    if (dateAujourdhui.getFullYear()>date.getFullYear()) {
        res = false;
    }else if (dateAujourdhui.getFullYear() === date.getFullYear() && dateAujourdhui.getMonth()+1 > date.getMonth()+1) {
        res = false;
    }else if (dateAujourdhui.getMonth() === date.getMonth() && dateAujourdhui.getDate() > date.getDate()) {
        res = false;
    }
    return res;
}

function verifier_valeur() {
    const periodes = document.getElementById("periodes");
    const dates_spe = document.getElementById("dates_spe");
    let liste = [];
    let list = [];
    let verif = false;
    let erreur_donnees = false;
    let date_incorrect = false;
    for (let i = 0; i < periodes.children.length; i++) {
        const ul = periodes.children[i]; // récupère l'élément ul
        for (let j = 0; j < ul.children.length; j++) {
            const li = ul.children[j]; // récupère l'élément li dans l'élément ul
            if (li.children.length>0){
                for (let k = 0; k < li.children.length; k++) {
                    const balise = li.children[k];  // récupère l'élément dans l'élément li 
                    // on vérifie que l'élément est un select
                    if (balise.tagName == "SELECT") {
                        // on vérifie que l'élément n'est pas vide
                        if (balise.value == "") {
                            verif = true;
                            balise.style.backgroundColor = "#ff4d4d";
                        } else {
                            balise.style.backgroundColor = "white";
                            // sinon on vérifie que l'élément est une heure
                            if (balise.textContent.includes("h")) {
                                list.push(balise);
                            }
                        }
                    }
                }
            }
        }
        if (list.length == 2) {
            liste.push(list);
            list = [];
        }
    }

    for (let i = 0; i < dates_spe.children.length; i++) {
        const ul = dates_spe.children[i];
        for (let j = 0; j < ul.children.length; j++) {
            const li = ul.children[j];
            if (li.children.length>0){
                for (let k = 0; k < li.children.length; k++) {
                    const balise = li.children[k]; 
                    if (balise.tagName == "SELECT") {
                        if (balise.value == "") {
                            verif = true;
                            balise.style.backgroundColor = "#ff4d4d";
                        } else {
                            balise.style.backgroundColor = "white";
                            if (balise.textContent.includes("h")) {
                                list.push(balise);
                            }
                        }
                    } else if (balise.tagName == "INPUT") {
                        verifie_date = verifierDates(new Date(balise.value));
                        if (verifie_date == false) {
                            balise.style.backgroundColor = "#ff4d4d";
                            date_incorrect = true;
                        } else {
                            balise.style.backgroundColor = "white";
                        }
                    }
                }
            }
        }
        if (list.length == 2) {
            liste.push(list);
            list = [];
        }
    }
    for (let i = 0; i < liste.length; i++) {
        val1 = parseInt(liste[i][0].value);
        val2 = parseInt(liste[i][1].value);
        if (val1 >= val2) {
            erreur_donnees = true;
            liste[i][0].style.backgroundColor = "#c7c2ff";
            liste[i][1].style.backgroundColor = "#c7c2ff";
        }
    }


    if (verif) {
        alert("Veuillez remplir tous les champs");
    }
    if (erreur_donnees) {
        alert("Veuillez vérifier les données saisies");
    }
    if (date_incorrect) {
        alert("Veuillez vérifier les dates saisies(les dates doivent être supérieures à la date d'aujourd'hui)");
    }

}
