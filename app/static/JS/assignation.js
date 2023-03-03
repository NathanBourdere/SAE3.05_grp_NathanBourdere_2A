// Constantes pour les classes et les groupes
const nb_de_classes = 3;
const nb_de_groupes = 2;
const anneeMax = 3;
const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";



function getClassesEnFonctionCours(cours,jour,annee,ligne) {
    const liste = [];
    if (cours === "TP") {
        for (let annee = 1; annee <= anneeMax; annee++) {
            for (let classe = 1; classe <= nb_de_classes; classe++) {
                for (let groupe = 0; groupe < nb_de_groupes; groupe++) {
                    const nomDeClasse = `${annee}A${classe}${ALPHABET[groupe]}`;
                    liste.push(nomDeClasse);
                }
            }
        }
    } else if (cours === "TD") {
        for (let annee = 1; annee <= anneeMax; annee++) {
            for (let classe = 1; classe <= nb_de_classes; classe++) {
                const nomDeClasse = `${annee}A${classe}`;
                liste.push(nomDeClasse);
            }
        }
    } else if (cours === "CM") {
        for (let annee = 1; annee <= anneeMax; annee++) {
            const nomDeClasse = `${annee}A`;
            liste.push(nomDeClasse);
        }
    } else {
        throw new Error(`Mauvais type de cours: ${cours}`);
    }
    
    // Récupère la balise select qui a pour nom : jour-annee-Classe
    const select = document.getElementsByName(`${jour}-${annee}-Classe${ligne}`)[0];

    // Supprime toutes les options
    select.innerHTML = "";

    // Ajoute les options
    for (let i = 0; i < liste.length; i++) {
        const option = document.createElement("option");
        option.value = liste[i];
        option.innerHTML = liste[i];
        select.appendChild(option);
    }
}

function getClassesEnFonctionCoursPourDateSpe(cours,id_dispo,ligne) {
    const liste = [];
    if (cours === "TP") {
        for (let annee = 1; annee <= anneeMax; annee++) {
            for (let classe = 1; classe <= nb_de_classes; classe++) {
                for (let groupe = 0; groupe < nb_de_groupes; groupe++) {
                    const nomDeClasse = `${annee}A${classe}${ALPHABET[groupe]}`;
                    liste.push(nomDeClasse);
                }
            }
        }
    } else if (cours === "TD") {
        for (let annee = 1; annee <= anneeMax; annee++) {
            for (let classe = 1; classe <= nb_de_classes; classe++) {
                const nomDeClasse = `${annee}A${classe}`;
                liste.push(nomDeClasse);
            }
        }
    } else if (cours === "CM") {
        for (let annee = 1; annee <= anneeMax; annee++) {
            const nomDeClasse = `${annee}A`;
            liste.push(nomDeClasse);
        }
    } else {
        throw new Error(`Mauvais type de cours: ${cours}`);
    }
    
    const select = document.getElementsByName(`${id_dispo}-Classe${ligne}`)[0];

    // Supprime toutes les options
    select.innerHTML = "";

    // Ajoute les options
    for (let i = 0; i < liste.length; i++) {
        const option = document.createElement("option");
        option.value = liste[i];
        option.innerHTML = liste[i];
        select.appendChild(option);
    }
}


function ajouterLigneAssignation(periode,jour){
    // RÃ©cupÃ©ration du nom rÃ©duit du jour
    const jour2Lettres = jour.substring(0,2);

    // RÃ©cupÃ©ration des balises
    const tableJour = document.getElementById(`tableau-periode${periode}-${jour}`);

    // Compte le nombre de tr dans la table
    const nbLignes = tableJour.getElementsByTagName("tr").length;
    const numNewLigne = nbLignes + 1;

    // CrÃ©ation des Ã©lÃ©ments
    const newTR = document.createElement("tr");
    const newTD1 = document.createElement("td");
    const newTD2 = document.createElement("td");
    const newTD3 = document.createElement("td");
    const newTD4 = document.createElement("td");

    // Ajout des informations dans les Ã©lÃ©ments
    newTD1.innerHTML = `<input type="select" name="${jour2Lettres}-${numNewLigne}-Debut">`;
    newTD2.innerHTML = `<input type="select" name="${jour2Lettres}-${numNewLigne}-Fin">`;
    newTD3.innerHTML = `<input type="select" name="${jour2Lettres}-${numNewLigne}-Cours">`;
    newTD4.innerHTML = `<input type="select" name="${jour2Lettres}-${numNewLigne}-Classe">`;

    // CrÃ©ation du bouton pour rajouter une ligne
    const newButton = document.createElement("button");
    newButton.innerHTML = "+";
    newButton.setAttribute("onclick", `ajouterLigneAssignation(${periode},"${jour}")`);

    // Ajout des Ã©lÃ©ments dans le tr
    newTR.appendChild(newTD1);
    newTR.appendChild(newTD2);
    newTR.appendChild(newTD3);
    newTR.appendChild(newTD4);
    newTR.appendChild(newButton);

    // Ajout du tr dans la table
    tableJour.appendChild(newTR);
}

function genererHeure(){
    const selects = document.getElementsByTagName('select');
    const listeSelects = [];
    // Pour chaque select, on regarde le nom, et si il ya "Debut" ou "Fin"
    for (let i = 0; i < selects.length; i++) {
        const select = selects[i];
        const nom = select.getAttribute("name");
        if (nom.includes("Debut") || nom.includes("Fin")) {
            listeSelects.push(select);
        }
    }

    // 2 par 2, on ajoute les heures possibles
    for (let i = 0; i < listeSelects.length; i+=2) {
        const selectDebut = listeSelects[i];
        const selectFin = listeSelects[i+1];
        const listeHeures = genererHeureEntreheure(selectDebut.value,selectFin.value);
        clearFirstChildSelectList(selectDebut);
        clearFirstChildSelectList(selectFin);
        for (let j = 0; j < listeHeures.length; j++) {
            const heure = listeHeures[j];
            const option = document.createElement("option");
            option.value = heure;
            option.innerHTML = heure;
            selectDebut.appendChild(option);
            selectFin.appendChild(option.cloneNode(true));
        }
    }
}

function genererHeureEntreheure(debut,fin){
    const listeHeures = [];
    const debutInt = parseInt(debut);
    const finInt = parseInt(fin);

    // On ajoute les heures entre debut et fin toutes les 30 minutes
    for (let i = debutInt; i <= finInt; i++) {
        const heure = i.toString();
        listeHeures.push(heure+"h");
        // Si on est a la derniere heure, on ne rajoute pas 30 minutes
        if (i !== finInt) {
            listeHeures.push(heure+"h30");
        }
    }
    return listeHeures;
}

function clearFirstChildSelectList(selectList) {
    // Supprime la première option de chaque select
    for (let i = 0; i < selectList.length; i++) {
        const select = selectList[i];
        select.removeChild(select.firstChild);
    }
}