from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, IntegerField, DateField ,validators, HiddenField
from .models import Vacataire,PersonnelAdministratif, get_vacataire,max_id_actuel
from hashlib import sha256

class InscriptionVacataire(FlaskForm):

    login = StringField('Login')
    nom = StringField('Nom', [validators.DataRequired(), validators.Length(min=1, max=35)])
    prenom = StringField('Prenom', [validators.DataRequired(), validators.Length(min=1, max=35)])
    email = StringField('E-mail', [validators.DataRequired(), validators.Length(min=6, max=35)])
    tel = StringField('Téléphone', [validators.DataRequired(), validators.Length(min=6, max=35)])
    ddn = DateField('Date De Naissance',[validators.DataRequired()])
    password = PasswordField('Password',[validators.DataRequired(), validators.Length(min=1, max=35),validators.EqualTo('confirm', message='Passwords must match')])
    confirmation = PasswordField('Répétez le mot de passe', [validators.DataRequired()])
    entreprise = StringField('Entreprise', [validators.DataRequired(), validators.Length(min=1, max=35)])
    legal = BooleanField('Mention Légale')
    nationalite = StringField("Nationalité")
    profession = StringField("Profession")
    meilleur_diplome = StringField("Diplôme")
    annee_obtiention = StringField("Année d'obtiention de votre diplôme")
    adresse = StringField("Adresse")

    def init(self,vacataire=None) -> None:
        super().init()
        if vacataire is None:
            self.login.data = 'V'+max_id_actuel()
        else:
            self.remplir_champs(vacataire)


class NewAccount(FlaskForm):
    login = StringField('Identifiant', [validators.Length(min=1)])
    password = PasswordField('Mot de passe')
    next = HiddenField()

def is_mdp(formulaire,user_type,user):
    m = sha256()
    m.update(formulaire.password.data.encode())
    passwd = m.hexdigest()
    if user_type == "A":
        return user if passwd == user.mdp_pa else None
    return user if passwd == user.mdp_v else None
    
def get_authenticated_user(formulaire):
    if formulaire.login.data[0] == "V":
        user = Vacataire.query.get(formulaire.login.data)
        if user is None:
            return None
        return is_mdp(formulaire,formulaire.login.data[0],user)
    elif formulaire.login.data[0] == "A":
        user = PersonnelAdministratif.query.get(formulaire.login.data)
        if user is None:
            return None
        return is_mdp(formulaire,formulaire.login.data[0],user)