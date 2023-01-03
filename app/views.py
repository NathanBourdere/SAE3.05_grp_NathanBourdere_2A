from app.formulaires import InscriptionVacataire, NewAccount
from .app import db,app
from flask import render_template,url_for,redirect,request,send_from_directory
from .models import *
from hashlib import sha256
import csv
from flask_login import login_user, current_user, logout_user,login_required
# from flask_uploads import UploadSet,configure_uploads, IMAGES, patch_request_class
import os

# Initialisation des routes
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/matiere.html')
@login_required
def matiere():
    return render_template('matiere.html')

@app.route('/disponibilites.html')
@login_required
def disponibilites():
    return render_template('disponibilites.html')

@app.route('/nouveau_vacataire.html', methods= ['GET', 'POST'])
def new_vaca():
    form = InscriptionVacataire(csrf_enabled=False)
    if form.validate_on_submit():
        id = maxIdActu()
        vac = Vacataire('V' + id,'Spontanée', '0',form.entreprise.data, form.nom.data ,form.prenom.data ,form.tel.data,form.ddn.data,form.email.data,form.password.data)
        db.session.add(vac)
        db.session.commit()
        return url_for('menu_admin')
    else:
        return render_template('nouveau_vacataire.html', form = form)

@app.route('/EDT.html')
@login_required
def EDT():
    return render_template('EDT.html')

@app.route('/menu_admin.html')
@login_required
def menu_admin():
    return render_template('menu_admin.html',nom_prenom=current_user.prenomPa + " " + current_user.nomPa)

@app.route('/profile.html')
@login_required
def profile():
    if estVacataire(current_user):
        return render_template('profile.html',profile_nom=current_user.nomV, profile_prenom=current_user.prenomV, profile_email=current_user.mailV, profile_tel=current_user.numTelV)
    return render_template('profile.html',profile_nom=current_user.nomPa, profile_prenom=current_user.prenomPa, profile_email=current_user.mailPa, profile_tel=current_user.numTelPa)

@app.route('/recherche-dossiers.html',methods=['GET', 'POST'])
@login_required
def check_doss(lstTri=['Trier les dossiers ↓','Nom','Prenom','Telephone','Status'],filtre=["Filtrer les dossiers ↓","Distribué","Complet","Incomplet","Validé"]):
    listeVaca = Vacataire.query.all()
    textPlace="Veuillez sélectionner une méthode de tri..."
    if request.method == "POST":
        listeVaca = Vacataire.query.all()
        if request.form['tri'] != "Trier les dossiers ↓" or request.form['filtre'] != "Filtrer les dossiers ↓":
            match(request.form['tri']):
                case 'Nom':
                    textPlace="Chercher un nom..."
                    if request.form['filtre'] != "Filtrer les dossiers ↓":
                        if request.form['search']!="":
                            print("non1")
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(Vacataire.nomV.ilike("%"+request.form['search']+"%"),GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                        else:
                            print("%"+request.form['search']+"%")
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                    else:
                        if request.form['search']!="":
                            print("non2")
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(Vacataire.nomV.ilike("%"+request.form['search']+"%")).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                        else:
                            print('pkpas')
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).order_by(Vacataire.nomV).all()
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
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(Vacataire.prenomV.ilike("%"+request.form['search']+"%"),GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                        else:
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                    else:
                        if request.form['search']!="":
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(Vacataire.prenomV.ilike("%"+request.form['search']+"%")).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                        else:
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).order_by(Vacataire.prenomV).all()
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
                    textPlace="Chercher un numéro de téléphone..."
                    if request.form['filtre'] != "Filtrer les dossiers ↓":
                        if request.form['search']!="":
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(Vacataire.numTelV.ilike("%"+request.form['search']+"%"),GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                        else:
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                    else:
                        if request.form['search']!="":
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(Vacataire.numTelV.ilike("%"+request.form['search']+"%")).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                        else:
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).order_by(Vacataire.numTelV).all()
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
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(GererDossier.etat_dossier.ilike("%"+request.form['search']+"%"),GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                        else:
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                    else:
                        if request.form['search']!="":
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(GererDossier.etat_dossier.ilike("%"+request.form['search']+"%")).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
                        else:
                            listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).order_by(GererDossier.etat_dossier).all()
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
                    listeVaca = db.session.query(Vacataire.nomV,Vacataire.prenomV,Vacataire.numTelV,Vacataire.mailV,GererDossier.etat_dossier).filter(GererDossier.etat_dossier==request.form['filtre']).join(GererDossier,GererDossier.IDVacataire==Vacataire.IDVacataire).all()
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
    return render_template('recherche-dossiers.html',vaca=listeVaca,tri=lstTri,filtre=filtre,placeHold=textPlace)                    

@app.route('/recherche-cours.html', methods=['GET','POST'])
@login_required
def check_cours():
    filtre=['Filtrer les infos ↓','Nom','Prenom','Cours','Domaine','Date','Classe','Salle']
    plh="Selectionnez un filtre..."
    listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).all()
    if request.method == "POST":
        if request.form['infos'] != "Filtrer les infos ↓":
            match(request.form['infos']):
                case "Nom":
                    filtre=['Nom','Prenom','Cours','Domaine','Date','Classe','Salle','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).filter(Vacataire.nomV==request.form['search']).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Vacataire.nomV).all()
                    else:
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Vacataire.nomV).all()
                case "Prenom":
                    plh="Entrez un prénom..."
                    filtre=['Prenom','Nom','Cours','Domaine','Date','Classe','Salle','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).filter(Vacataire.prenomV==request.form['search']).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Vacataire.prenomV).all()
                    else:
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Vacataire.prenomV).all()
                case "Cours":
                    plh="Entrez un nom..."
                    filtre=['Cours','Domaine','Prenom','Nom','Date','Classe','Salle','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).filter(Cours.nomCours==request.form['search']).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Cours.nomCours).all()
                    else:
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Cours.nomCours).all()
                case "Domaine":
                    plh="Entrez un domaine..."
                    filtre=['Domaine','Cours','Prenom','Nom','Date','Classe','Salle','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).filter(Cours.TypeCours==request.form['search']).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Cours.TypeCours).all()
                    else:
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Cours.TypeCours).all()
                case "Date":
                    plh="Entrez une Date..."
                    filtre=['Date','Domaine','Cours','Prenom','Nom','Classe','Salle','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).filter(Assigner.dateCours==request.form['search']).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Assigner.dateCours).all()
                    else:
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Assigner.dateCours).all()
                case "Classe":
                    plh="Entrez une classe..."
                    filtre=['Classe','Domaine','Cours','Prenom','Nom','Date','Salle','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).filter(Assigner.classe==request.form['search']).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Assigner.classe).all()
                    else:
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Assigner.classe).all()
                case "Salle":
                    plh="Entrez une Salle..."
                    filtre=['Salle','Classe','Domaine','Cours','Prenom','Nom','Date','Ne pas filtrer']
                    if request.form['search']!="":
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).filter(Assigner.classe==request.form['search']).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Assigner.salle).all()
                    else:
                        listeCours = db.session.query(Assigner.dateCours,Vacataire.IDVacataire,Vacataire.nomV,Vacataire.prenomV,Cours.nomCours,Cours.TypeCours,Cours.dureeCours,Assigner.HeureCours,Assigner.classe,Assigner.salle).join(Cours, Assigner.IDcours == Cours.IDcours).join(Vacataire, Assigner.IDVacataire == Vacataire.IDVacataire).order_by(Assigner.salle).all()
    return render_template('recherche-cours.html',cours=listeCours,filtre=filtre,placeHolder=plh)           

@app.route('/dossier_vacataire.html',)
@login_required
def editdoss():
    etat_dossier_user = db.session.query(GererDossier.etat_dossier).filter(current_user.IDVacataire==GererDossier.IDVacataire).join(Vacataire,Vacataire.IDVacataire==GererDossier.IDVacataire).first()
    date_fr_modif = db.session.query(GererDossier.dateModif,GererDossier.heureModif).filter(current_user.IDVacataire==GererDossier.IDVacataire).join(Vacataire,Vacataire.IDVacataire==GererDossier.IDVacataire).first()
    return render_template('dossier_vacataire.html',etat_doc=etat_dossier_user,date_modif=date_fr_modif)

@app.route('/menu_vacataire.html')
@login_required
def menu_vacataire():
    return render_template('menu_vacataire.html',nom_prenom=current_user.prenomV + " " + current_user.nomV)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('main'))
    
@app.route('/login.html', methods= ['GET', 'POST'])
def log():
    if request.method == "POST":
        if estVacataire(request.form['idUser']):
            try:
                log = Vacataire.query.filter_by(IDVacataire=request.form['idUser']).first()
                if request.form['password'] == log.mdpV:
                    login_user(log)
                    return menu_vacataire()
            except:
                return render_template('login.html')
        else:
            try:
                adm = PersonnelAdministratif.query.filter_by(IDpersAdmin=request.form['idUser']).first()
                if request.form['password'] == adm.mdpPa:
                    login_user(adm)
                    return menu_admin()
            except:
                return render_template('login.html')
    return render_template('login.html')

@app.route('/EDT.html')
@login_required
def load_edt():
    return render_template("EDT.html",current_user.prenomV + " " + current_user.nomV)

@login_manager.user_loader
def load_user(utilisateurID):
    if utilisateurID[0] == 'V':
        return Vacataire.query.filter_by(IDVacataire=utilisateurID).first()
    else:
        return PersonnelAdministratif.query.filter_by(IDpersAdmin=utilisateurID).first()

def estVacataire(user):
    if type(user) == str:
        if user[0] == 'V':
            return True
    else:
        if user.get_id()[0] == 'V':
            return True
    return False

def maxIdActu():
    idmax = 0
    VMax = db.session.query(Vacataire.IDVacataire).all()
    for id in VMax:
        if idmax<int(id[0][1:]):
            idmax = int(id[0][1:])
    PAMax = db.session.query(PersonnelAdministratif.IDpersAdmin).all()
    for id in PAMax:
        if idmax<int(id[0][1:]):
            idmax = int(id[0][1:])
    return str(idmax+1)

def test_connection():
    """
        Insère les valeurs des CSV courants dans /data dans la base de donnée
    """
    listeCsv = ['admin.csv','vacataire.csv','dossier.csv','cours.csv','affectable.csv','assigner.csv']
    for i in range(len(listeCsv)):
        with open("static/data/"+listeCsv[i]) as data:
            fileReader = csv.reader(data)
            match(i):
                case 0:
                    for ligne in fileReader:
                        db.session.add(PersonnelAdministratif(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6]))
                case 1:
                    for ligne in fileReader:
                        db.session.add(Vacataire(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6],ligne[7],ligne[8],ligne[9]))
                case 2:
                    for ligne in fileReader:
                        db.session.add(GererDossier(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4]))
                case 3:
                    for ligne in fileReader:
                        db.session.add(Cours(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5]))
                case 4:
                    for ligne in fileReader:
                        db.session.add(Affectable(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4]))
                case 5:
                    for ligne in fileReader:
                        db.session.add(Assigner(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6]))
            db.session.commit()

test_connection()

if __name__=="__main__":
    app.run()
