import click
from .app import app,db
import os
from .models import *
from .views import max_id_actu
import csv

@app.cli.command()
@click.argument('family_name')
@click.argument('name')
@click.argument('tel')
@click.argument('ddn')
@click.argument('mail')
@click.argument('mdp')
def new_pers_admin(family_name,name,tel,ddn,mail,mdp):
    """Créer un nouveau compte de personnel administratif"""
    vrai_sel,hache = saler_mot_de_passe(mdp)
    admin = PersonnelAdministratif('A'+max_id_actu(),family_name,name,tel,ddn,mail,hache,vrai_sel)
    db.session.add(admin)
    db.session.commit()
    
@app.cli.command()
def init_db():
    """Initialiser la base de données avec des tables vides."""

    if os.path.exists("../db.sqlite3"):
        os.remove("../db.sqlite3")
    db.create_all()

@app.cli.command()
def drop_db():
    """Supprimer la base de données."""

    if os.path.exists("../db.sqlite3"):
        os.remove("../db.sqlite3")
    else:
        print("Le ficher de la base de données n'a pas été trouvé.")

@app.cli.command()
def feed_db():
    """Initialiser et nourrir la base de données."""

    if not os.path.exists("../db.sqlite3"):
        db.create_all()

    listeCsv = ['admin.csv','vacataire.csv','dossier.csv','cours.csv','affectable.csv','assigner.csv','matieres.csv']
    for i in range(len(listeCsv)):
        with open("static/data/"+listeCsv[i]) as data:
            file_reader = csv.reader(data)
            match(i):
                case 0:
                    for ligne in file_reader:
                        db.session.add(PersonnelAdministratif(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6],ligne[7]))
                case 1:
                    for ligne in file_reader:
                        db.session.add(Vacataire(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6],ligne[7],ligne[8],ligne[9],ligne[10],ligne[11],ligne[12],ligne[13],ligne[14],ligne[15]))
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
                case 6:
                    for ligne in file_reader:
                        db.session.add(Domaine(ligne[0],ligne[1],ligne[2],ligne[3]))
            db.session.commit()