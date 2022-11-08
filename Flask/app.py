# pip install flask
# pip install flask_sqlalchemy
# pip install flask_login

from flask import Flask,render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import os
import csv

# Suppression de l'ancienne BD
if os.path.exists("instance/db.sqlite3"):
  os.remove("instance/db.sqlite3")
  os.rmdir('instance')

# Configuration de l'application Flask
app=Flask(__name__,template_folder='static/HTML')
app.secret_key = "mot de passe trop crypté"
app.app_context().push()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
login_manager = LoginManager()
login_manager.init_app(app)

# Création de la base de donnée
db = SQLAlchemy(app)

# Initialisation des tables ORM
class PersonnelAdministratif(UserMixin,db.Model):
    __tablename__ = 'PersonnelAdministratif'

    IDpersAdmin = db.Column(db.Text,primary_key=True)
    nomPa = db.Column(db.Text)
    prenomPa = db.Column(db.Text)
    numTelPa = db.Column(db.Text)
    ddnPa = db.Column(db.Text)
    mailPa = db.Column(db.Text)
    mdpPa = db.Column(db.Text)

    # dossierVacataire = db.relationship("Vacataire", back_populates = "selfdossier")
    # gererdossier = db.relationship("GererDossier", back_populates = "gerantdossier")

    def __init__(self,idpa,nom,pnom,tel,ddn,mail,mdp):
        self.IDpersAdmin = idpa
        self.nomPa = nom
        self.prenomPa = pnom
        self.numTelPa = tel
        self.ddnPa = ddn
        self.mailPa = mail
        self.mdpPa = mdp

    def get_id(self):
           return (self.IDpersAdmin)

    def __str__(self):
        return "PersonnelAdministratif :"+" "+self.IDpersAdmin+" "+self.nomPa+" "+self.prenomPa+" né(e) le ",self.ddnPa," mail : "+self.mailPa

class Vacataire(UserMixin, db.Model):
    __tablename__ = "vacataire"

    IDVacataire = db.Column(db.Text,primary_key=True)
    candidature = db.Column(db.Text) #0 ou 1
    ancien = db.Column(db.Integer)
    nomV = db.Column(db.Text)
    prenomV = db.Column(db.Text)
    numTelV = db.Column(db.Text)
    ddnV = db.Column(db.Text)
    mailV = db.Column(db.Text)
    mdpV = db.Column(db.Text)
    
    # selfdossier = db.relationship("PersonnelAdministratif", back_populates = "dossierVacataire")
    # dossier_qui_se_fait_gerer = db.relationship("GererDossier", back_populates = "dossierDuVacataire")
    # vacataire_a_cours = db.relationship("Cours", back_populates ="cours_a_vacataire")
    # vacataire_a_affectable = db.relationship("Affectable", back_populates = "affectable_a_vacataire")
    # vacataire_a_assigner = db.relationship("Assigner", back_populates = "assigner_a_vacataire")

    def __init__(self,idv,candidature,est_ancien,nom,pnom,tel,ddn,mail,mdp):
        self.IDVacataire = idv
        self.candidature = candidature
        self.ancien = est_ancien
        self.nomV = nom
        self.prenomV = pnom
        self.numTelV = tel
        self.ddnV = ddn
        self.mailV = mail
        self.mdpV = mdp
    
    def get_id(self):
        return (self.IDVacataire)

    def __str__(self):
        return "Vacataire : "+" "+self.IDVacataire+" "+self.nomV+" "+self.prenomV+" né(e) le "+self.ddnV+" mail : "+self.mailV+" type de candidature : "+self.candidature+" est ancien :"+str(self.ancien)

class GererDossier(db.Model):
    __tablename__= "GererDossier"

    IDVacataire = db.Column(db.Text,primary_key=True)
    IDpersAdmin = db.Column(db.Text,primary_key=True)
    etat_dossier = db.Column(db.Text)
    dateModif = db.Column(db.Text)
    heureModif = db.Column(db.Integer)

    # gerantdossier = db.relationship("PersonnelAdministratif",back_populates="gererdossier")
    # dossierDuVacataire =db.relationship("Vacataire",back_populates="dossier_qui_se_fait_gerer")

    def __init__(self,idv,idp,edoc,date,h):
        self.IDVacataire = idv
        self.IDpersAdmin = idp
        self.etat_dossier = edoc
        self.dateModif = date
        self.heureModif = h
    
    def __str__(self):
        return "Dossier du vacataire "+self.IDVacataire+", modification le ",self.dateModif," à "+ str(self.heureModif)+"par "+self.IDpersAdmin+", le dossier est "+self.etat_dossier

class Cours(db.Model):
    __tablename__= "Cours"

    IDcours = db.Column(db.Text,primary_key=True)
    TypeCours = db.Column(db.Text,primary_key=True)
    nomCours = db.Column(db.Text)
    domaine = db.Column(db.Text)
    heuresTotale = db.Column(db.Integer)
    dureeCours = db.Column(db.Integer)

    # cours_a_assigner = db.relationship("Assigner",back_populates="assigner_a_cours")
    # cours_a_affectable = db.relationship("Affectable",back_populates="affectable_a_cours")
    # cours_a_vacataire = db.relationship("Vacataire",back_populates="vacataire_a_cours")

    def __init__(self,idc,t,n,d,h,dur):
        self.IDcours = idc
        self.TypeCours = t
        self.nomCours = n
        self.domaine = d
        self.heuresTotale = h
        self.dureeCours = dur
    
    def __str__(self):
        return self.TypeCours+" "+str(self.IDcours)+" : "+self.nomCours+" domaine de "+self.domaine+" "+str(self.heuresTotale)+" d'heures totale pour une duree de "+str(self.dureeCours)+" par cours"

class Affectable(db.Model):
    __tablename__= "Affectable"

    IDVacataire = db.Column(db.Text,primary_key=True)
    IDcours = db.Column(db.Text,db.ForeignKey("Cours.IDcours"),primary_key=True)
    TypeCours = db.Column(db.Text,db.ForeignKey("Cours.TypeCours"),primary_key=True)

    # affectable_a_vacataire = db.relationship("Vacataire",back_populates="vacataire_a_affectable")
    # affectable_a_cours = db.relationship("Cours",back_populates="cours_a_affectable")

    def __init__(self,idv,idc,tc):
        self.IDVacataire = idv
        self.IDcours = idc
        self.TypeCours = tc
    
    def __str__(self):
        return self.IDVacataire+" est affectable à "+self.IDcours+" "+self.TypeCours

class Assigner(db.Model):
    __tablename__ = "Assigner"

    IDVacataire = db.Column(db.Text,primary_key=True)
    IDcours = db.Column(db.Text,db.ForeignKey("Cours.IDcours"),primary_key=True)
    TypeCours = db.Column(db.Text,db.ForeignKey("Cours.TypeCours"),primary_key=True)
    salle = db.Column(db.Text)
    classe = db.Column(db.Text)
    dateCours = db.Column(db.Text)
    HeureCours = db.Column(db.Integer)

    # assigner_a_vacataire = db.relationship("Vacataire",back_populates="vacataire_a_assigner")
    # assigner_a_cours = db.relationship("Cours",back_populates="cours_a_assigner")

    def __init__(self,idv,idc,t,s,c,d,h):
        self.IDVacataire = idv
        self.IDcours = idc
        self.TypeCours = t
        self.classe = c
        self.salle = s
        self.DateCours = d
        self.HeureCours = h
    
    def __str__(self):
        return "Le vacataire "+self.IDVacataire+" est assigné au cours "+self.TypeCours+" "+self.IDcours+" avec la classe "+self.classe+" dans la salle "+self.salle+" le ",self.db.TextCours+" à "+str(self.HeureCours)

db.create_all()
db.session.commit()

# Initialisation des routes
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/nouveau_vacataire.html', methods= ['GET', 'POST'])
def new_vaca():
    if request.method == "POST":
        vac = Vacataire('V' + maxIdActu(),'Spontanée','0',request.form['nom'],request.form['prenom'],request.form['tel'],request.form['ddn'],request.form['email'],'177013')
        listeCours = []
        for i in range(1,4):
            ez = Cours.query.filter_by(nomCours=request.form['Matiere'+str(i)]).all()
            for cours in ez:
                db.session.add(Affectable('V' + maxIdActu(),cours.IDcours,cours.TypeCours))
        db.session.add(vac)
        db.session.commit()
    return render_template('nouveau_vacataire.html')

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

@app.route('/recherche-dossiers.html')
@login_required
def check_doss():
    return render_template('recherche-dossiers.html')           

@app.route('/login.html', methods= ['GET', 'POST'])
def log():
    if request.method == "POST":
        if estVacataire(request.form['idUser']):
            log = Vacataire.query.filter_by(IDVacataire=request.form['idUser']).first()
            if request.form['password'] == log.mdpV:
                login_user(log)
                return EDT()
        else:
            adm = PersonnelAdministratif.query.filter_by(IDpersAdmin=request.form['idUser']).first()
            if request.form['password'] == adm.mdpPa:
                login_user(adm)
                return menu_admin()
    return render_template('login.html')

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
                        db.session.commit()
                case 1:
                    for ligne in fileReader:
                        db.session.add(Vacataire(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6],ligne[7],ligne[8]))
                        db.session.commit()
                case 2:
                    for ligne in fileReader:
                        db.session.add(GererDossier(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4]))
                        db.session.commit()
                case 3:
                    for ligne in fileReader:
                        db.session.add(Cours(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5]))
                        db.session.commit()
                case 4:
                    for ligne in fileReader:
                        db.session.add(Affectable(ligne[0],ligne[1],ligne[2]))
                        db.session.commit()
                case 5:
                    for ligne in fileReader:
                        db.session.add(Assigner(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6]))
                        db.session.commit()

test_connection()

if __name__=="__main__":
    app.run()