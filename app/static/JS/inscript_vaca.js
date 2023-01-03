function colorButton() {
  if (!verifPageInput("infosPrincipales")) {
    console.log(verifPageInput("infosPrincipales"));
    $("input[value='Informations principales']").css("color", "red");
    console.log("aled");
  } else {
    $("input[value='Informations principales']").css("color", "lightgreen");
  }
  if (!verifPageInput("dispos")) {
    $("input[value='Renseigner les disponibilités']").css(
      "color",
      "red"
    );
  } else {
    $("input[value='Renseigner les disponibilités']").css("color", "lightgreen");
  }
}

$("body").on("change", function () {
  verifEnd = true;
  if (verifEnd) {
    verifEnd = verifPageInput("infosPrincipales");
  }
  if (verifEnd) {
    verifEnd = verifPageInput("dispos");
  }
  if (verif) {
    $("#submit").css("display", "flex");
  } else {
    $("#submit").css("display", "none");
  }
  colorButton();
});

function setDispo() {
  $("#button1").attr("value", "Informations principales");
  $("#button1").attr("onClick", "setInfos()");
  $("#button2").attr("value", "Renseigner les matières");
  $("#button2").attr("onClick", "setMatiere()");
  $("article").css("display", "contents");
  $("#infosPrincipales").css("display", "none");
  $("#matieres").css("display", "none");
  colorButton();
}

function setInfos() {
  $("#button1").attr("value", "Renseigner les disponibilités");
  $("#button1").attr("onClick", "setDispo()");
  $("#button2").attr("value", "Renseigner les matières");
  $("#button2").attr("onClick", "setMatiere()");
  $("article").css("display", "contents");
  $("#dispos").css("display", "none");
  $("#matieres").css("display", "none");
  colorButton();
}

function setMatiere() {
  $("#button1").attr("value", "Renseigner les disponibilités");
  $("#button1").attr("onClick", "setDispo()");
  $("#button2").attr("value", "Informations principales");
  $("#button2").attr("onClick", "setInfos()");
  $("article").css("display", "contents");
  $("#dispos").css("display", "none");
  $("#infosPrincipales").css("display", "none");
  colorButton();
}

function verifPageInput(idPage) {
  verif = true;
  let lst = $("#" + idPage + " input");
  for (i = 0; i < lst.length; i++) {
    if (lst.get(i).type != "submit") {
      if (lst.get(i).value == "") {
        verif = false;
      }
    }
  }
  return verif;
}

function supprimerDispo() {
    window.confirm("Êtes-vous sûr ?");
}

function ajouterDispoPeriode() {
    const periodes = document.getElementById("periodes");
    const ul = document.createElement("ul");

    ul.innerHTML = "<li><select name=\"jour_semaine\"><option value=\"\">Jour de la semaine</option><option value=\"lundi\">Lundi</option><option value=\"mardi\">Mardi</option><option value=\"mercredi\">Mercredi</option><option value=\"jeudi\">Jeudi</option><option value=\"vendredi\">Vendredi</option><option value=\"samedi\">Samedi</option></select></li><li>de</li><li><select name=\"heure_debut\"><option value=\"\">Heure de début</option><option value=\"8\">8h</option><option value=\"9\">9h</option><option value=\"10\">10h</option><option value=\"11\">11h</option><option value=\"12\">12h</option><option value=\"13\">13h</option><option value=\"14\">14h</option><option value=\"15\">15h</option><option value=\"16\">16h</option><option value=\"17\">17h</option><option value=\"18\">18h</option></select></li><li>à</li><li><select name=\"heure_fin\"><option value=\"\">Heure de fin</option><option value=\"8\">8h</option><option value=\"9\">9h</option><option value=\"10\">10h</option><option value=\"11\">11h</option><option value=\"12\">12h</option><option value=\"13\">13h</option><option value=\"14\">14h</option><option value=\"15\">15h</option><option value=\"16\">16h</option><option value=\"17\">17h</option><option value=\"18\">18h</option></select></li><li><input type='button' value='supprimer' onclick=\"supprimerDispo()\"/></li>"
    periodes.appendChild(ul);
}

function ajouterDispoDate() {
    const datesSpe = document.getElementById("dates_spe");
    const ul = document.createElement("ul");

    ul.innerHTML = "<li><input type=\"date\"></li><li>de</li><li><select name=\"heure_debut\"><option value=\"\">Heure de début</option><option value=\"8\">8h</option><option value=\"9\">9h</option><option value=\"10\">10h</option><option value=\"11\">11h</option><option value=\"12\">12h</option><option value=\"13\">13h</option><option value=\"14\">14h</option><option value=\"15\">15h</option><option value=\"16\">16h</option><option value=\"17\">17h</option><option value=\"18\">18h</option></select></li><li>à</li><li><select name=\"heure_fin\"><option value=\"\">Heure de fin</option><option value=\"8\">8h</option><option value=\"9\">9h</option><option value=\"10\">10h</option><option value=\"11\">11h</option><option value=\"12\">12h</option><option value=\"13\">13h</option><option value=\"14\">14h</option><option value=\"15\">15h</option><option value=\"16\">16h</option><option value=\"17\">17h</option><option value=\"18\">18h</option></select></li><li><input type='button' value='supprimer' onclick=\"supprimerDispo()\"/></li>"
    datesSpe.appendChild(ul);
}

function verifier_valeur() {
    const periodes = document.getElementById("periodes");
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
    if (verif) {
        alert("Veuillez remplir tous les champs");
    }
}