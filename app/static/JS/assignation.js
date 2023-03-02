// Constantes pour les classes et les groupes
const nb_de_classes = 300;
const nb_de_groupes = 20;
const anneeMax = 300;
const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

// Constantes des pages HTML


function getClassesEnFonctionCours(cours) {
    const liste = [];
    if (cours === "TP") {
        for (let i = 1; i <= anneeMax; i++) {
            for (let j = 1; j <= nb_de_classes; j++) {
                for (let k = 0; k < nb_de_groupes; k++) {
                    const classe = `${i}A${j}${ALPHABET[k]}`;
                    liste.push(classe);
                }
            }
        }
    } else if (cours === "TD") {
        for (let i = 1; i <= anneeMax; i++) {
            for (let j = 1; j <= nb_de_classes; j++) {
                const classe = `${i}A${j}`;
                liste.push(classe);
            }
        }
    } else if (cours === "CM") {
        for (let i = 1; i <= anneeMax; i++) {
            const classe = `${i}A`;
            liste.push(classe);
        }
    }
    return liste;
}

