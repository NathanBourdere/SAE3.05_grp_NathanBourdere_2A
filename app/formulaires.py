from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, IntegerField, DateField ,validators, HiddenField
from .models import Vacataire,PersonnelAdministratif, get_vacataire,max_id_actuel,verifier_mot_de_passe
from hashlib import sha256

class InscriptionVacataire(FlaskForm):

    login = StringField('Login', validators=[validators.Regexp('^[a-zA-Z0-9_-]{3,16}$')], render_kw={"pattern": "^[a-zA-Z0-9_-]{3,16}$"})
    nom = StringField('Nom', validators=[validators.DataRequired(), validators.Length(min=1, max=35), validators.Regexp('^[a-zA-ZÀ-ÿ]{2,35}$')], render_kw={"pattern": "^[a-zA-ZÀ-ÿ]{2,35}$"})
    prenom = StringField('Prenom', validators=[validators.DataRequired(), validators.Length(min=1, max=35), validators.Regexp('^[a-zA-ZÀ-ÿ]{2,35}$')], render_kw={"pattern": "^[a-zA-ZÀ-ÿ]{2,35}$"})
    email = StringField('E-mail', validators=[validators.DataRequired(), validators.Length(min=6, max=35), validators.Regexp('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')], render_kw={"pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"})
    tel = StringField('Téléphone', validators=[validators.DataRequired(), validators.Regexp('^(?:\+33|0)[1-9](?:[\.\-\s]?[0-9]{2}){4}$')], render_kw={"pattern": "^(?:\+33|0)[1-9](?:[\.\-\s]?[0-9]{2}){4}$"})
    ddn = DateField('Date De Naissance', [validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=1, max=35), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Répétez le mot de passe', validators=[validators.DataRequired()])
    entreprise = StringField('Entreprise', validators=[validators.DataRequired(), validators.Length(min=1, max=35)])
    legal = BooleanField('')
    nationalite = StringField("Nationalité")
    profession = StringField("Profession")
    meilleur_diplome = StringField("Diplôme")
    annee_obtiention = StringField("Année d'obtention de votre diplôme")
    adresse = StringField("Adresse", validators=[validators.Regexp('^[a-zA-Z0-9\s,\'-]{3,}$')])


    def __init__(self,vacataire=None) -> None:
        super().__init__()
        if vacataire is None:
            self.login.data = 'V'+max_id_actuel()
        else:
            self.remplir_champs(vacataire)
    
    def remplir_champs(self, vacataire) -> None:
        """Permet de préremplir les champs du formulaire.

        Args:
            vacataire (Vacataire): Le vacataire dans lequel récupérer les informations.
        """        
        from datetime import datetime

        ddn_vacataire = datetime.strptime(vacataire.ddn_v, "%Y-%m-%d")
        self.nom.data = vacataire.nom_v
        self.prenom.data = vacataire.prenom_v
        self.email.data = vacataire.mail_v
        self.tel.data = vacataire.num_tel_v
        self.ddn.data = ddn_vacataire
        self.entreprise.data = vacataire.entreprise
        self.nationalite.data = vacataire.nationnalite
        self.profession.data = vacataire.profession
        self.meilleur_diplome.data = vacataire.meilleur_diplome
        self.annee_obtiention.data = vacataire.annee_obtiention
        self.adresse.data = vacataire.adresse
        if vacataire.legal == 0:
            self.legal.data = False
        else :
            self.legal.data = True

class NewAccount(FlaskForm):
    login = StringField('Identifiant', [validators.Length(min=1)])
    password = PasswordField('Mot de passe')
    next = HiddenField()

class NouveauMDP(FlaskForm):
    mdp_actuel = PasswordField("Mot de passe actuel")
    nouveau_mdp = PasswordField("Nouveau mot de passe")
    confirmation = PasswordField("Répéter le nouveau mot de passe")

def is_mdp(formulaire,user_type,user):
    m = sha256()
    m.update(formulaire.password.data.encode())
    passwd = m.hexdigest()
    if user_type == "A":
        return user if verifier_mot_de_passe(formulaire.password.data,user.cds_pa,user.mdp_pa) else None
    return user if verifier_mot_de_passe(formulaire.password.data,user.cds_v,user.mdp_v) else None
    
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