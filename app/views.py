from datetime import date, datetime
import time
from app.formulaires import InscriptionVacataire, NewAccount
from .app import db,app
from flask import render_template,url_for,redirect,request,send_from_directory
from .models import *
from hashlib import sha256
import csv
from flask_login import login_user, current_user, logout_user,login_required
import os


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
            for typeMat in db.session.query(Cours.id_cours, Cours.type_cours, Cours.nom_cours).filter(Cours.nom_cours == mat).group_by(Cours.nom_cours, Cours.type_cours).all():
                try:
                    db.session.add(Affectable(current_user.id_vacataire,typeMat[0],typeMat[1],date.today(),datetime.now().strftime("%H:%M:%S")))
                    db.session.commit()
                except Exception as e:
                    print(e)
                    print("Erreur d'insertion, le vacataire est déjà affectable a la matiere " + mat)
        return render_template('menu_vacataire.html')
    lstMatiereDispo = db.session.query(Cours.nom_cours).all()
    setMatiere = set()
    for item in lstMatiereDispo:
        setMatiere.add(item[0])
    return render_template('matiere.html', listeMatiere = setMatiere)

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
            db.session.add(Disponibilites(maxIdDispo()+1,current_user.id_vacataire,periodes[item][0],periodes[1],periodes[0], periodes[item][1], periodes[item][2], date.today(),datetime.now().strftime("%H:%M:%S")))
            db.session.commit()
        for item in jours_spe:
            db.session.add(Disponibilites(maxIdDispo()+1,current_user.id_vacataire,item[0],-1,-1, item[1], item[2],date.today(),datetime.now().strftime("%H:%M:%S")))
            db.session.commit()
    return render_template('disponibilites.html')

@app.route('/nouveau_vacataire/', methods= ['GET', 'POST'])
def new_vaca():
    form = InscriptionVacataire()
    if request.method == "POST":
        id = max_id_actuel()
        if form.validate_on_submit():
            vac = Vacataire('V' + id,'Spontanée','0',form.entreprise.data, form.nom_v.data ,form.prenom_v.data ,form.num_tel_v.data,form.ddn_v.data,form.mail_v.data,encode_mdp(form.mdp_v.data))
            db.session.add(vac)
            db.session.commit()
            return url_for('menu_admin')
        else:
            return render_template('nouveau_vacataire.html', form = form)
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
def check_doss(lstTri=['Trier les dossiers ↓','Nom','Prenom','Telephone','Status'],filtre=["Filtrer les dossiers ↓","Distribué","Complet","Incomplet","Validé"]):
    liste_vaca = Vacataire.query.all()
    text_place = "Veuillez sélectionner une méthode de tri..."
    if request.method == "POST":
        liste_vaca = Vacataire.query.all()
        if request.form['tri'] != "Trier les dossiers ↓" or request.form['filtre'] != "Filtrer les dossiers ↓":
            match(request.form['tri']):
                case 'Nom':
                    text_place = "Chercher un nom..."
                    if request.form['filtre'] != "Filtrer les dossiers ↓":
                        if request.form['search']!="":
                            liste_vaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(Vacataire.nomV.ilike("%"+request.form['search']+"%"),GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                        else:
                            liste_vaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                    else:
                        if request.form['search']!="":
                            liste_vaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(Vacataire.nomV.ilike("%"+request.form['search']+"%")).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                        else:
                            liste_vaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).order_by(Vacataire.nomV).all()
                    lstTri=['Nom','Prenom','Telephone','Status','Ne pas trier']
                    if request.form['filtre'] == "Ne pas trier" or request.form['filtre'] == "Ne pas filtrer":
                        filtre=["Filtrer les dossiers ↓","Distribué","Complet","Incomplet","Validé"]
                    elif request.form['filtre'] == 'Distribué':
                        filtre=["Distribué","Complet","Incomplet","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Complet':
                        filtre=["Complet","Distribué","Incomplet","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Incomplet':
                        filtre=["Incomplet","Complet","Distribué","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Validé':
                        filtre=["Validé","Incomplet","Complet","Distribué","Ne pas trier"]
                case 'Prenom':
                    textPlace="Chercher un prenom..."
                    if request.form['filtre'] != "Filtrer les dossiers ↓":
                        if request.form['search']!="":
                            liste_vaca = db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(Vacataire.prenom_v.ilike("%"+request.form['search']+"%"),GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).all()
                        else:
                            liste_vaca = db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).all()
                    else:
                        if request.form['search']!="":
                            liste_vaca = db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(Vacataire.prenom_v.ilike("%"+request.form['search']+"%")).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).all()
                        else:
                            liste_vaca = db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).order_by(Vacataire.prenom_v).all()
                    lstTri=['Prenom','Nom','Telephone','Status','Ne pas trier']
                    if request.form['filtre'] == "Ne pas trier" or request.form['filtre'] == "Ne pas filtrer":
                        filtre=["Filtrer les dossiers ↓","Distribué","Complet","Incomplet","Validé"]
                    elif request.form['filtre'] == 'Distribué':
                        filtre=["Distribué","Complet","Incomplet","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Complet':
                        filtre=["Complet","Distribué","Incomplet","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Incomplet':
                        filtre=["Incomplet","Complet","Distribué","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Validé':
                        filtre=["Validé","Incomplet","Complet","Distribué","Ne pas trier"]
                case 'Telephone':
                    text_place = "Chercher un numéro de téléphone..."
                    if request.form['filtre'] != "Filtrer les dossiers ↓":
                        if request.form['search']!="":
                            liste_vaca = db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(Vacataire.num_tel_v.ilike("%"+request.form['search']+"%"),GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).all()
                        else:
                            liste_vaca = db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).all()
                    else:
                        if request.form['search']!="":
                            liste_vaca = db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(Vacataire.num_tel_v.ilike("%"+request.form['search']+"%")).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).all()
                        else:
                            liste_vaca = db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).order_by(Vacataire.numTelV).all()
                    lstTri=['Telephone','Prenom','Nom','Status','Ne pas trier']
                    if request.form['filtre'] == "Ne pas trier" or request.form['filtre'] == "Ne pas filtrer":
                        filtre=["Filtrer les dossiers ↓","Distribué","Complet","Incomplet","Validé"]
                    elif request.form['filtre'] == 'Distribué':
                        filtre=["Distribué","Complet","Incomplet","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Complet':
                        filtre=["Complet","Distribué","Incomplet","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Incomplet':
                        filtre=["Incomplet","Complet","Distribué","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Validé':
                        filtre=["Validé","Incomplet","Complet","Distribué","Ne pas trier"]
                case 'Status':
                    textPlace="Chercher un status de dossier..."
                    if request.form['filtre'] != "Filtrer les dossiers ↓":
                        if request.form['search']!="":
                            liste_vaca = db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(GererDossier.etat_dossier.ilike("%"+request.form['search']+"%"),GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).all()
                        else:
                            liste_vaca = db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).all()
                    else:
                        if request.form['search']!="":
                            liste_vaca = db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(GererDossier.etat_dossier.ilike("%"+request.form['search']+"%")).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                        else:
                            liste_vaca = db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).order_by(GererDossier.etat_dossier).all()
                    lstTri=['Status','Telephone','Prenom','Nom','Ne pas trier']
                    if request.form['filtre'] == "Ne pas trier" or request.form['filtre'] == "Ne pas filtrer":
                        filtre=["Filtrer les dossiers ↓","Distribué","Complet","Incomplet","Validé"]
                    elif request.form['filtre'] == 'Distribué':
                        filtre=["Distribué","Complet","Incomplet","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Complet':
                        filtre=["Complet","Distribué","Incomplet","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Incomplet':
                        filtre=["Incomplet","Complet","Distribué","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Validé':
                        filtre=["Validé","Incomplet","Complet","Distribué","Ne pas trier"]
                case 'Trier les dossiers ↓':
                    liste_vaca = db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).all()
                    if request.form['filtre'] == "Ne pas trier" or request.form['filtre'] == "Ne pas filtrer":
                        filtre=["Filtrer les dossiers ↓","Distribué","Complet","Incomplet","Validé"]
                    elif request.form['filtre'] == 'Distribué':
                        filtre=["Distribué","Complet","Incomplet","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Complet':
                        filtre=["Complet","Distribué","Incomplet","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Incomplet':
                        filtre=["Incomplet","Complet","Distribué","Validé","Ne pas trier"]
                    elif request.form['filtre'] == 'Validé':
                        filtre=["Validé","Incomplet","Complet","Distribué","Ne pas trier"]
    return render_template('recherche-dossiers.html',vaca=liste_vaca,tri=lstTri,filtre=filtre,placeHold=text_place)                    

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

@app.route('/dossier_vacataire/',)
@login_required
def edit_dossier():
    etat_dossier_user = db.session.query(GererDossier.etat_dossier).filter(current_user.id_vacataire==GererDossier.id_vacataire).join(Vacataire,Vacataire.id_vacataire==GererDossier.id_vacataire).first()
    date_fr_modif = db.session.query(GererDossier.date_modif,GererDossier.heure_modif).filter(current_user.id_vacataire==GererDossier.id_vacataire).join(Vacataire,Vacataire.id_vacataire==GererDossier.id_vacataire).first()
    return render_template('dossier_vacataire.html',etat_doc=etat_dossier_user,date_modif=date_fr_modif)

@app.route('/menu_vacataire/')
@login_required
def menu_vacataire():
    return render_template('menu_vacataire.html',nom_prenom=current_user.prenom_v + " " + current_user.nom_v)

@app.route("/logout/")
def logout():
    logout_user()
    #on attends d'abord que l'utilisateur soit bien déconnecté avant de redirect
    while True:
        if not current_user.is_authenticated:
            break
    return redirect(url_for('home'))
    
@app.route('/login/', methods= ['GET', 'POST'])
def log():
    if request.method == "POST":
        if est_vacataire(request.form['idUser']):
            try:
                log = Vacataire.query.filter_by(id_vacataire=request.form['idUser']).first()
                if encode_mdp(request.form['password']) == log.mdp_v:
                    login_user(log)
                    return redirect(url_for('menu_vacataire'))
            except:
                return render_template('login.html')
        else:
            try:
                adm = PersonnelAdministratif.query.filter_by(id_pers_admin=request.form['idUser']).first()
                if encode_mdp(request.form['password']) == adm.mdp_pa:
                    login_user(adm)
                    return redirect(url_for('menu_admin'))
            except:
                return render_template('login.html')
    return render_template('login.html')

@app.route('/EDT/')
@login_required
def load_edt():
    return render_template("EDT.html",nom_prenom = current_user.prenom_v + " " + current_user.nom_v)

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


def maxIdActu():
    IDMAX = 0
    VMax = db.session.query(Vacataire.IDVacataire).all()
    for id in VMax:
        if IDMAX<int(id[0][1:]):
            IDMAX = int(id[0][1:])
    PAMax = db.session.query(PersonnelAdministratif.IDpersAdmin).all()
    for id in PAMax:
        if IDMAX<int(id[0][1:]):
            IDMAX = int(id[0][1:])
    return str(IDMAX+1)

def maxIdDispo():
    x = db.session.query(Disponibilites.id_dispo).all()
    if x == None:
        return 0
    return len(x)


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
    app.run()
