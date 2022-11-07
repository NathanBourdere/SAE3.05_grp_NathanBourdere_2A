from flask import Flask,render_template

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

@app.route('/login.html')
def log():
    return render_template('/login.html')

if __name__=="__main__":
    app.run(port=1598)