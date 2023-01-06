from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, IntegerField, DateField ,validators, HiddenField
from .models import Vacataire,PersonnelAdministratif,max_id_actuel
from hashlib import sha256

class InscriptionVacataire(FlaskForm):

    login = StringField('Login')
    nom = StringField('Nom')
    prenom = StringField('Prenom')
    email = StringField('E-mail', [validators.Length(min=6, max=35)])
    tel = StringField('Telephone', [validators.Length(min=6, max=35)])
    ddn = DateField('DateDeNaissance')
    password = PasswordField('Password')
    confirmation = PasswordField('Répétez le mot de passe')
    entreprise = StringField('Entreprise')
    legal = BooleanField('Mention Légale')

    def __init__(self) -> None:
        super().__init__()
        self.login.data = 'V'+max_id_actuel()

    def __init__(self,vacataire) -> None:
        super().__init__()
        self.remplir_champ(vacataire)


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