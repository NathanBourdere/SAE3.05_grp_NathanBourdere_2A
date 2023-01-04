from yaml import *
import os.path
from .app import db,login_manager
from flask_login import UserMixin

# Initialisation des tables ORM

class GererDossier(db.Model):
    __tablename__= "GererDossier"

    IDVacataire = db.Column(db.String(100),db.ForeignKey("Vacataire.IDVacataire"),primary_key=True,nullable=False)
    IDpersAdmin = db.Column(db.String(100),db.ForeignKey("PersonnelAdministratif.IDpersAdmin"),primary_key=True,nullable=False)
    etat_dossier = db.Column(db.String(100))
    dateModif = db.Column(db.String(100))
    heureModif = db.Column(db.String(100))

    personnelAdmin = db.relationship('PersonnelAdministratif',back_populates="gerant_dossier")
    dossierVacataire = db.relationship("Vacataire", back_populates = "selfdossier")

    def __init__(self,idv,idp,edoc,date,h):
        self.IDVacataire = idv
        self.IDpersAdmin = idp
        self.etat_dossier = edoc
        self.dateModif = date
        self.heureModif = h
    
    def __str__(self):
        return "Dossier du vacataire "+self.IDVacataire+", modification le ",self.dateModif," à "+ self.heureModif+"par "+self.IDpersAdmin+", le dossier est "+self.etat_dossier

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
    DateModifMatiere = db.Column(db.String(100))
    HeureModifMatiere = db.Column(db.String(100))

    cours_affecter_vacataire = db.relationship("Vacataire",back_populates="vacat_affectable")
    affecter_cours_id = db.relationship("Cours",back_populates="cours_affecter_id", foreign_keys=[IDcours])
    affecter_cours_type = db.relationship("Cours",back_populates="cours_affecter_type", foreign_keys=[TypeCours])

    def __init__(self,idv,idc,t,dmd,hmm):
        self.IDVacataire = idv
        self.IDcours = idc
        self.TypeCours = t
        self.DateModifMatiere = dmd
        self.HeureModifMatiere = hmm
    
    def __str__(self):
        return "Le vacataire "+self.IDVacataire+" est assigné au cours "+self.TypeCours+" "+self.IDcours+" dernière modif : "+self.DateModifMatiere+" "+self.HeureModifMatiere

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

    IDDISPO = db.Column(db.Integer, primary_key=True)
    IDVacataire = db.Column(db.String(100),db.ForeignKey("Vacataire.IDVacataire"),nullable=False)
    jourDispo = db.Column(db.String(100))# lundi,mardi ... PAS DIMANCHE
    periodeAnneeDispo = db.Column(db.Integer)
    periodeSemestreDispo = db.Column(db.Integer) # 1 ou 2 ou 3 ou 4, il y a 2 périodes par semestre
    heureDispoDebut = db.Column(db.String(100)) # "14:30"
    heureDispoFin = db.Column(db.String(100)) # idem
    dateModifDispo = db.Column(db.String(100))
    heureModifDispo = db.Column(db.String(100))
    

    def __init__(self,idd,idv,j,pA,pS,hd,hf,dmd,hmd):
        self.IDdispo = idd
        self.jourDispo = j
        self.periodeAnneeDispo = pA
        self.periodeSemestreDispo = pS
        self.heureDispoDebut = hd
        self.heureDispoFin = hf
        self.IDVacataire = idv
        self.dateModifDispo = dmd
        self.heureModifDispo = hmd

    def __str__(self):
        res = "Vacataire "+self.IDVacataire+" dispo. id : "+self.IDdispo+" : "+self.jourDispo
        res += " semaine "+self.semaineDispo+" de la période "+self.periodeDispo
        res += " disponible de "+self.heureDispoDebut +" jusqu'à "+self.heureDispoFin
        res += "derniere modification le :"+self.dateModifDispo+" à "+self.heureModifDispo+"\n"
        return res

db.create_all()
db.session.commit()