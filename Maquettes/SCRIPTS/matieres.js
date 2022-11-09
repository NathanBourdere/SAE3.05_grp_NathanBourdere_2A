function supprimerMatiere(idBouton) {
  let div;
  let ulBouton;

  if (window.confirm("Êtes-vous sûr ?")) {
    div = document.getElementById("matieres");
  }
  for (let enfant of div.children) {
      if (enfant.children[enfant.children.length-1].children[0].id === idBouton) {
          ulBouton = enfant;
          break;
      }
  }
  ulBouton.remove();
}

function ajouterMatiere() { 
  const matieres = document.getElementById("matieres");
  const ul = document.createElement("ul");
  let idBoutonDernierUL;

  if (matieres.children.length > 0) {
      const dernierUL = matieres.children[matieres.children.length-1];
      const boutonDernierUL = dernierUL.children[dernierUL.children.length-1].children[0];
      idBoutonDernierUL = boutonDernierUL.id;
  }else {
      idBoutonDernierUL = "BP0";
  }

  ul.innerHTML = `<li><select name="listes_matieres"><option value="Maths">Maths</option><option value="Français">Français</option><option value="Anglais">Anglais</option><option value="Histoire">Histoire</option></select></li><li><button id="BP${parseInt(idBoutonDernierUL.slice(-1))+1}" onclick="supprimerMatiere('BP${parseInt(idBoutonDernierUL.slice(-1))+1}')">Supprimer</button></li>`
  matieres.appendChild(ul);
  
}
function verifier_valeur() {
  const matieres = document.getElementById("matieres");
  let verif = false
  for (let i = 0; i < matieres.children.length; i++) {
      const ul = matieres.children[i];
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