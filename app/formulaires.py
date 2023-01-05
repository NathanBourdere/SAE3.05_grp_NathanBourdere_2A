from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, IntegerField, DateField ,validators

class InscriptionVacataire(FlaskForm):
    nom_v = StringField('Nom')
    prenom_v = StringField('Prenom')
    mail_v = StringField('E-mail', [validators.Length(min=6, max=35)])
    num_tel_v = StringField('Telephone', [validators.Length(min=6, max=35)])
    ddn_v= DateField('DateDeNaissance')
    mdp_v = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirmation', message='Les mots de passe ne sont pas les mêmes')
    ])
    confirmation = PasswordField('Répétez le mot de passe')
    entreprise = StringField('Entreprise')

class NewAccount(FlaskForm):
    login = StringField('Name', [validators.Length(min=1)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Les mots de passe ne sont pas les mêmes')
    ])