#!/usr/bin/python3

# pour avoir sqlalchemy :
# sudo apt-get update 
# sudo apt-get install python3-sqlalchemy
# pip3 install mysql-connector-python
import getpass  # pour faire la lecture cachée d'un mot de passe
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import func
import time
from datetime import date

import pymysql
pymysql.install_as_MySQLdb()

# Base class used by my classes (my entities)
Base = declarative_base()  # Required

class PersonnelAdministratif(Base):
    __tablename__ = 'PERSONNELADMINISTRATIF'

    IDpersAdmin = Column(Text,primary_key=True)
    nomPa = Column(Text)
    prenomPa = Column(Text)
    ddnPa = Column(Date)
    mailPa = Column(Text)
    mdpPa = Column(Text)

    dossierVacataire = relationship("Vacataire", back_populates = "selfdossier")
    gererdossier = relationship("GererDossier", back_populates = "gerantdossier")

    def __init__(self,idpa,nom,pnom,ddn,mail,mdp):
        self.IDpersAdmin = idpa
        self.nomPa = nom
        self.prenomPa = pnom
        self.ddnPa = ddn
        self.mailPa = mail
        self.mdpPa = mdp
    
    def __str__(self):
        return "PersonnelAdministratif :"+" "+self.IDpersAdmin+" "+self.nomPa+" "+self.prenomPa+" né(e) le ",self.ddnPa," mail : "+self.mailPa

class Vacataire(Base):
    __tablename__ = "VACATAIRE"

    IDVacataire = Column(Text,primary_key=True)
    candidature = Column(Text) #0 ou 1
    ancien = Column(Integer)
    nomV = Column(Text)
    prenomV = Column(Text)
    ddnV = Column(Date)
    mailV = Column(Text)
    mdpV = Column(Text)
    
    selfdossier = relationship("PersonnelAdministratif", back_populates = "dossierVacataire")
    dossier_qui_se_fait_gerer = relationship("GererDossier", back_populates = "dossierDuVacataire")
    vacataire_a_cours = relationship("Cours", back_populates ="cours_a_vacataire")
    vacataire_a_affectable = relationship("Affectable", back_populates = "affectable_a_vacataire")
    vacataire_a_assigner = relationship("Assigner", back_populates = "assigner_a_vacataire")

    def __init__(self,idv,candidature,est_ancien,nom,pnom,ddn,mail,mdp):
        self.IDVacataire = idv
        self.candidature = candidature
        self.ancien = est_ancien
        self.nomV = nom
        self.prenomV = pnom
        self.ddnV = ddn
        self.mailV = mail
        self.mdpV = mdp
    
    def __str__(self):
        return "Vacataire : "+" "+self.IDpersAdmin+" "+self.nomPa+" "+self.prenomPa+" né(e) le ",self.ddnPa," mail : "+self.mailPa+" type de candidature : "+self.candidature+" est ancien :"+self.ancien

class GererDossier(Base):
    __tablename__= "GERERDOSSIER"

    IDVacataire = Column(Text,primary_key=True)
    IDpersAdmin = Column(Text,primary_key=True)
    etat_dossier = Column(Text)
    dateModif = Column(Date)
    heureModif = Column(Integer)

    gerantdossier = relationship("PersonnelAdministratif",back_populates="gererdossier")
    dossierDuVacataire =relationship("Vacataire",back_populates="dossier_qui_se_fait_gerer")

    def __init__(self,idv,idp,edoc,date,h):
        self.IDVacataire = idv
        self.IDpersAdmin = idp
        self.etat_dossier = edoc
        self.dateModif = date
        self.heureModif = h
    
    def __str__(self):
        return "Dossier du vacataire "+self.IDVacataire+", modification le ",self.dateModif," à "+ str(self.heureModif)+"par "+self.IDpersAdmin+", le dossier est "+self.etat_dossier

class Cours(Base):
    __tablename__= "COURS"

    IDcours = Column(Text,primary_key=True)
    TypeCours = Column(Text,primary_key=True)
    nomCours = Column(Text)
    domaine = Column(Text)
    heuresTotale = Column(Integer)
    dureeCours = Column(Integer)

    cours_a_assigner = relationship("Assigner",back_populates="assigner_a_cours")
    cours_a_affectable = relationship("Affectable",back_populates="affectable_a_cours")
    cours_a_vacataire = relationship("Vacataire",back_populates="vacataire_a_cours")

    def __init__(self,idc,t,n,d,h,dur):
        self.IDcours = idc
        self.TypeCours = t
        self.nomCours = n
        self.domaine = d
        self.heuresTotale = h
        self.dureeCours = dur
    
    def __str__(self):
        return self.TypeCours+" "+self.IDcours+" : "+self.nomCours+" domaine de "+self.domaine+" "+self.heuresTotale+" d'heures totale pour une duree de "+self.dureeCours+" par cours"

class Affectable(Base):
    __tablename__= "AFFECTABLE"

    IDVacataire = Column(Text,primary_key=True)
    IDcours = Column(Text,ForeignKey("COURS.IDcours"),primary_key=True)
    TypeCours = Column(Text,ForeignKey("COURS.TypeCours"),primary_key=True)

    affectable_a_vacataire = relationship("Vacataire",back_populates="vacataire_a_affectable")
    affectable_a_cours = relationship("Cours",back_populates="cours_a_affectable")

    def __init__(self,idv,idc,tc):
        self.IDVacataire = idv
        self.IDcours = idc
        self.TypeCours = tc
    
    def __str__(self):
        return self.IDVacataire+" est affectable à "+self.IDcours+" "+self.TypeCours

class Assigner(Base):
    __tablename__ = "ASSIGNER"

    IDVacataire = Column(Text,primary_key=True)
    IDcours = Column(Text,ForeignKey("COURS.IDcours"),primary_key=True)
    TypeCours = Column(Text,ForeignKey("COURS.TypeCours"),primary_key=True)
    salle = Column(Text)
    classe = Column(Text)
    DateCours = Column(Date)
    HeureCours = Column(Integer)

    assigner_a_vacataire = relationship("Vacataire",back_populates="vacataire_a_assigner")
    assigner_a_cours = relationship("Cours",back_populates="cours_a_assigner")

    def __init__(self,idv,idc,t,s,c,d,h):
        self.IDVacataire = idv
        self.IDcours = idc
        self.TypeCours = t
        self.classe = c
        self.salle = s
        self.DateCours = d
        self.HeureCours = h
    
    def __str__(self):
        return "Le vacataire "+self.IDVacataire+" est assigné au cours "+self.TypeCours+" "+self.IDcours+" avec la classe "+self.classe+" dans la salle "+self.salle+" le ",self.DateCours+" à "+str(self.HeureCours)

#deprecated        
def ouvrir_connexion(user,passwd,host,database):
    """
    ouverture d'une connexion MySQL
    paramètres:
       user     (str) le login MySQL de l'utilsateur
       passwd   (str) le mot de passe MySQL de l'utilisateur
       host     (str) le nom ou l'adresse IP de la machine hébergeant le serveur MySQL
       database (str) le nom de la base de données à utiliser
    résultat: l'objet qui gère le connection MySQL si tout s'est bien passé
    """
    try:
        #creation de l'objet gérant les interactions avec le serveur de BD
        engine=create_engine('mysql+mysqlconnector://'+user+':'+passwd+'@'+host+'/'+database)
        #creation de la connexion
        cnx = engine.connect()
    except Exception as err:
        print(err)
        raise err
    print("connexion réussie")
    return cnx
    
if __name__ == "__main__":
    login=input("login MySQL ")
    passwd=getpass.getpass("mot de passe MySQL ")
    serveur=input("serveur MySQL ")
    bd=input("nom de la base de données ")
    cnx = ouvrir_connexion(login,passwd,serveur,bd)
    cnx.close()
