const lstMatiereGenesis = loadMat();

function loadMat() {
  let lstMatiere = [];
  let lstOptionOrigin = $('ul:last-child li option')
  for (i = 0; i < lstOptionOrigin.length; i++) {
    lstMatiere.push($('ul:last-child li option').eq(i).html());
  }
  return lstMatiere
}

function supprimerMatiere(idBouton) {
  let div;
  let ulBouton;

  if (window.confirm("Êtes-vous sûr ?")) {
    div = document.getElementById("matieres");
  }
  for (let enfant of div.children) {
    if (enfant.children[enfant.children.length - 1].children[0].id === "BP"+idBouton) {
      ulBouton = enfant;
      break;
    }
  }
  ulBouton.remove();
  console.log("oe")
}

function ajouterMatiere() {
  const matieres = document.getElementById("matieres");
  const ul = document.createElement("ul");
  let idBoutonDernierUL;
  console.log(matieres.children.length)
  if (matieres.children.length > 0) {
    const dernierUL = matieres.children[matieres.children.length - 1];
    console.log(dernierUL)
    const boutonDernierUL = dernierUL.children[dernierUL.children.length - 1].children[0];
    console.log(boutonDernierUL)
    idBoutonDernierUL = boutonDernierUL.id;
  } else {
    idBoutonDernierUL = "BP0";
  }
  strId = String(parseInt(idBoutonDernierUL.substring(2))+1)
  let newhtml = "<li><select name=listes_matieres"+strId+">"
  for (i=0;i<lstMatiereGenesis.length;i++) {
    newhtml += "<option value='`"+ lstMatiereGenesis[i] + "`'>" + lstMatiereGenesis[i] +" </option>"
  }
  newhtml += "</select></li><li><button id='BP" + strId + "' onclick='supprimerMatiere(" + strId +")'>Supprimer</button></li>"
  ul.innerHTML = newhtml
  matieres.appendChild(ul);
}