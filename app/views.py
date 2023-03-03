import ast
from datetime import date, datetime as datetemps
import time
from .formulaires import *
from .app import db,app
from flask import flash, render_template,url_for,redirect,request
from .models import *
import csv
from flask_login import login_user, current_user, logout_user,login_required

from .models import searchDossier

# Initialisation des routes
@app.route('/')
def home():
    if current_user.is_authenticated:
        # si c'est un admin
        try:
            if current_user.id_pers_admin:
                return redirect(url_for('menu_admin'))
        # si c'est un vacataire
        except AttributeError:
            return redirect(url_for('menu_vacataire'))
    return render_template('main.html')

@app.route('/credits/')
def credits():
    return render_template('credits.html')
    
@app.route('/mesmatieres/', methods=['GET'])
def voir_matieres():        
    subquery = db.session.query(
        Cours.id_cours,
        Assigner.id_vacataire
    ).outerjoin(
        Assigner,
        Assigner.id_cours == Cours.id_cours
    ).filter(
        Assigner.id_vacataire == current_user.id_vacataire
    ).subquery()

    assignations = db.session.query(
        Domaine.id_domaine,
        Domaine.domaine,
        PersonnelAdministratif.nom_pa,
        PersonnelAdministratif.prenom_pa,
        subquery.c.id_cours
    ).outerjoin(
        PersonnelAdministratif, 
        PersonnelAdministratif.id_pers_admin == Domaine.responsable
    ).outerjoin(
        Cours, 
        Cours.domaine == Domaine.id_domaine
    ).outerjoin(
        subquery,
        subquery.c.id_cours == Cours.id_cours
    ).all()


    print(assignations)
    return render_template('matieres_assignees.html',domaine=assignations)

@app.route('/matieres/', methods=['GET','POST'])
@login_required
def matiere():
    if request.method == "POST":
        Affectable.query.filter_by(id_vacataire=current_user.id_vacataire).delete()
        db.session.commit()
        lstMat = set()
        loop = True
        tuple = 0
        while(loop):
            try:
                lstMat.add(request.form['listes_matieres'+str(tuple)])
                tuple+=1
            except Exception as e:
                loop = False
        for mat in lstMat:
            liste_matiere_jsp = db.session.query(Domaine.id_domaine, Domaine.domaine).filter(Domaine.domaine.ilike("%" + mat + "%")).all()
            for id_dom,dom in liste_matiere_jsp:
                try:
                    db.session.add(Affectable(current_user.id_vacataire,id_dom,date.today(),datetemps.now().strftime("%H:%M:%S")))
                    db.session.commit()
                except Exception as e:
                    print(e)
                    print("Erreur d'insertion, le vacataire est déjà affectable a la matiere " + mat)
    lstAllMatiere = db.session.query(Domaine.domaine).all()
    lstMatiereDispo = db.session.query(Domaine.domaine, Affectable.id_vacataire, Domaine.id_domaine).join(Affectable, Affectable.id_domaine == Domaine.id_domaine).all()
    liste_final = []
    for tuple in lstMatiereDispo:
        liste_temp = []
        liste_temp.append(tuple)
        for matieres in lstAllMatiere:
            liste_temp.append(matieres)
        liste_final.append(liste_temp)
    liste_rendu = []
    start = []
    for listes in liste_final:
        if listes[0][0] not in start:
            start.append(listes[0][0])
            liste_rendu.append(anti_doublons(listes))
    dossierquery = get_dossier(current_user.id_vacataire)
    return render_template('matiere.html', listeMatiere = liste_rendu, dateModif = dossierquery.date_modif, heuremodif = dossierquery.heure_modif)

@app.route('/assigner_vacataire/', methods=['GET','POST'])
@login_required
def select_vacataire():
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
            
    liste_vaca = db.session.query(Vacataire.id_vacataire,Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).filter(GererDossier.etat_dossier.ilike("%Valid%")).all()
    text_place = "Veuillez sélectionner une méthode de tri..."
    if request.method == "POST":
        liste_de_tri = listeTri(request.form['tri'])
        liste_vaca = searchDossier(request.form['tri'],"Filtrer les dossiers ↓",request.form['search'])
        return render_template('recherche-vacataire.html',vaca=liste_vaca,tri=liste_de_tri,placeHold=text_place)
    return render_template('recherche-vacataire.html',vaca=liste_vaca,tri=['Trier les dossiers ↓','Nom','Prenom','Telephone','Status'],placeHold=text_place)  


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
                if request.form['jours_semaine'+str(i)] != "":
                    periodes.append([request.form['jours_semaine'+str(i)], request.form["heure_debut_periode"+str(i)], request.form["heure_fin_periode"+str(i)]])
                i+=1
            except Exception as e:
                i=0
                while(loop):
                    try:
                        print(request.form)
                        if request.form['date_spe'+str(i)] != "":
                            jour_particulier = []
                            jour_particulier.append(request.form["date_spe"+str(i)])
                            jour_particulier.append(request.form["heure_debut_date_spe"+str(i)])
                            jour_particulier.append(request.form["heure_fin_date_spe"+str(i)])
                            jours_spe.append(jour_particulier)
                        i+=1
                    except Exception as a:
                        loop = False
        for item in range(2,len(periodes)):
            db.session.add(Disponibilites(max_id_dispo()+1,current_user.id_vacataire,periodes[item][0],periodes[1],periodes[0], periodes[item][1], periodes[item][2], date.today(),datetemps.now().strftime("%H:%M:%S")))
            db.session.commit()
        for item in jours_spe:
            db.session.add(Disponibilites(max_id_dispo()+1,current_user.id_vacataire,item[0],-1,-1, item[1], item[2],date.today(),datetemps.now().strftime("%H:%M:%S")))
            db.session.commit()
    return render_template('disponibilites.html')

@app.route('/nouveau_vacataire/', methods= ['GET', 'POST'])
def new_vaca():
    from datetime import datetime
    form = InscriptionVacataire()
    if request.method == "POST":
        id = max_id_actuel()
        cds,mdp = saler_mot_de_passe(form.password.data)
        try:
            vac = Vacataire('V' + id,'Spontanée',form.entreprise.data,'0', form.nom.data ,form.prenom.data ,form.tel.data,form.ddn.data,form.email.data,mdp,"","","","","",cds)
            date_actuelle = date.today()
            heure_actuelle = datetime.now().strftime("%H:%M")
            dossier = GererDossier(vac.id_vacataire,current_user.id_pers_admin,"Distribué",date_actuelle,heure_actuelle)
            db.session.add(vac)
            db.session.add(dossier)
            db.session.commit()
            return redirect(url_for('menu_admin'))
        except Exception as e:
            flash("Le numéro de téléphone ou l'adresse email est déjà utilisée, veuillez vérifier vos infromations")
    return render_template('nouveau_vacataire.html', form = form)


@app.route('/menu_admin/') 
@login_required
def menu_admin():
    return render_template('menu_admin.html',nom_prenom=current_user.prenom_pa + " " + current_user.nom_pa)

@app.route('/assigner_matieres/<id_v>', methods= ['GET', 'POST'])
@login_required
def assigner_matieres(id_v):
    def listeTri(firstVariable):
        if firstVariable == 'Identifiant':
            return ["Identifiant","Domaine","Responsable","Ne pas trier"]
        elif firstVariable == 'Domaine':
            return ["Domaine","Identifiant","Responsable","Ne pas trier"]
        elif firstVariable == 'Responsable':
            return ["Responsable","Identifiant","Domaine","Ne pas trier"]
        else:
            return ["Ne pas trier","Identifiant","Domaine","Responsable"]        
    text_place = "Veuillez sélectionner une méthode de tri..."
    liste_de_tri = ["Ne pas trier","Identifiant","Domaine","Responsable"] 
    if request.method == "POST":
        liste_de_tri = listeTri(request.form['tri'])
        matieres = searchDomaine(id_v,request.form['tri'],request.form['search'])
    elif request.method == "GET":
        matieres = searchDomaine(id_v)
    return render_template('assigner_matieres.html',id_vacataire=id_v,domaine=matieres,text_place = text_place,liste_de_tri = liste_de_tri)

@app.route('/info_domaine/<idM>', methods= ['GET'])
@login_required
def voir_infos(idM,idV=""):
    domaine = get_domaine(idM)
    return render_template('infos_matieres.html',domaine=domaine,idv=idV)

@app.route('/edit_assignement/<id_v>/<id_m>',methods= ['GET', 'POST'])
@login_required
def edit_assignement(id_v,id_m):
    """
    recup a partir du form
    {
        "2022-23": { # Année début de la période scolaire
            1: { # periode
                "lundi": [ # Jour de la semaine
                    ("08:00", "10:00", "TP", "22A"), # Informations des cours ce jour
                    ("10:00","12:00", "TD","22")
                ]
            }
        }
    }
    a envoyer a la page
    {
        "2022-23": {
            1: {
                "lundi": {
                    "heure_debut": "08:00",
                    "heure_fin": "12:00"
                }
            },
            2: [{
                "lundi": {
                    "heure_debut": "08:00",
                    "heure_fin": "12:00"
                }]
            }
        }
    }
    """
    dispos = get_dispos(id_v)
    dispos_dates = []
    dispos_propres = dict()
    dispo_propre = dict()
    for dispo in dispos:
        if not dispo.periode_dispo == -1:
            periode = dict()
            jour = dict()
            if dispo.periode_dispo not in dispos_propres.keys():
                dispo_propre = dict()
            jour["heure_debut"] = dispo.heure_dispo_debut
            jour["heure_fin"] = dispo.heure_dispo_fin
            periode[dispo.jour_dispo] = jour
            if dispo.semestre_dispo in dispo_propre.keys():
                dispo_propre[dispo.semestre_dispo].append(periode)
            else:
                dispo_propre[dispo.semestre_dispo] = [periode]
            dispos_propres[dispo.periode_dispo] = dispo_propre
                
        else:
            dispos_dates.append(dispo)
    if request.method == "POST":
        dico = dispos_propres
        dom = get_domaine(id_m)
        dates_periode = get_dates_from_json_file("static/data/periodes.json")
        for annee,periodes in dico.items():
            for periode,liste_dispos in periodes.items():
                for dico_jours in liste_dispos:
                    for jour in dico_jours.keys():
                        dico_jours[jour] = []
                        i = 0
                        loop = True
                        while(loop):
                            try:
                                dico_jours[jour].append((request.form[str(jour)+"-"+str(annee)+"-"+str(periode)+"-Debut"+str(i)],
                                                  request.form[str(jour)+"-"+str(annee)+"-"+str(periode)+"-Fin"+str(i)],
                                                  request.form[str(jour)+"-"+str(annee)+"-Type"+str(i)],
                                                  request.form[str(jour)+"-"+str(annee)+"-Classe"+str(i)]))
                                i+=1
                            except Exception:
                                loop = False
                        for ind in range(len(dico_jours[jour])):
                            id = str(max_id_cours())
                            calc = duree_entre_deux_temps(dico_jours[jour][ind][0],dico_jours[jour][ind][1])
                            db.session.add(Cours(id,dico_jours[jour][ind][2],dom.domaine,str(calc),dom.id_domaine))
                            db.session.commit()
                            for date_uniq in dates_periode[annee][periode]:
                                if get_jour(date_uniq,jour):
                                    db.session.add(Assigner(id_v,id,dico_jours[jour][2],"I003",dico_jours[jour][ind][3],date_uniq,dico_jours[jour][ind][0]))
                                    db.session.commit()
        i2=0
        for dispo in dispos_dates:
            dom = get_domaine(id_m)
            liste_dates = []
            id = str(max_id_cours())
            duree = duree_entre_deux_temps(request.form.get("date-"+str(dispo.id_dispo)+"-Debut"+str(i2),request.form.get("date-"+str(dispo.id_dispo)+"-Fin"+str(i2))))
            db.session.add(Cours(
                    id,
                    request.form.get("date-"+str(dispo.id_dispo)+"-Type"+str(i)),
                    dom.domaine,
                    duree,
                    dom.id_domaine
            ))
            db.session.commit()
            db.session.add(Assigner(
                    id_v,
                    id,
                    request.form.get("date-"+str(dispo.id_dispo)+"-Type"+str(i)),
                    "I003",
                    request.form.get("date-"+str(dispo.id_dispo)+"-Classe"+str(i)),
                    request.form.get("date-"+str(dispo.id_dispo)),
                    request.form.get("date-"+str(dispo.id_dispo)+"-Debut"+str(i))
            ))
            db.session.commit()
            i2+=1
        return redirect(url_for("menu_admin"))
    return render_template("edit_assignement.html",disponibilitesPeriode=dispos_propres, disponibilitesDates=dispos_dates)

@app.route('/profile/')
@login_required
def profile():
    if est_vacataire(current_user):
        return render_template('profile.html',profile_nom=current_user.nom_v, profile_prenom=current_user.prenom_v, profile_email=current_user.mail_v, profile_tel=current_user.num_tel_v, idUser = current_user.id_vacataire)
    return render_template('profile.html',profile_nom=current_user.nom_pa, profile_prenom=current_user.prenom_pa, profile_email=current_user.mail_pa, profile_tel=current_user.num_tel_pa, idUser = current_user.id_pers_admin)

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
    filtre = []
    for item in db.session.query(Cours.nom_cours).all():
        filtre.append(item[0])
    liste_matieres = []
    for item in filtre:
        if item not in liste_matieres:
            liste_matieres.append(item)
    plh="Selectionnez un filtre..."
    listeCours = db.session.query(Vacataire.nom_v, Vacataire.prenom_v, Cours.nom_cours, Cours.type_cours, Cours.duree_cours, Assigner.date_cours, Assigner.heure_cours, Assigner.classe, Assigner.salle).join(Assigner, Assigner.id_vacataire == Vacataire.id_vacataire).join(Cours, Cours.id_cours == Assigner.id_cours).order_by(Cours.nom_cours).all()
    if request.method == "POST":
         listeCours = searchCours(request.form['infos'],request.form['nick'],request.form['search'])
    return render_template('recherche-cours.html',cours=listeCours,filtre=liste_matieres,placeHolder=plh)           

@app.route('/dossier_vacataire/', methods=['GET','POST',])
@login_required
def dossier_vacataire():
    vacataire = get_vacataire(current_user.id_vacataire)
    dossier = get_dossier(current_user.id_vacataire)
    acc = InscriptionVacataire(vacataire)
    return render_template("dossier_vacataire.html", form=acc, dossier=dossier, date_modif_dossier=dossier.date_modif)

@app.route('/edit_dossier_vacataire/', methods=['GET','POST',])
@login_required
def edit_dossier():
    vacataire = get_vacataire(current_user.id_vacataire)
    dossier = get_dossier(current_user.id_vacataire)
    form = InscriptionVacataire(vacataire)    
    if request.method=="POST":
        update_dossier_vac(vacataire,request.form.get("legal"),
                   nom=request.form.get("nom"),
                   prenom=request.form.get("prenom"),
                   tel=request.form.get("tel"),
                   ddn=request.form.get("ddn"),
                   mail=request.form.get("email"),
                   entreprise=request.form.get("entreprise"),
                   nationalite=request.form.get("nationalite"),
                   profession=request.form.get("profession"),
                   meilleur_diplome=request.form.get("meilleur_diplome"),
                   annee_obtiention=request.form.get("annee_obtiention"),
                   adresse=request.form.get("adresse"))
        actualiser_date_dossier(dossier)
        editeur_auto_doc(dossier,vacataire)   
        return redirect(url_for("menu_vacataire"))
    return render_template("dossier_vacataire.html", form=form, dossier=dossier, date_modif_dossier=dossier.date_modif)

@app.route('/menu_vacataire/')
@login_required
def menu_vacataire():
    return render_template('menu_vacataire.html',nom_prenom=current_user.prenom_v + " " + current_user.nom_v)

@app.route('/dossier/<id>/', methods=['GET', 'POST'])
@login_required
def voir_dossier_vacataire(id):
    vacataire = Vacataire.query.filter_by(id_vacataire=id).first()
    dossier = get_dossier(id)
    droit_changement_dossier = False
    if current_user.id_pers_admin == dossier.id_pers_admin:
        droit_changement_dossier = True
        
    if request.method == 'POST':
        actualiser_date_dossier(dossier)
        dossier.etat_dossier = "Validé"
        db.session.commit()
        return render_template('voir_dossier.html', info_vacataire=vacataire, date_modif=dossier.date_modif, heure_modif=dossier.heure_modif, etat=dossier.etat_dossier, admin_du_dossier=droit_changement_dossier)

    return render_template('voir_dossier.html', info_vacataire=vacataire, date_modif=dossier.date_modif, heure_modif=dossier.heure_modif, etat=dossier.etat_dossier, admin_du_dossier=droit_changement_dossier)
    
@app.route("/logout/")
def logout():
    logout_user()
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
            Disponibilites.query.filter(Disponibilites.id_vacataire == current_user.id_vacataire, Disponibilites.periode_dispo == -1, Disponibilites.jour_dispo == date[0], Disponibilites.heure_dispo_debut == date[1], Disponibilites.heure_dispo_fin == date[2]).delete()
        db.session.commit()
        liste_periode = db.session.query(Disponibilites.semestre_dispo, Disponibilites.periode_dispo, Disponibilites.jour_dispo, Disponibilites.heure_dispo_debut, Disponibilites.heure_dispo_fin).filter(Disponibilites.periode_dispo != -1).all()
        liste_dates = db.session.query(Disponibilites.jour_dispo, Disponibilites.heure_dispo_debut, Disponibilites.heure_dispo_fin).filter(Disponibilites.periode_dispo == -1).all()
    return render_template("EDT.html",liste_periodes = liste_periode, liste_dates = liste_dates)

@app.route('/changer_mdp/', methods=["GET", "POST"])
@login_required
def changer_mdp():
    form = NouveauMDP()
    valide = True
    erreur = ""
    if request.method == "POST":
        if current_user.__class__ is PersonnelAdministratif:
            if not verifier_mot_de_passe(form.mdp_actuel.data, current_user.cds_pa, current_user.mdp_pa):
                valide = False
                erreur = "Le mot de passe actuel ne correspond pas."
                return render_template("changer_mdp.html", form=form, valide=valide, erreur=erreur)
            elif form.nouveau_mdp.data != form.confirmation.data:
                valide = False
                erreur = "Le nouveau mot de passe ne correspond pas à la répétition."
                return render_template("changer_mdp.html", form=form, valide=valide, erreur=erreur)
            else:
                current_user.cds_pa, current_user.mdp_pa = saler_mot_de_passe(form.nouveau_mdp.data)
                db.session.commit()
                return redirect(url_for("menu_admin"))
        else:
            if not verifier_mot_de_passe(form.mdp_actuel.data, current_user.cds_v, current_user.mdp_v):
                valide = False
                erreur = "Le mot de passe actuel ne correspond pas."
                return render_template("changer_mdp.html", form=form, valide=valide, erreur=erreur)
            elif form.nouveau_mdp.data != form.confirmation.data:
                valide = False
                erreur = "Le nouveau mot de passe ne correspond pas à la répétition."
                return render_template("changer_mdp.html", form=form, valide=valide, erreur=erreur)
            else:
                current_user.cds_v, current_user.mdp_v = saler_mot_de_passe(form.nouveau_mdp.data)
                db.session.commit()
                return redirect(url_for("menu_vacataire"))
    return render_template("changer_mdp.html", form=form, valide=valide, erreur=erreur)

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

def anti_doublons(liste):
    res = []
    liste_matieres = []
    for item in liste:
        if item[0] not in liste_matieres:
            res.append(item)
            liste_matieres.append(item[0])
    return res

if __name__=="__main__":
    app.run(4095)
