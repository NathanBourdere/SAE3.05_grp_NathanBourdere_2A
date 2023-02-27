import ast
from datetime import date, datetime
import time
from .formulaires import *
from .app import db,app
from flask import render_template,url_for,redirect,request
from .models import *
import csv
from flask_login import login_user, current_user, logout_user,login_required

from .models import searchDossier


# Initialisation des routes
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/matieres/', methods=['GET','POST'])
@login_required
def matiere():
    if request.method == "POST":
        lstMat = set()
        loop = True
        i = 0
        while(loop):
            try:
                lstMat.add(request.form['listes_matieres'+str(i)])
                i+=1
            except Exception as e:
                loop = False
        for mat in lstMat:
            (lstMat)
            for typeMat in db.session.query(Cours.id_cours, Cours.type_cours, Cours.nom_cours).filter(Cours.nom_cours.ilike(mat+"%")).group_by(Cours.nom_cours, Cours.type_cours).all():
                try:
                    db.session.add(Affectable(current_user.id_vacataire,typeMat[0],typeMat[1],date.today(),datetime.now().strftime("%H:%M:%S")))
                    db.session.commit()
                except Exception:
                    ("Erreur d'insertion, le vacataire est déjà affectable a la matiere " + mat)
        return render_template('menu_vacataire.html')
    lstAllMatiere = db.session.query(Cours.nom_cours).all()
    lstMatiereDispo = db.session.query(Cours.nom_cours, Affectable.id_vacataire, Cours.id_cours).filter(Affectable.id_vacataire == current_user.id_vacataire, Affectable.id_cours == Cours.id_cours).all()
    Affectable.query.filter_by(id_vacataire=current_user.id_vacataire).delete()
    db.session.commit()
    liste_final = []
    liste_intermediaire = []

    for matiere_attitrees in lstMatiereDispo:
        liste_intermediaire.append(matiere_attitrees)
        for matieres_restantes in lstAllMatiere:
            liste_intermediaire.append(matieres_restantes)
        liste_final.append(anti_doublons(liste_intermediaire))
        liste_intermediaire = []
    if liste_final == []:
        for matiere in lstAllMatiere:
            liste_intermediaire.append(matiere)
        liste_final.append(anti_doublons(liste_intermediaire))
    matiere_verif = []
    for item in liste_final:
        if item[0][0] not in matiere_verif:
            matiere_verif.append(item[0][0])
        else:
            liste_final.remove(item)
    dossierquery = get_dossier(current_user.id_vacataire)
    actualiser_date_dossier(dossierquery)
    return render_template('matiere.html', listeMatiere = liste_final, dateModif = dossierquery.date_modif, heuremodif = dossierquery.heure_modif)

@app.route('/disponibilites/', methods=['GET','POST'])
@login_required
def disponibilites():
    if request.method == "POST":
        periodes = [request.form["periode"], request.form["annee"]]
        jours_spe = []
        loop = True
        i = 0
        while(loop):
            try:
                periodes.append([request.form['jours_semaine'+str(i)], request.form["heure_debut_periode"+str(i)], request.form["heure_fin_periode"+str(i)]])
                i+=1
            except Exception as e:
                i=0
                while(loop):
                    try:
                        jour_particulier = []
                        jour_particulier.append(request.form["date_spe"+str(i)])
                        jour_particulier.append(request.form["heure_debut_date_spe"+str(i)])
                        jour_particulier.append(request.form["heure_fin_date_spe"+str(i)])
                        jours_spe.append(jour_particulier)
                        i+=1
                    except Exception as a:
                        loop = False
        for item in range(2,len(periodes)):
            db.session.add(Disponibilites(max_id_dispo()+1,current_user.id_vacataire,periodes[item][0],periodes[1],periodes[0], periodes[item][1], periodes[item][2], date.today(),datetime.now().strftime("%H:%M:%S")))
            db.session.commit()
        for item in jours_spe:
            db.session.add(Disponibilites(max_id_dispo()+1,current_user.id_vacataire,item[0],-1,-1, item[1], item[2],date.today(),datetime.now().strftime("%H:%M:%S")))
            db.session.commit()
    return render_template('disponibilites.html')

@app.route('/nouveau_vacataire/', methods= ['GET', 'POST'])
def new_vaca():
    form = InscriptionVacataire()
    if request.method == "POST":
        id = max_id_actuel()
        vac = Vacataire('V' + id,'Spontanée',form.entreprise.data,'0', form.nom.data ,form.prenom.data ,form.tel.data,form.ddn.data,form.email.data,encode_mdp(form.password.data),"","","","","")
        date_actuelle = date.today()
        heure_actuelle = datetime.now().strftime("%H:%M")
        dossier = GererDossier(vac.id_vacataire,current_user.id_pers_admin,"Distribué",date_actuelle,heure_actuelle)
        db.session.add(vac)
        db.session.add(dossier)
        db.session.commit()
        return redirect(url_for('menu_admin'))
    return render_template('nouveau_vacataire.html', form = form)


@app.route('/menu_admin/')
@login_required
def menu_admin():
    return render_template('menu_admin.html',nom_prenom=current_user.prenom_pa + " " + current_user.nom_pa)

@app.route('/profile/')
@login_required
def profile():
    if est_vacataire(current_user):
        return render_template('profile.html',profile_nom=current_user.nom_v, profile_prenom=current_user.prenom_v, profile_email=current_user.mail_v, profile_tel=current_user.num_tel_v)
    return render_template('profile.html',profile_nom=current_user.nom_pa, profile_prenom=current_user.prenom_pa, profile_email=current_user.mail_pa, profile_tel=current_user.num_tel_pa)

@app.route('/recherche-dossiers/',methods=['GET', 'POST'])
@login_required
def check_doss():
    def listeFiltre(firstVariable):
        if firstVariable == "Filtrer les dossiers ↓":
            return ["Filtrer les dossiers ↓","Distribué","Complet","Incomplet","Validé"]
        elif firstVariable == 'Distribué':
            return ["Distribué","Complet","Incomplet","Validé","Filtrer les dossiers ↓"]
        elif firstVariable == 'Complet':
            return ["Complet","Distribué","Incomplet","Validé","Filtrer les dossiers ↓"]
        elif firstVariable == 'Incomplet':
            return ["Incomplet","Complet","Distribué","Validé","Filtrer les dossiers ↓"]
        else:
            return ["Validé","Incomplet","Complet","Distribué","Filtrer les dossiers ↓"]
    
    def listeTri(firstVariable):
        if firstVariable == "Trier les dossiers ↓":
            return ['Trier les dossiers ↓','Nom','Prenom','Telephone','Status']
        elif firstVariable == 'Nom':
            return ['Nom','Prenom','Telephone','Status','Trier les dossiers ↓']
        elif firstVariable == 'Prenom':
            return ['Prenom','Nom','Telephone','Status','Trier les dossiers ↓']
        elif firstVariable == 'Telephone':
            return ['Telephone','Nom','Prenom','Status','Trier les dossiers ↓']
        else:
            return ['Status','Nom','Prenom','Telephone','Trier les dossiers ↓']
            
    liste_vaca = db.session.query(Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).all()
    text_place = "Veuillez sélectionner une méthode de tri..."
    if request.method == "POST":
        liste_de_tri = listeTri(request.form['tri'])
        liste_de_filtre = listeFiltre(request.form['filtre'])
        liste_vaca = searchDossier(request.form['tri'],request.form['filtre'],request.form['search'])
        return render_template('recherche-dossiers.html',vaca=liste_vaca,tri=liste_de_tri,filtre=liste_de_filtre,placeHold=text_place)
    return render_template('recherche-dossiers.html',vaca=liste_vaca,tri=['Trier les dossiers ↓','Nom','Prenom','Telephone','Status'],filtre=["Filtrer les dossiers ↓","Distribué","Complet","Incomplet","Validé"],placeHold=text_place)  

@app.route('/recherche-cours/', methods=['GET','POST'])
@login_required
def check_cours():
    filtre=['Filtrer les infos ↓','Nom','Prenom','Cours','Domaine','Date','Classe','Salle']
    plh="Selectionnez un filtre..."
    listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).all()
    if request.method == "POST":
        if request.form['infos'] != "Filtrer les infos ↓":
            match(request.form['infos']):
                case "Nom":
                    filtre=['Nom','Prenom','Cours','Domaine','Date','Classe','Salle','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).filter(Vacataire.nom_v==request.form['search']).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).order_by(Vacataire.nom_v).all()
                    else:
                        listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).order_by(Vacataire.nom_v).all()
                case "Prenom":
                    plh="Entrez un prénom..."
                    filtre=['Prenom','Nom','Cours','Domaine','Date','Classe','Salle','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).filter(Vacataire.prenom_v==request.form['search']).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).order_by(Vacataire.prenom_v).all()
                    else:
                        listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).order_by(Vacataire.prenom_v).all()
                case "Cours":
                    plh="Entrez un nom..."
                    filtre=['Cours','Domaine','Prenom','Nom','Date','Classe','Salle','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).filter(Cours.nom_cours==request.form['search']).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).order_by(Cours.nom_cours).all()
                    else:
                        listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).order_by(Cours.nom_cours).all()
                case "Domaine":
                    plh="Entrez un domaine..."
                    filtre=['Domaine','Cours','Prenom','Nom','Date','Classe','Salle','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).filter(Cours.type_cours==request.form['search']).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).order_by(Cours.type_cours).all()
                    else:
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Cours.TypeCours).all()
                case "Date":
                    plh="Entrez une Date..."
                    filtre=['Date','Domaine','Cours','Prenom','Nom','Classe','Salle','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).filter(Assigner.date_cours==request.form['search']).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).order_by(Assigner.date_cours).all()
                    else:
                        listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).order_by(Assigner.date_cours).all()
                case "Classe":
                    plh="Entrez une classe..."
                    filtre=['Classe','Domaine','Cours','Prenom','Nom','Date','Salle','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).filter(Assigner.classe==request.form['search']).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).order_by(Assigner.classe).all()
                    else:
                        listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).order_by(Assigner.classe).all()
                case "Salle":
                    plh="Entrez une Salle..."
                    filtre=['Salle','Classe','Domaine','Cours','Prenom','Nom','Date','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).filter(Assigner.classe==request.form['search']).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).order_by(Assigner.salle).all()
                    else:
                        listeCours = db.session.query(Assigner.date_cours,Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Cours.nom_cours,Cours.type_cours,Cours.duree_cours,Assigner.heure_cours,Assigner.classe,Assigner.salle).join(Cours, Assigner.id_cours == Cours.id_cours).join(Vacataire, Assigner.id_vacataire == Vacataire.id_vacataire).order_by(Assigner.salle).all()
    return render_template('recherche-cours.html',cours=listeCours,filtre=filtre,placeHolder=plh)           

@app.route('/dossier_vacataire/', methods=['GET', 'POST'])
@login_required
def edit_dossier():
    def ameliorer_format_date(date:str)->str:
        """Permet de mettre une date sous une meilleure forme.

        Args:
            date (str): Une date sous la forme AAAA-MM-JJ

        Returns:
            str: Une date sous la forme JJ/MM/AAAA
        """        
        res = ""
        annee = ""
        mois = ""
        jour = ""

        # Enlever les "-"
        for char in date:
            if char!="-":
                res+=char
        
        # Isoler l'année dans une variable
        for i in range(0,4):
            annee+=res[i]

        # Isoler le mois dans une variable
        for i in range(4,6):
            mois+=res[i]

        #Isoler le jour dans une variable
        for  i in range(6,8):
            jour+=res[i]

        # Reconstruire la date dans res
        res = jour + "/" + mois + "/" + annee

        return res
    
    vacataire = get_vacataire(current_user.id_vacataire)
    acc = InscriptionVacataire(vacataire)
    dossier = get_dossier(current_user.id_vacataire)
    date_modif_dossier = ameliorer_format_date(dossier.date_modif)
    return render_template("dossier_vacataire.html", form=acc, dossier=dossier, date_modif_dossier=date_modif_dossier)

    

@app.route('/menu_vacataire/')
@login_required
def menu_vacataire():
    return render_template('menu_vacataire.html',nom_prenom=current_user.prenom_v + " " + current_user.nom_v)

@app.route('/dossier/<id>/', methods=['GET', 'POST'])
@login_required
def voir_dossier_vacataire(id):
    if request.method == 'POST':
        dossier = get_dossier(id)
        dossier.etat_dossier = "Validé"
        db.session.commit()
        return redirect(url_for('voir_dossier_vacataire', id=id))

    vacataire = Vacataire.query.filter_by(id_vacataire=id).first()
    dossier = get_dossier(vacataire.id_vacataire)
    droit_changement_dossier = False
    if current_user.id_pers_admin == dossier.id_pers_admin:
        droit_changement_dossier = True
    return render_template('voir_dossier.html', info_vacataire=vacataire, date_modif=dossier.date_modif, heure_modif=dossier.heure_modif, etat=dossier.etat_dossier, admin_du_dossier=droit_changement_dossier)
    
@app.route("/logout/")
def logout():
    logout_user()
    #on attends d'abord que l'utilisateur soit bien déconnecté avant de redirect
    while True:
        if not current_user.is_authenticated:
            break
    return redirect(url_for('home'))
    
@app.route('/login/', methods= ['GET', 'POST'])
def login():
    acc = NewAccount()
    if not acc.is_submitted():
            acc.next.data = request.args.get("next")
    elif acc.validate_on_submit():
            user = get_authenticated_user(acc)
            try:
                if user and est_vacataire(user):
                    login_user(user)
                    next = acc.next.data or url_for('menu_vacataire')
                    return redirect(next)
                elif user and not est_vacataire(user):
                    login_user(user)
                    next = acc.next.data or url_for('menu_admin')
                    return redirect(next)
            except:
                return render_template('login.html',form = acc)
    return render_template('login.html',form = acc)

@app.route('/disponibilites/edit/', methods=["GET", "POST"])
@login_required
def load_edt():
    liste_periode = db.session.query(Disponibilites.semestre_dispo, Disponibilites.periode_dispo, Disponibilites.jour_dispo, Disponibilites.heure_dispo_debut, Disponibilites.heure_dispo_fin).filter(Disponibilites.periode_dispo != -1).all()
    liste_dates = db.session.query(Disponibilites.jour_dispo, Disponibilites.heure_dispo_debut, Disponibilites.heure_dispo_fin).filter(Disponibilites.periode_dispo == -1).all()
    if request.method == "POST":
        for periode in request.form.getlist('perio'):
            periode = ast.literal_eval(periode)
            Disponibilites.query.filter(Disponibilites.id_vacataire == current_user.id_vacataire, Disponibilites.semestre_dispo == periode[0], Disponibilites.periode_dispo == periode[1], Disponibilites.jour_dispo == periode[2], Disponibilites.heure_dispo_debut == periode[3], Disponibilites.heure_dispo_fin == periode[4]).delete()
        for date in request.form.getlist('dat'):
            date = ast.literal_eval(date)
            Disponibilites.query.filter(Disponibilites.id_vacataire == current_user.id_vacataire, Disponibilites.periode_dispo == -1, Disponibilites.jour_dispo == date[0], Disponibilites.heure_dispo_debut == date[1], Disponibilites.heure_dispo_fin == date[2])
        db.session.commit()
        liste_periode = db.session.query(Disponibilites.semestre_dispo, Disponibilites.periode_dispo, Disponibilites.jour_dispo, Disponibilites.heure_dispo_debut, Disponibilites.heure_dispo_fin).filter(Disponibilites.periode_dispo != -1).all()
        liste_dates = db.session.query(Disponibilites.jour_dispo, Disponibilites.heure_dispo_debut, Disponibilites.heure_dispo_fin).filter(Disponibilites.periode_dispo == -1).all()
    return render_template("EDT.html",liste_periodes = liste_periode, liste_dates = liste_dates)




@login_manager.user_loader
def load_user(utilisateur_id):
    if utilisateur_id[0] == 'V':
        return Vacataire.query.filter_by(id_vacataire=utilisateur_id).first()
    else:
        return PersonnelAdministratif.query.filter_by(id_pers_admin=utilisateur_id).first()

def est_vacataire(user):
    if type(user) == str:
        if user[0] == 'V':
            return True
    else:
        if user.get_id()[0] == 'V':
            return True
        
    return False

def max_id_actu():
    id_max = 0
    vacataires = db.session.query(Vacataire.id_vacataire).all()
    for id in vacataires:
        if id_max<int(id[0][1:]):
            id_max = int(id[0][1:])
    personnel_administratif = db.session.query(PersonnelAdministratif.id_pers_admin).all()
    for id in personnel_administratif:
        if id_max<int(id[0][1:]):
            id_max = int(id[0][1:])
    return str(id_max+1)

def max_id_dispo():
    x = db.session.query(Disponibilites.id_dispo).all()
    if x == None:
        return 0
    max = 0
    for val in x:
        if int(val[0])>max:
            max = int(val[0])
    return max

def encode_mdp(mdp:str)->str:
    """Permet d'encoder un mot de passe donné avec sha256.

    Args:
        mdp (str): Une chaine de caractères représentant un mot de passe.

    Returns:
        str: Une chaine de caractères représentant un mot de passe chiffré.
    """ 
    from hashlib import sha256
    m = sha256()
    m.update(mdp.encode())
    return m.hexdigest()

def anti_doublons(liste):
    res = []
    liste_matieres = []
    (liste)
    for item in liste:
        if item[0] not in liste_matieres:
            res.append(item)
            liste_matieres.append(item[0])
    return res

def test_connection():
    """
        Insère les valeurs des CSV courants dans /data dans la base de données
    """
    listeCsv = ['admin.csv','vacataire.csv','dossier.csv','cours.csv','affectable.csv','assigner.csv']
    for i in range(len(listeCsv)):
        with open("static/data/"+listeCsv[i]) as data:
            file_reader = csv.reader(data)
            match(i):
                case 0:
                    for ligne in file_reader:
                        db.session.add(PersonnelAdministratif(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6]))
                case 1:
                    for ligne in file_reader:
                        db.session.add(Vacataire(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6],ligne[7],ligne[8],ligne[9],ligne[10],ligne[11],ligne[12],ligne[13],ligne[14]))
                case 2:
                    for ligne in file_reader:
                        db.session.add(GererDossier(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4]))
                case 3:
                    for ligne in file_reader:
                        db.session.add(Cours(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5]))
                case 4:
                    for ligne in file_reader:
                        db.session.add(Affectable(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4]))
                case 5:
                    for ligne in file_reader:
                        db.session.add(Assigner(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6]))
            db.session.commit()

test_connection()

if __name__=="__main__":
    app.run(4095)
