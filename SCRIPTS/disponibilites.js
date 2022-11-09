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

    ul.innerHTML = `<li><select name="jour_semaine"><option value="">-- Jour de la semaine --</option><option value="lundi">Lundi</option><option value="mardi">Mardi</option><option value="mercredi">Mercredi</option><option value="jeudi">Jeudi</option><option value="vendredi">Vendredi</option><option value="samedi">Samedi</option></select></li><li>de</li><li><select name="heure_debut"><option value="">-- Heure de début --</option><option value="8">8h</option><option value="9">9h</option><option value="10">10h</option><option value="11">11h</option><option value="12">12h</option><option value="13">13h</option><option value="14">14h</option><option value="15">15h</option><option value="16">16h</option><option value="17">17h</option><option value="18">18h</option></select></li><li>à</li><li><select name="heure_fin"><option value="">-- Heure de fin --</option><option value="8">8h</option><option value="9">9h</option><option value="10">10h</option><option value="11">11h</option><option value="12">12h</option><option value="13">13h</option><option value="14">14h</option><option value="15">15h</option><option value="16">16h</option><option value="17">17h</option><option value="18">18h</option></select></li><li><button id="BP${parseInt(idBoutonDernierUL.slice(-1))+1}" onclick="supprimerDispo('BP${parseInt(idBoutonDernierUL.slice(-1))+1}')">Supprimer</button></li>`
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

    ul.innerHTML = `<li><input type="date"></li><li>de</li><li><select name="heure_debut"><option value="">-- Heure de début --</option><option value="8">8h</option><option value="9">9h</option><option value="10">10h</option><option value="11">11h</option><option value="12">12h</option><option value="13">13h</option><option value="14">14h</option><option value="15">15h</option><option value="16">16h</option><option value="17">17h</option><option value="18">18h</option></select></li><li>à</li><li><select name="heure_fin"><option value="">-- Heure de fin --</option><option value="8">8h</option><option value="9">9h</option><option value="10">10h</option><option value="11">11h</option><option value="12">12h</option><option value="13">13h</option><option value="14">14h</option><option value="15">15h</option><option value="16">16h</option><option value="17">17h</option><option value="18">18h</option></select></li><li><button id="BD${parseInt(idBoutonDernierUL.slice(-1))+1}" onclick="supprimerDispo('BD${parseInt(idBoutonDernierUL.slice(-1))+1}')">Supprimer</button></li>`
    datesSpe.appendChild(ul);
}

function verifier_valeur() {
    const periodes = document.getElementById("periodes");
    const dates_spe = document.getElementById("dates_spe");
    let verif = false
    for (let i = 0; i < periodes.children.length; i++) {
        const ul = periodes.children[i];
        for (let j = 0; j < ul.children.length; j++) {
            const li = ul.children[j];
            if (li.children.length>0){
                for (let k = 0; k < li.children.length; k++) {
                    const select = li.children[k]; 
                    if (select.tagName == "SELECT") {
                        if (select.value == "") {
                            verif = true;
                            select.style.backgroundColor = "red";
                        } else {
                            select.style.backgroundColor = "white";
                        }
                    }
                }
            }
        }
    }
    for (let i = 0; i < dates_spe.children.length; i++) {
        const ul = dates_spe.children[i];
        for (let j = 0; j < ul.children.length; j++) {
            const li = ul.children[j];
            if (li.children.length>0){
                for (let k = 0; k < li.children.length; k++) {
                    const select = li.children[k]; 
                    if (select.tagName == "SELECT" || select.tagName == "INPUT") {
                        if (select.value == "") {
                            verif = true;
                            select.style.backgroundColor = "red";
                        } else {
                            select.style.backgroundColor = "white";
                        }
                    }
                }
            }
        }
    }
    if (verif) {
        alert("Veuillez remplir tous les champs");
    }
}