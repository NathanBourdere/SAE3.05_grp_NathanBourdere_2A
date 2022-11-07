from flask import Flask,render_template, request

app=Flask(__name__,template_folder='static/HTML')

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/nouveau_vacataire.html', methods= ['GET', 'POST'])
def new_vaca():
    return render_template('nouveau_vacataire.html')

@app.route('/EDT.html')
def EDT():
    return render_template('EDT.html')

@app.route('/menu_admin.html')
def menu_admin():
    return render_template('menu_admin.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')

@app.route('/recherche-dossiers.html')
def check_doss():
    return render_template('recherche-dossiers.html')           

@app.route('/login.html', methods= ['GET', 'POST'])
def log():
    # Nécéssite la base de données afin de vérifier les informations.
    if request.method == "POST":
        print('oe')
        try:
            print(request.form['username'])
            log = Vacataire.query.filter_by(IDVacataire=request.form['username']).first()
            if request.form['password'] == log.mdpV:
                return render_template('EDT.html')
        except:
            try:
                print('PA1')
                adm = PersonnelAdministratif.query.filter_by(IDpersAdmin=request.form['username']).first()
                print('PA2')
                if request.form['password'] == adm.mdpPa:
                    return render_template('menu_admin.html')
            except:
                return render_template('login.html')
    return render_template('login.html')

if __name__=="__main__":
    app.run(port=1598)