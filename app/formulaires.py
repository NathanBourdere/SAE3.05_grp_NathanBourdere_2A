from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, IntegerField, DateField ,validators

class InscriptionVacataire(FlaskForm):
    nom = StringField('Nom')
    prenom = StringField('Prenom')
    email = StringField('E-mail', [validators.Length(min=6, max=35)])
    tel = StringField('Telephone', [validators.Length(min=6, max=35)])
    ddn = DateField('DateDeNaissance')
    password = PasswordField('Password', [
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