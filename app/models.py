from yaml import *
from .app import db, login_manager
from flask_login import UserMixin

# Initialisation des tables ORM

class GererDossier(db.Model):
    __tablename__= "GererDossier"

    id_vacataire = db.Column(db.String(100),db.ForeignKey("Vacataire.id_vacataire"),primary_key=True,nullable=False)
    id_pers_admin = db.Column(db.String(100),db.ForeignKey("PersonnelAdministratif.id_pers_admin"),primary_key=True,nullable=False)
    etat_dossier = db.Column(db.String(100))
    date_modif = db.Column(db.String(100))
    heure_modif = db.Column(db.String(100))

    personnel_admin = db.relationship('PersonnelAdministratif',back_populates="gerant_dossier")
    dossier_vacataire = db.relationship("Vacataire", back_populates = "selfdossier")

    def __init__(self,idv,idp,edoc,date,h):
        self.id_vacataire = idv
        self.id_pers_admin = idp
        self.etat_dossier = edoc
        self.date_modif = date
        self.heure_modif = h
    
    def __str__(self):
        return "Dossier du vacataire "+self.id_vacataire+", modification le ",self.date_modif," à "+ self.heure_modif+"par "+self.id_pers_admin+", le dossier est "+self.etat_dossier

class Assigner(db.Model):
    __tablename__ = "Assigner"

    id_vacataire = db.Column(db.String(100),db.ForeignKey("Vacataire.id_vacataire"),primary_key=True,nullable=False)
    id_cours = db.Column(db.String(100),db.ForeignKey("Cours.id_cours"),primary_key=True,nullable=False)
    type_cours = db.Column(db.String(100),db.ForeignKey("Cours.type_cours"),primary_key=True,nullable=False)
    salle = db.Column(db.String(100))
    classe = db.Column(db.String(100))
    date_cours = db.Column(db.String(100))
    heure_cours = db.Column(db.Integer)

    cours_a_vacataire = db.relationship("Vacataire",back_populates="vacataire_assignee")
    assigner_cours_id = db.relationship("Cours",back_populates="cours_assignee_id", foreign_keys=[id_cours])
    assigner_cours_type = db.relationship("Cours",back_populates="cours_assignee_type", foreign_keys=[type_cours])

    def __init__(self,idv,idc,t,s,c,d,h):
        self.id_vacataire = idv
        self.id_cours = idc
        self.type_cours = t
        self.classe = c
        self.salle = s
        self.date_cours = d
        self.heure_cours = h
    
    def __str__(self):
        return "Le vacataire "+self.id_vacataire+" est assigné au cours "+self.type_cours+" "+self.id_cours+" avec la classe "+self.classe+" dans la salle "+self.salle+" le ",str(self.date_cours)+" à "+str(self.heure_cours)

class PersonnelAdministratif(UserMixin,db.Model):
    __tablename__ = 'PersonnelAdministratif'

    id_pers_admin = db.Column(db.String(100),primary_key=True,nullable=False)
    nom_pa = db.Column(db.String(100))
    prenom_pa = db.Column(db.String(100))
    num_tel_pa = db.Column(db.String(100),unique=True)
    ddn_pa = db.Column(db.String(100))
    mail_pa = db.Column(db.String(100),unique=True)
    mdp_pa = db.Column(db.String(100))

    gerant_dossier = db.relationship("GererDossier", back_populates = "personnelAdmin")

    def __init__(self,idpa,nom,pnom,tel,ddn,mail,mdp):
        self.id_pers_admin = idpa
        self.nom_pa = nom
        self.prenom_pa = pnom
        self.num_tel_pa = tel
        self.ddn_pa = ddn
        self.mail_pa = mail
        self.mdp_pa = mdp

    def get_id(self):
           return (self.id_pers_admin)

    def __str__(self):
        return "PersonnelAdministratif :"+" "+self.id_pers_admin+" "+self.nom_pa+" "+self.prenom_pa+" né(e) le ",self.ddn_pa," mail : "+self.mail_pa


class Affectable(db.Model):
    tablename__ = "Affectable"

    id_acataire = db.Column(db.String(100),db.ForeignKey("Vacataire.id_vacataire"),primary_key=True)
    id_cours = db.Column(db.String(100),db.ForeignKey("Cours.id_cours"),primary_key=True)
    type_cours = db.Column(db.String(100),db.ForeignKey("Cours.type_cours"),primary_key=True)
    date_modif_matiere = db.Column(db.String(100))
    heure_modif_matiere = db.Column(db.String(100))

    cours_affecter_vacataire = db.relationship("Vacataire",back_populates="vacat_affectable")
    affecter_cours_id = db.relationship("Cours",back_populates="cours_affecter_id", foreign_keys=[id_cours])
    affecter_cours_type = db.relationship("Cours",back_populates="cours_affecter_type", foreign_keys=[type_cours])

    def __init__(self,idv,idc,t,dmd,hmm):
        self.id_vacataire = idv
        self.id_cours = idc
        self.type_cours = t
        self.date_modif_matiere = dmd
        self.heure_modif_matiere = hmm
    
    def __str__(self):
        return "Le vacataire "+self.id_vacataire+" est assigné au cours "+self.type_cours+" "+self.id_cours+" dernière modif : "+self.date_modif_matiere+" "+self.heure_modif_matiere

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

    id_vacataire = db.Column(db.String(100),primary_key=True)
    candidature = db.Column(db.String(100),nullable=False) 
    ancien = db.Column(db.Integer) #0 ou 1
    entreprise = db.Column(db.String(100))
    nom_v = db.Column(db.String(100))
    prenom_v = db.Column(db.String(100))
    num_tel_v = db.Column(db.String(100),unique=True)
    ddn_v = db.Column(db.String(100))
    mail_v = db.Column(db.String(100),unique=True)
    mdp_v = db.Column(db.String(100))
    nationnalite = db.Column(db.String(100))
    profession = db.Column(db.String(100))
    meilleur_diplome = db.Column(db.String(100))
    annee_obtiention = db.Column(db.String(100))
    adresse_postale = db.Column(db.String(100))

    vacat_affectable = db.relationship("Affectable",back_populates="cours_affecter_vacataire",foreign_keys=[Affectable.id_vacataire])
    selfdossier = db.relationship("GererDossier", back_populates = "dossier_vacataire")
    vacataire_assignee = db.relationship("Assigner", back_populates ="cours_a_vacataire")
    dispo = db.relationship("Disponibilites", backref = "vacataire")

    def __init__(self,idv,candidature,ent,est_ancien,nom,pnom,tel,ddn,mail,mdp,nationnalite,profession,meilleur_diplome,annee_obtention,adresse_postale):
        self.id_vacataire = idv
        self.candidature = candidature
        self.entreprise = ent
        self.ancien = est_ancien
        self.nom_v = nom
        self.prenom_v = pnom
        self.num_tel_v = tel
        self.ddn_v = ddn
        self.mail_v = mail
        self.mdp_v = mdp
        self.nationnalite = nationnalite
        self.profession = profession
        self.meilleur_diplome = meilleur_diplome
        self.annee_obtiention = annee_obtention
        self.adresse_postale = adresse_postale
    
    def get_id(self):
        return (self.id_vacataire)

    def __str__(self):
        return "Vacataire : "+" "+self.id_vacataire+" "+self.nom_v+" "+self.prenom_v+" né(e) le "+self.ddn_v+" mail : "+self.mail_v+" type de candidature : "+self.candidature+" est ancien :"+str(self.ancien)+" de l'entreprise "+self.entreprise

class Cours(db.Model):
    __tablename__= "Cours"

    id_cours = db.Column(db.String(100),primary_key=True)
    type_cours = db.Column(db.String(100),primary_key=True)
    nom_cours = db.Column(db.String(100),nullable=False)
    heures_totales = db.Column(db.Integer)
    duree_cours = db.Column(db.Integer)
    domaine = db.Column(db.String(100),db.ForeignKey("Domaine.domaine"),nullable=False)

    cours_assignee_id = db.relationship("Assigner",back_populates="assigner_cours_id", foreign_keys=[Assigner.id_cours])
    cours_assignee_type = db.relationship("Assigner",back_populates="assigner_cours_type", foreign_keys=[Assigner.type_cours])
    cours_affecter_id = db.relationship("Affectable",back_populates="affecter_cours_id",foreign_keys=[Affectable.id_cours])
    cours_affecter_type = db.relationship("Affectable",back_populates="affecter_cours_type",foreign_keys=[Affectable.type_cours])

    def __init__(self,idc,t,n,h,dur,dom):
        self.id_cours = idc
        self.type_cours = t
        self.nom_cours = n
        self.heures_totales = h
        self.duree_cours = dur
        self.domaine = dom
    
    def __str__(self):
        return self.type_cours+" "+str(self.id_cours)+" : "+self.nom_cours+" "+str(self.heures_totales)+" d'heures totales pour une duree de "+str(self.duree_cours)+" par cours "+" du domaine "+self.domaine

class Disponibilites(db.Model):
    __tablename__ = "Disponibilites"

    id_dispo = db.Column(db.String(100),primary_key=True)
    jour_dispo = db.Column(db.String(100))# lundi,mardi ... PAS DIMANCHE
    semaine_dispo = db.Column(db.Integer) # 1,2 jusqu'à 52
    periode_dispo = db.Column(db.Integer) # 1 ou 2 ou 3 ou 4, il y a 2 périodes par semestre
    heure_dispo_debut = db.Column(db.String(100)) # "14:30"
    heure_dispo_fin = db.Column(db.String(100)) # idem
    date_modif_dispo = db.Column(db.String(100))
    heure_modif_dispo = db.Column(db.String(100))
    id_vacataire = db.Column(db.String(100),db.ForeignKey("Vacataire.id_vacataire"),nullable=False,unique=True)

    def __init__(self,idd,j,s,p,hd,hf,idv,dmd,hmd):
        self.id_dispo = idd
        self.jour_dispo = j
        self.semaine_dispo = s
        self.periode_dispo = p
        self.heure_dispo_debut = hd
        self.heure_dispo_fin = hf
        self.id_vacataire = idv
        self.date_modif_dispo = dmd
        self.heure_modif_dispo = hmd

    def __str__(self):
        res = "Vacataire "+self.id_vacataire+" dispo. id : "+self.id_dispo+" : "+self.jour_dispo
        res += " semaine "+self.semaine_dispo+" de la période "+self.periode_dispo
        res += " disponible de "+self.heure_dispo_debut +" jusqu'à "+self.heure_dispo_fin
        res += "derniere modification le :"+self.date_modif_dispo+" à "+self.heure_modif_dispo+"\n"
        return res

db.create_all()
db.session.commit()

def max_id_actuel():
    id_max = 0
    vacataires = db.session.query(Vacataire.id_vacataire).all()
    for id in vacataires:
        if id_max<int(id[0][1:]):
            id_max = int(id[0][1:])
    personnels_admin = db.session.query(PersonnelAdministratif.id_pers_admin).all()
    for id in personnels_admin:
        if id_max<int(id[0][1:]):
            id_max = int(id[0][1:])
    return str(id_max+1)

def est_vacataire(user):
    if type(user) == str:
        if user[0] == 'V':
            return True
    else:
        if user.get_id()[0] == 'V':
            return True
        
    return False