from yaml import *
from .app import db,login_manager
from flask_login import UserMixin
import hashlib
import binascii
import os
from sqlalchemy import * 

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

class Cours(db.Model):
    __tablename__= "Cours"

    id_cours = db.Column(db.String(100),primary_key=True)
    type_cours = db.Column(db.String(100),primary_key=True)
    nom_cours = db.Column(db.String(100),nullable=False)
    duree_cours = db.Column(db.Integer)
    domaine = db.Column(db.String(100),db.ForeignKey("Domaine.id_domaine"))

    domaine_a_cours = db.relationship("Domaine", backref=db.backref("cours", lazy="dynamic"))
    cours_assignee_id = db.relationship("Assigner",back_populates="assigner_cours_id", foreign_keys=[Assigner.id_cours])
    cours_assignee_type = db.relationship("Assigner",back_populates="assigner_cours_type", foreign_keys=[Assigner.type_cours])

    def __init__(self,idc,t,n,dur,dom):
        self.id_cours = idc
        self.type_cours = t
        self.nom_cours = n
        self.duree_cours = dur
        self.domaine = dom
    
    def __str__(self):
        return self.type_cours+" "+str(self.id_cours)+" : "+self.nom_cours+" "+" d'heures totales pour une duree de "+str(self.duree_cours)+" par cours "+" du domaine "

class Affectable(db.Model):
    __tablename__ = "Affectable"

    id_vacataire = db.Column(db.String(100),db.ForeignKey("Vacataire.id_vacataire"),primary_key=True)
    id_domaine = db.Column(db.String(100),db.ForeignKey("Domaine.id_domaine"),primary_key=True)
    date_modif_matiere = db.Column(db.String(100))
    heure_modif_matiere = db.Column(db.String(100))

    cours_affecter_vacataire = db.relationship("Vacataire",back_populates="vacat_affectable")
    affecter_domaine =  db.relationship("Domaine",back_populates="domaine_affecter", foreign_keys=[id_domaine])

    def __init__(self,idv,idc,dmd,hmm):
        self.id_vacataire = idv
        self.id_domaine = idc
        self.date_modif_matiere = dmd
        self.heure_modif_matiere = hmm
    
    def __str__(self):
        return "Le vacataire "+self.id_vacataire+" est assigné au domaine "+self.id_domaine+" dernière modif : "+self.date_modif_matiere+" "+self.heure_modif_matiere


class Domaine(db.Model):
    __tablename__ = "Domaine"

    id_domaine = db.Column(db.String(100),primary_key=True)
    domaine = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(3500),nullable=False)
    responsable = db.Column(db.String(100),db.ForeignKey("PersonnelAdministratif.id_pers_admin"),nullable=False)

    # le_cours = db.relationship("Cours", backref = "cours")
    pers_admin = db.relationship("PersonnelAdministratif",back_populates="responsable_dom")
    domaine_affecter = db.relationship("Affectable",back_populates="affecter_domaine",foreign_keys=[Affectable.id_domaine])

    def __init__(self,id,nomdom,description,resp):
        self.id_domaine = id
        self.domaine = nomdom
        self.description = description
        self.responsable = resp
    
    def __str__(self):
        return "Le domaine "+self.domaine+"id_v est sous la responsabilité de "+self.responsable

class PersonnelAdministratif(UserMixin,db.Model):
    __tablename__ = 'PersonnelAdministratif'

    id_pers_admin = db.Column(db.String(100),primary_key=True,nullable=False)
    cds_pa = db.Column(db.String(100), nullable=False) #cds = couche de sécurité, le sel
    nom_pa = db.Column(db.String(100))
    prenom_pa = db.Column(db.String(100))
    num_tel_pa = db.Column(db.String(100),unique=True)
    ddn_pa = db.Column(db.String(100))
    mail_pa = db.Column(db.String(100),unique=True)
    mdp_pa = db.Column(db.String(200))

    responsable_dom = db.relationship("Domaine", back_populates = "pers_admin",foreign_keys=[Domaine.responsable])
    gerant_dossier = db.relationship("GererDossier", back_populates = "personnel_admin")

    def __init__(self,idpa,nom,pnom,tel,ddn,mail,mdp,cds):
        self.id_pers_admin = idpa
        self.nom_pa = nom
        self.prenom_pa = pnom
        self.num_tel_pa = tel
        self.ddn_pa = ddn
        self.mail_pa = mail
        self.mdp_pa = mdp
        self.cds_pa = cds

    def get_id(self):
           return (self.id_pers_admin)

    def __str__(self):
        return "PersonnelAdministratif :"+" "+self.id_pers_admin+" "+self.nom_pa+" "+self.prenom_pa+" né(e) le ",self.ddn_pa," mail : "+self.mail_pa

class Vacataire(UserMixin,db.Model):
    __tablename__ = "Vacataire"

    id_vacataire = db.Column(db.String(100),primary_key=True)
    cds_v = db.Column(db.String(100), nullable=False) #cds = couche de sécurité, le sel
    candidature = db.Column(db.String(100),nullable=False) 
    ancien = db.Column(db.Integer) #0 ou 1
    entreprise = db.Column(db.String(100),nullable=True)
    nom_v = db.Column(db.String(100))
    prenom_v = db.Column(db.String(100))
    num_tel_v = db.Column(db.String(100),unique=True)
    ddn_v = db.Column(db.String(100),nullable=True)
    mail_v = db.Column(db.String(100),unique=True)
    mdp_v = db.Column(db.String(200),nullable=True)
    nationnalite = db.Column(db.String(100),nullable=True)
    profession = db.Column(db.String(100),nullable=True)
    meilleur_diplome = db.Column(db.String(100),nullable=True)
    annee_obtiention = db.Column(db.String(100),nullable=True)
    adresse = db.Column(db.String(100),nullable=True)
    legal = db.Column(db.Integer,nullable=True)

    vacat_affectable = db.relationship("Affectable",back_populates="cours_affecter_vacataire",foreign_keys=[Affectable.id_vacataire])
    selfdossier = db.relationship("GererDossier", back_populates = "dossier_vacataire")
    vacataire_assignee = db.relationship("Assigner", back_populates ="cours_a_vacataire")
    dispo = db.relationship("Disponibilites", backref = "vacataire")

    def __init__(self,idv,candidature,ent,est_ancien,nom,pnom,tel,ddn,mail,mdp,nationnalite,profession,meilleur_diplome,annee_obtention,adresse_postale,cds):
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
        self.adresse = adresse_postale
        self.legal = 0
        self.cds_v = cds
    
    def get_id(self):
        return (self.id_vacataire)
    
    def is_filled(self):
        return all([getattr(self, attr) != "" for attr in ['entreprise', 'nom_v', 'prenom_v', 'num_tel_v', 'mail_v', 
        'nationnalite', 'adresse','annee_obtiention', 'ddn_v', 'profession', 'meilleur_diplome']]) and self.legal == 1

    def __str__(self):
        return "Vacataire : "+" "+self.id_vacataire+" "+self.nom_v+" "+self.prenom_v+" né(e) le "+self.ddn_v+" mail : "+self.mail_v+" type de candidature : "+self.candidature+" est ancien :"+str(self.ancien)+" de l'entreprise "+self.entreprise

class Disponibilites(db.Model):
    __tablename__ = "Disponibilites"

    id_dispo = db.Column(db.String(100),primary_key=True)
    jour_dispo = db.Column(db.String(100))# lundi,mardi ... PAS DIMANCHE
    periode_dispo = db.Column(db.Integer) # 1 ou 2 ou 3 ou 4, il y a 2 périodes par semestre
    semestre_dispo = db.Column(db.Integer) # 1,2 jusqu'à 52
    heure_dispo_debut = db.Column(db.String(100)) # "14:30"
    heure_dispo_fin = db.Column(db.String(100)) # idem
    date_modif_dispo = db.Column(db.String(100))
    heure_modif_dispo = db.Column(db.String(100))
    id_vacataire = db.Column(db.String(100),db.ForeignKey("Vacataire.id_vacataire"),nullable=False)

    def __init__(self,idd,idv,j,pA,pS,hd,hf,dmd,hmd):
        self.id_dispo = idd
        self.jour_dispo = j
        self.semestre_dispo = pS
        self.periode_dispo = pA
        self.heure_dispo_debut = hd
        self.heure_dispo_fin = hf
        self.id_vacataire = idv
        self.date_modif_dispo = dmd
        self.heure_modif_dispo = hmd

    def __str__(self):
        res = "Vacataire "+self.id_vacataire+" dispo. id : "+self.id_dispo+" : "+self.jour_dispo
        res += " semaine "+str(self.semestre_dispo)+" de la période "+str(self.periode_dispo)
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

def max_id_cours():
    id_max = 0
    for id in db.session.query(Cours.id_cours).all():
        if id>id_max:
            id_max = id
    return id_max + 1

def est_vacataire(user):
    if type(user) == str:
        if user[0] == 'V':
            return True
    else:
        if user.get_id()[0] == 'V':
            return True
        
    return False

def get_vacataire(id_vaca:int)->Vacataire:
    """Retourne les informations d'un vacataire grâce à un identifiant donné.

    Args:
        id_vaca (int): L'identifiant du vacataire recherché.

    Returns:
        Vacataire: Le vacataire recherché.
    """    
    vacataires = Vacataire.query.all()
    for vacataire in vacataires:
        if vacataire.id_vacataire == id_vaca:
            return vacataire
    return None

def actualiser_date_dossier(dossier:GererDossier):
    """Actualise l'heure et la date de dernière modification du dossier du vacataire donné avec la date et l'heure actuelle.

    Args:
        dossier (GererDossier): Le dossier à mettre à jour.
    """    
    from datetime import date, datetime

    date_actuelle = date.today()
    heure_actuelle = datetime.now().strftime("%H:%M")
    dossier.date_modif = date_actuelle
    dossier.heure_modif = heure_actuelle

    db.session.commit()

def get_dossier(id_vaca:int)->GererDossier:
    """Récupère les informations relatives à u

    Args:
        id_vaca (int): _description_

    Returns:
        GererDossier: _description_
    """   
    dossiers = GererDossier.query.all()
    for dossier in dossiers:
        if dossier.id_vacataire == id_vaca:
            return dossier
    return None

def searchDomaine(id_v,tri="Ne pas trier",search=""):
    filtre = Domaine.id_domaine
    match(tri):
        case "Identifiant":
            filtre = Domaine.id_domaine
        case "Domaine":
            filtre = Domaine.domaine
        case "Responsable":
            filtre = PersonnelAdministratif.nom_pa  + " " + PersonnelAdministratif.prenom_pa
        case "Ne pas trier":
            return db.session.query(Domaine.id_domaine,Domaine.domaine,Domaine.responsable, PersonnelAdministratif.nom_pa, PersonnelAdministratif.prenom_pa).join(PersonnelAdministratif, PersonnelAdministratif.id_pers_admin == Domaine.responsable).join(Affectable,Affectable.id_domaine == Domaine.id_domaine and Affectable.id_vacataire == id_v).all()
    return db.session.query(Domaine.id_domaine,Domaine.domaine,Domaine.responsable, PersonnelAdministratif.nom_pa, PersonnelAdministratif.prenom_pa).join(PersonnelAdministratif, PersonnelAdministratif.id_pers_admin == Domaine.responsable).join(Affectable,Affectable.id_domaine == Domaine.id_domaine and Affectable.id_vacataire == id_v).filter(filtre.ilike("%"+search+"%")).order_by(filtre).all()

def searchDossier(tri="Trier les dossiers ↓",filtre="Filtrer les dossiers ↓",search=""):
    if filtre == "Filtrer les dossiers ↓":
        match(tri):
            case "Nom":
                orderR = Vacataire.nom_v
            case "Prenom":
                orderR = Vacataire.prenom_v
            case "Telephone":
                orderR = Vacataire.num_tel_v
            case "Status":
                orderR = GererDossier.etat_dossier
            case "Trier les dossiers ↓":
                return db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).all() 
        return db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(orderR.ilike("%"+search+"%")).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).order_by(orderR).all()    
    else:
        match(tri):
            case "Nom":
                return db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(Vacataire.nom_v.ilike("%"+search+"%"),GererDossier.etat_dossier.ilike(filtre)).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).order_by(Vacataire.nom_v).all()
            case "Prenom":
                  return db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(Vacataire.prenom_v.ilike("%"+search+"%"),GererDossier.etat_dossier.ilike(filtre)).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).order_by(Vacataire.prenom_v).all()
            case "Telephone":
                return db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(Vacataire.num_tel_v.ilike("%"+search+"%"),GererDossier.etat_dossier.ilike(filtre)).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).order_by(Vacataire.num_tel_v).all()
            case "Status":
                return db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(GererDossier.etat_dossier.ilike("%"+search+"%"),GererDossier.etat_dossier.ilike(filtre)).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).order_by(GererDossier.etat_dossier).all()
            case "Trier les dossiers ↓":
                return db.session.query(Vacataire.nom_v,Vacataire.prenom_v,Vacataire.num_tel_v,Vacataire.mail_v,GererDossier.etat_dossier).filter(GererDossier.etat_dossier.ilike(filtre)).join(GererDossier,GererDossier.id_vacataire==Vacataire.id_vacataire).all()

def searchCours(tri, filtre, search=""):
    if filtre == 'Nom':
        return db.session.query(Vacataire.nom_v, Vacataire.prenom_v, Cours.nom_cours, Cours.type_cours, Cours.duree_cours, Assigner.date_cours, Assigner.heure_cours, Assigner.classe, Assigner.salle).filter(Vacataire.nom_v.ilike("%"+search+"%"),Cours.nom_cours == tri).join(Assigner, Assigner.id_vacataire == Vacataire.id_vacataire).join(Cours, Cours.id_cours == Assigner.id_cours).order_by(Cours.nom_cours).all()
    else:
          return db.session.query(Vacataire.nom_v, Vacataire.prenom_v, Cours.nom_cours, Cours.type_cours, Cours.duree_cours, Assigner.date_cours, Assigner.heure_cours, Assigner.classe, Assigner.salle).filter(Vacataire.prenom_v.ilike("%"+search+"%"),Cours.nom_cours == tri).join(Assigner, Assigner.id_vacataire == Vacataire.id_vacataire).join(Cours, Cours.id_cours == Assigner.id_cours).order_by(Cours.nom_cours).all()

def editeur_auto_doc(dossier,vacataire):
    if vacataire.is_filled():
        if dossier.etat_dossier == "Incomplet" or dossier.etat_dossier == "Distribué":
            dossier.etat_dossier = "Complet"
    else:
        if dossier.etat_dossier != "Validé":
            dossier.etat_dossier = "Incomplet"
    db.session.commit()

def update_dossier_vac(vac, **kwargs):
    for key, value in kwargs.items():
        if hasattr(vac, key) and value is not None:
            setattr(vac, key, value)
    db.session.commit()

def saler_mot_de_passe(mot_de_passe, sel=None):
    """
    Cette fonction prend en entrée un mot de passe et un sel (facultatif), 
    et renvoie le mot de passe salé en utilisant la fonction de hachage SHA-256.
    Si aucun sel n'est fourni, un sel aléatoire est généré.
    """
    if sel is None:
        sel =os.urandom(16)# Génère 16 bytes aléatoires

    # Réencode les bytes en hexadécimal
    hex_str = sel.hex()

    # Réencode les bytes en UTF-8
    sel_utf = hex_str.encode('utf-8')

    mot_de_passe_encode = mot_de_passe.encode('utf-8') # Convertir le mot de passe en bytes
    # Concaténer le sel et le mot de passe
    mot_de_passe_sel = mot_de_passe_encode + sel_utf

    # Calculer le haché du mot de passe salé
    hache = hashlib.sha256(mot_de_passe_sel).hexdigest()

    # Retourner le sel et le haché du mot de passe salé
    return (sel_utf.decode("utf-8"), hache)

def verifier_mot_de_passe(mot_de_passe, sel, hache_stocke):
    """
    Cette fonction prend en entrée un mot de passe, un sel et le haché stocké dans la base de données,
    et renvoie True si le mot de passe fourni correspond à celui stocké, False sinon.
    """
    
    mot_de_passe_encode = mot_de_passe.encode('utf-8') # Convertir le mot de passe en bytes
    sel = sel.encode('utf-8')
    # Concaténer le sel et le mot de passe
    mot_de_passe_sel = mot_de_passe_encode + sel

    # Calculer le haché du mot de passe salé
    hache = hashlib.sha256(mot_de_passe_sel).hexdigest()

    # Vérifier si le haché calculé correspond à celui stocké dans la base de données
    return hache == hache_stocke

def get_domaines():
    return Domaine.query.all()

def get_domaine(id):
    return Domaine.query.get(id)

def get_dispos(id_vacataire):
    return db.session.query(Disponibilites).filter(Disponibilites.id_vacataire==id_vacataire).all()

def get_affectables(vaca):
    return Affectable.query.get(Affectable.id_vacataire==vaca.id_vacataire).all()

def get_dates_from_json_file(filename):
    import json
    from datetime import datetime
    """
    Cette fonction prend un nom de fichier JSON en entrée et renvoie un dictionnaire
    contenant toutes les données du fichier.
    """
    with open(filename, 'r') as f:
        json_dict = json.load(f) # charge le fichier JSON dans un dictionnaire Python

    data_dict = {} # initialiser un dictionnaire vide pour stocker les données

    # boucler sur les clés du dictionnaire externe
    for key1 in json_dict.keys():
        data_dict[key1] = {} # initialiser un dictionnaire interne pour chaque clé externe
        # boucler sur les clés du dictionnaire interne
        for key2 in json_dict[key1].keys():
            data_dict[key1][key2] = [] # initialiser une liste pour chaque clé interne
            # boucler sur chaque élément de la liste
            for value in json_dict[key1][key2]:
                # vérifier si la valeur est une date valide
                try:
                    date_obj = datetime.strptime(value, '%Y-%m-%d').date()
                    # vérifier si le jour correspondant est dimanche
                    if date_obj.weekday() != 6: # 6 correspond à dimanche
                        data_dict[key1][key2].append(value) # ajouter la valeur à la liste
                except ValueError:
                    pass # ignorer les valeurs qui ne sont pas des dates valides
    
    return data_dict


def duree_entre_deux_temps(temps1, temps2):
    from datetime import time, datetime, timedelta
    if len(temps1) <=3:
        date_temps1 = datetime.strptime(temps1,'%Hh')
    else:
        date_temps1 = datetime.strptime(temps1, '%Hh%M')
    
    if len(temps2) <=3:
        date_temps2 = datetime.strptime(temps2,'%Hh')
    else:
        date_temps2 = datetime.strptime(temps2, '%Hh%M')
    
    secondes_temps1 = time(date_temps1.hour, date_temps1.minute).second
    secondes_temps2 = time(date_temps2.hour, date_temps2.minute).second
    
    duree_secondes = abs(secondes_temps2 - secondes_temps1)
    duree = timedelta(seconds=duree_secondes)
    
    heures, reste = divmod(duree.seconds, 3600)
    minutes, secondes = divmod(reste, 60)
    
    format_duree = f"{heures:02d}h{minutes:02d}"
    
    return format_duree

def get_jour(val,voulu):
    from datetime import datetime
    match(voulu):
        case "Lundi":
            voulu = 0
        case "Mardi":
            voulu = 1
        case "Mercredi":
            voulu = 2
        case "Jeudi":
            voulu = 3
        case "Vendredi":
            voulu = 4
        case "Samedi":
            voulu = 5
        case "Dimanche":
            voulu = 6
    return datetime.datetime.strptime(val, '%Y-%m-%d').weekday() == voulu