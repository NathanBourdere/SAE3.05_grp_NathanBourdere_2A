# pip install Flask
# pip install flask_sqlalchemy

from flask import Flask,render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import csv

# Suppression de l'ancienne BD
if os.path.exists("instance/db.sqlite3"):
  os.remove("instance/db.sqlite3")
  os.rmdir('instance')

# Configuration de l'application Flask
app=Flask(__name__,template_folder='static/HTML')
app.app_context().push()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

# Création de la base de donnée
db = SQLAlchemy(app)

# Initialisation des tables ORM
class GererDossier(db.Model):
    __tablename__= "GererDossier"

    IDVacataire = db.Column(db.String(100),db.ForeignKey("Vacataire.IDVacataire"),primary_key=True,nullable=False)
    IDpersAdmin = db.Column(db.String(100),db.ForeignKey("PersonnelAdministratif.IDpersAdmin"),primary_key=True,nullable=False)
    etat_dossier = db.Column(db.String(100))
    dateModif = db.Column(db.String(100))
    heureModif = db.Column(db.Integer)

    personnelAdmin = db.relationship('PersonnelAdministratif',back_populates="gerant_dossier")
    dossierVacataire = db.relationship("Vacataire", back_populates = "selfdossier")

    def __init__(self,idv,idp,edoc,date,h):
        self.IDVacataire = idv
        self.IDpersAdmin = idp
        self.etat_dossier = edoc
        self.dateModif = date
        self.heureModif = h
    
    def __str__(self):
        return "Dossier du vacataire "+self.IDVacataire+", modification le ",self.dateModif," à "+ str(self.heureModif)+"par "+self.IDpersAdmin+", le dossier est "+self.etat_dossier

class Assigner(db.Model):
    __tablename__ = "Assigner"

    IDVacataire = db.Column(db.String(100),db.ForeignKey("Vacataire.IDVacataire"),primary_key=True,nullable=False)
    IDcours = db.Column(db.String(100),db.ForeignKey("Cours.IDcours"),primary_key=True,nullable=False)
    TypeCours = db.Column(db.String(100),db.ForeignKey("Cours.TypeCours"),primary_key=True,nullable=False)
    salle = db.Column(db.String(100))
    classe = db.Column(db.String(100))
    dateCours = db.Column(db.String(100))
    HeureCours = db.Column(db.Integer)

    cours_a_vacataire = db.relationship("Vacataire",back_populates="vacataire_assignee")
    assigner_cours = db.relationship("Cours",back_populates="cours_assignee")

    def __init__(self,idv,idc,t,s,c,d,h):
        self.IDVacataire = idv
        self.IDcours = idc
        self.TypeCours = t
        self.classe = c
        self.salle = s
        self.DateCours = d
        self.HeureCours = h
    
    def __str__(self):
        return "Le vacataire "+self.IDVacataire+" est assigné au cours "+self.TypeCours+" "+self.IDcours+" avec la classe "+self.classe+" dans la salle "+self.salle+" le ",str(self.DateCours)+" à "+str(self.HeureCours)

class PersonnelAdministratif(db.Model):
    __tablename__ = 'PersonnelAdministratif'

    IDpersAdmin = db.Column(db.String(100),primary_key=True,nullable=False)
    nomPa = db.Column(db.String(100))
    prenomPa = db.Column(db.String(100))
    numTelPa = db.Column(db.String(100),unique=True)
    ddnPa = db.Column(db.String(100))
    mailPa = db.Column(db.String(100),unique=True)
    mdpPa = db.Column(db.String(100))

    gerant_dossier = db.relationship("GererDossier", backref = "personnelAdmin")

    def __init__(self,idpa,nom,pnom,tel,ddn,mail,mdp):
        self.IDpersAdmin = idpa
        self.nomPa = nom
        self.prenomPa = pnom
        self.numTelPa = tel
        self.ddnPa = ddn
        self.mailPa = mail
        self.mdpPa = mdp
    
    def __str__(self):
        return "PersonnelAdministratif :"+" "+self.IDpersAdmin+" "+self.nomPa+" "+self.prenomPa+" né(e) le ",self.ddnPa," mail : "+self.mailPa

affectable = db.Table("Affectable",db.Column("IDVacataire",db.Integer,db.ForeignKey("Vacataire.IDVacataire"),primary_key=True,nullable=False),
                                   db.Column("IDCours",db.String(100),db.ForeignKey("Cours.IDcours"),primary_key=True,nullable=False),
                                   db.Column("TypeCours",db.String(100),db.ForeignKey("Cours.TypeCours"),primary_key=True,nullable=False)
                     )

class Vacataire(db.Model):
    __tablename__ = "Vacataire"

    IDVacataire = db.Column(db.String(100),primary_key=True,nullable=False)
    candidature = db.Column(db.String(100)) 
    ancien = db.Column(db.Integer) #0 ou 1
    nomV = db.Column(db.String(100))
    prenomV = db.Column(db.String(100))
    numTelV = db.Column(db.String(100),unique=True)
    ddnV = db.Column(db.String(100))
    mailV = db.Column(db.String(100),unique=True)
    mdpV = db.Column(db.String(100))

    cours_affectable = db.relationship("Cours",secondary=affectable)
    selfdossier = db.relationship("GererDossier", back_populates = "dossierVacataire")
    vacataire_assignee = db.relationship("Assigner", back_populates ="cours_a_vacataire")
    dispo = db.relationship("Disponibilites", backref = "vacataire")

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
    
    def __str__(self):
        return "Vacataire : "+" "+self.IDVacataire+" "+self.nomV+" "+self.prenomV+" né(e) le "+self.ddnV+" mail : "+self.mailV+" type de candidature : "+self.candidature+" est ancien :"+str(self.ancien)

class Cours(db.Model):
    __tablename__= "Cours"

    IDcours = db.Column(db.String(100),primary_key=True,nullable=False)
    TypeCours = db.Column(db.String(100),primary_key=True,nullable=False)
    nomCours = db.Column(db.String(100),nullable=False)
    domaine = db.Column(db.String(100),nullable=False)
    heuresTotale = db.Column(db.Integer)
    dureeCours = db.Column(db.Integer)

    cours_assignee = db.relationship("Assigner",back_populates="assigner_cours")
    vacataires_affectable = db.relationship("Vacataire",secondary=affectable)

    def __init__(self,idc,t,n,d,h,dur):
        self.IDcours = idc
        self.TypeCours = t
        self.nomCours = n
        self.domaine = d
        self.heuresTotale = h
        self.dureeCours = dur
    
    def __str__(self):
        return self.TypeCours+" "+self.IDcours+" : "+self.nomCours+" domaine de "+self.domaine+" "+self.heuresTotale+" d'heures totale pour une duree de "+self.dureeCours+" par cours"

class Disponibilites(db.Model):
    __tablename__ = "Disponibilites"

    IDdispo = db.Column(db.String(100),primary_key=True)
    jourDispo = db.Column(db.String(100))# lundi,mardi ... PAS DIMANCHE
    semaineDispo = db.Column(db.Integer) # 1,2 jusqu'à 52
    periodeDispo = db.Column(db.Integer) # 1 ou 2 ou 3 ou 4, il y a 2 périodes par semestre
    heureDispoDebut = db.Column(db.String(100)) # "14:30"
    heureDispoFin = db.Column(db.String(100)) # idem
    IDVacataire = db.Column(db.String(100),db.ForeignKey("Vacataire.IDVacataire"),nullable=False,unique=True)

    def __init__(self,idd,j,s,p,hd,hf,idv):
        self.IDdispo = idd
        self.jourDispo = j
        self.semaineDispo = s
        self.periodeDispo = p
        self.heureDispoDebut = hd
        self.heureDispoFin = hf
        self.IDVacataire = idv
    
    def __str__(self):
        res = "Vacataire "+self.IDVacataire+" dispo. id : "+self.IDdispo+" : "+self.jourDispo
        res += " semaine "+self.semaineDispo+" de la période "+self.periodeDispo
        res += " disponible de "+self.heureDispoDebut +" jusqu'à "+self.heureDispoFin+"\n"
        return res

db.create_all()
db.session.commit()

# Initialisation des routes
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/nouveau_vacataire.html', methods= ['GET', 'POST'])
def new_vaca():
    if request.method == "POST":
        vac = Vacataire('V4','Spontanée','0',request.form['nom'],request.form['prenom'],request.form['tel'],'30-02-1997',request.form['email'],'177013')
        db.session.add(vac)
        db.session.commit()
    return render_template('nouveau_vacataire.html')

@app.route('/EDT.html')
def EDT():
    return render_template('EDT.html')

@app.route('/menu_admin.html')
def menu_admin():
    return render_template('menu_admin.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')

@app.route('/recherche-dossiers.html')
def check_doss():
    return render_template('recherche-dossiers.html')           

@app.route('/login.html')
def log():
    return render_template('/login.html')

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
                        db.session.add(affectable(ligne[0],ligne[1],ligne[2]))
                        db.session.commit()
                case 5:
                    for ligne in fileReader:
                        db.session.add(Assigner(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6]))
                        db.session.commit()

test_connection()

if __name__=="__main__":
    app.run()