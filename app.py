from flask import Flask,render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import os
import csv

# Suppression de l'ancienne BD
if os.path.exists("instance/db.sqlite3"):
  os.remove("instance/db.sqlite3")
  os.rmdir('instance')

# Configuration de l'application Flask et la base de données
app=Flask(__name__,template_folder='static/HTML')
app.secret_key = "IUTO"
app.app_context().push()
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
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
    assigner_cours_id = db.relationship("Cours",back_populates="cours_assignee_id", foreign_keys=[IDcours])
    assigner_cours_type = db.relationship("Cours",back_populates="cours_assignee_type", foreign_keys=[TypeCours])

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

class PersonnelAdministratif(UserMixin,db.Model):
    __tablename__ = 'PersonnelAdministratif'

    IDpersAdmin = db.Column(db.String(100),primary_key=True,nullable=False)
    nomPa = db.Column(db.String(100))
    prenomPa = db.Column(db.String(100))
    numTelPa = db.Column(db.String(100),unique=True)
    ddnPa = db.Column(db.String(100))
    mailPa = db.Column(db.String(100),unique=True)
    mdpPa = db.Column(db.String(100))

    gerant_dossier = db.relationship("GererDossier", back_populates = "personnelAdmin")

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


class Affectable(db.Model):
    tablename__ = "Affectable"

    IDVacataire = db.Column(db.String(100),db.ForeignKey("Vacataire.IDVacataire"),primary_key=True)
    IDcours = db.Column(db.String(100),db.ForeignKey("Cours.IDcours"),primary_key=True)
    TypeCours = db.Column(db.String(100),db.ForeignKey("Cours.TypeCours"),primary_key=True)

    cours_affecter_vacataire = db.relationship("Vacataire",back_populates="vacat_affectable")
    affecter_cours_id = db.relationship("Cours",back_populates="cours_affecter_id", foreign_keys=[IDcours])
    affecter_cours_type = db.relationship("Cours",back_populates="cours_affecter_type", foreign_keys=[TypeCours])

    def __init__(self,idv,idc,t):
        self.IDVacataire = idv
        self.IDcours = idc
        self.TypeCours = t
    
    def __str__(self):
        return "Le vacataire "+self.IDVacataire+" est assigné au cours "+self.TypeCours+" "+self.IDcours

class Domaine(db.Model):
    __tablename__ = "Domaine"

    domaine = db.Column(db.String(100),primary_key=True)
    responsable = db.Column(db.String(100),nullable=False)

    le_cours = db.relationship("Cours", backref = "cours")

    def __init__(self,nomdom,resp):
        self.domaine = nomdom
        self.responsable = resp

    
    def __str__(self):
        return "Le domaine "+self.domaine+" est sous la responsabilité de "+self.responsable

class Vacataire(UserMixin,db.Model):
    __tablename__ = "Vacataire"

    IDVacataire = db.Column(db.String(100),primary_key=True)
    candidature = db.Column(db.String(100),nullable=False) 
    ancien = db.Column(db.Integer) #0 ou 1
    entreprise = db.Column(db.String(100))
    nomV = db.Column(db.String(100))
    prenomV = db.Column(db.String(100))
    numTelV = db.Column(db.String(100),unique=True)
    ddnV = db.Column(db.String(100))
    mailV = db.Column(db.String(100),unique=True)
    mdpV = db.Column(db.String(100))

    vacat_affectable = db.relationship("Affectable",back_populates="cours_affecter_vacataire",foreign_keys=[Affectable.IDVacataire])
    selfdossier = db.relationship("GererDossier", back_populates = "dossierVacataire")
    vacataire_assignee = db.relationship("Assigner", back_populates ="cours_a_vacataire")
    dispo = db.relationship("Disponibilites", backref = "vacataire")

    def __init__(self,idv,candidature,ent,est_ancien,nom,pnom,tel,ddn,mail,mdp):
        self.IDVacataire = idv
        self.candidature = candidature
        self.entreprise = ent
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
        return "Vacataire : "+" "+self.IDVacataire+" "+self.nomV+" "+self.prenomV+" né(e) le "+self.ddnV+" mail : "+self.mailV+" type de candidature : "+self.candidature+" est ancien :"+str(self.ancien)+" de l'entreprise "+self.entreprise

class Cours(db.Model):
    __tablename__= "Cours"

    IDcours = db.Column(db.String(100),primary_key=True)
    TypeCours = db.Column(db.String(100),primary_key=True)
    nomCours = db.Column(db.String(100),nullable=False)
    heuresTotale = db.Column(db.Integer)
    dureeCours = db.Column(db.Integer)
    domaine = db.Column(db.String(100),db.ForeignKey("Domaine.domaine"),nullable=False)

    cours_assignee_id = db.relationship("Assigner",back_populates="assigner_cours_id", foreign_keys=[Assigner.IDcours])
    cours_assignee_type = db.relationship("Assigner",back_populates="assigner_cours_type", foreign_keys=[Assigner.TypeCours])
    cours_affecter_id = db.relationship("Affectable",back_populates="affecter_cours_id",foreign_keys=[Affectable.IDcours])
    cours_affecter_type = db.relationship("Affectable",back_populates="affecter_cours_type",foreign_keys=[Affectable.TypeCours])

    def __init__(self,idc,t,n,h,dur,dom):
        self.IDcours = idc
        self.TypeCours = t
        self.nomCours = n
        self.heuresTotale = h
        self.dureeCours = dur
        self.domaine = dom
    
    def __str__(self):
        return self.TypeCours+" "+str(self.IDcours)+" : "+self.nomCours+" "+str(self.heuresTotale)+" d'heures totale pour une duree de "+str(self.dureeCours)+" par cours "+" du domaine "+self.domaine

class Disponibilites(db.Model):
    __tablename__ = "Disponibilites"

    IDdispo = db.Column(db.String(100),primary_key=True)
    jourDispo = db.Column(db.String(100))# lundi,mardi ... PAS DIMANCHE
    semaineDispo = db.Column(db.Integer) # 1,2 jusqu'à 52
    periodeDispo = db.Column(db.Integer) # 1 ou 2 ou 3 ou 4, il y a 2 périodes par semestre
    heureDispoDebut = db.Column(db.String(100)) # "14:30"
    heureDispoFin = db.Column(db.String(100)) # idem
    dateModifDispo = db.Column(db.String(100))
    heureModifDispo = db.Column(db.Integer)
    IDVacataire = db.Column(db.String(100),db.ForeignKey("Vacataire.IDVacataire"),nullable=False,unique=True)

    def __init__(self,idd,j,s,p,hd,hf,idv,dmd,hmd):
        self.IDdispo = idd
        self.jourDispo = j
        self.semaineDispo = s
        self.periodeDispo = p
        self.heureDispoDebut = hd
        self.heureDispoFin = hf
        self.IDVacataire = idv
        self.dateModifDispo = dmd
        self.heureModifDispo = hmd

    def __str__(self):
        res = "Vacataire "+self.IDVacataire+" dispo. id : "+self.IDdispo+" : "+self.jourDispo
        res += " semaine "+self.semaineDispo+" de la période "+self.periodeDispo
        res += " disponible de "+str(self.heureDispoDebut) +" jusqu'à "+str(self.heureDispoFin)
        res += "derniere modification le :"+self.dateModifDispo+" à "+str(self.heureModifDispo)+"\n"
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
        id = maxIdActu()
        vac = Vacataire('V' + id,'Spontanée','0',request.form['nom'],request.form['prenom'],request.form['tel'],request.form['ddn'],request.form['email'],'177013')
        for i in range(1,4):
            les_cours = Cours.query.filter_by(nomCours=request.form['Matiere'+str(i)]).all()
            for cours in les_cours:
                db.session.execute(Affectable.insert().values(IDVacataire='V' + id,IDCours=cours.IDcours,TypeCours=cours.TypeCours))
                db.session.commit()
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
            try:
                log = Vacataire.query.filter_by(IDVacataire=request.form['idUser']).first()
                if request.form['password'] == log.mdpV:
                    login_user(log)
                    return EDT()
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
                        db.session.add(Affectable(ligne[0],ligne[1],ligne[2]))
                case 5:
                    for ligne in fileReader:
                        db.session.add(Assigner(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6]))
            db.session.commit()

test_connection()

if __name__=="__main__":
    app.run()