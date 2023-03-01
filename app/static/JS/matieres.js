function supprimerMatiere(idBouton) {
  let div;
  let ulBouton;

  if (idBouton == 'BP0') {
    alert('Vous ne pouvez pas supprimer votre première matière');
    event.preventDefault();
  }
  else {
    if (window.confirm("Êtes-vous sûr ?")) {
      div = document.getElementById("matieres");
    }
    for (let enfant of div.children) {
      if (enfant.children[enfant.children.length - 1].children[0].id === idBouton) {
        ulBouton = enfant;
        break;
      }
    }
    ulBouton.remove();
  }
}

function ajouterMatiere() {
  const matieres = document.getElementById("matieres");
  const ul = document.createElement("ul");
  let idBoutonDernierUL;

  if (matieres.children.length > 0) {
    const dernierUL = matieres.children[matieres.children.length - 1];
    const boutonDernierUL = dernierUL.children[dernierUL.children.length - 1].children[0];
    idBoutonDernierUL = boutonDernierUL.id;
  } else {
    idBoutonDernierUL = "BP0";
  }
  numberId = idBoutonDernierUL.substring(2);
  listeMatiere = document.getElementsByName("listes_matieres0");
  numberId = parseInt(numberId) + 1
  console.log(listeMatiere[0].innerHTML)
  let strin = `<li><select id ="pimpSelect" name="listes_matieres` + numberId + `"> `+ listeMatiere[0].innerHTML + `</select></li><li><button class="deleteButton" id="BP${parseInt(idBoutonDernierUL.slice(-1))+1}" onclick="supprimerMatiere('BP${parseInt(idBoutonDernierUL.slice(-1))+1}')">❌</button></li>`
  console.log(strin)
  ul.innerHTML = strin
  matieres.appendChild(ul);
}