function supprimerDispo() {
    window.confirm("Êtes-vous sûr ?");
}

function ajouterDispoPeriode() {
    const periodes = document.getElementById("periodes");
    const article = document.createElement("article");

    article.innerHTML = "<ul><li><select name=\"jour_semaine\"><option value=\"\">Jour de la semaine</option><option value=\"lundi\">Lundi</option><option value=\"mardi\">Mardi</option><option value=\"mercredi\">Mercredi</option><option value=\"jeudi\">Jeudi</option><option value=\"vendredi\">Vendredi</option><option value=\"samedi\">Samedi</option></select></li><li>de</li><li><select name=\"heure_debut\"><option value=\"\">Heure de début</option><option value=\"8\">8h</option><option value=\"9\">9h</option><option value=\"10\">10h</option><option value=\"11\">11h</option><option value=\"12\">12h</option><option value=\"13\">13h</option><option value=\"14\">14h</option><option value=\"15\">15h</option><option value=\"16\">16h</option><option value=\"17\">17h</option><option value=\"18\">18h</option></select></li><li>à</li><li><select name=\"heure_fin\"><option value=\"\">Heure de fin</option><option value=\"8\">8h</option><option value=\"9\">9h</option><option value=\"10\">10h</option><option value=\"11\">11h</option><option value=\"12\">12h</option><option value=\"13\">13h</option><option value=\"14\">14h</option><option value=\"15\">15h</option><option value=\"16\">16h</option><option value=\"17\">17h</option><option value=\"18\">18h</option></select></li><li><button onclick=\"supprimerDispo()\">Supprimer</button></li></ul>"
    periodes.appendChild(article);    
}

function ajouterDispoDate() {
    window.alert("ajouter dispo date");
}