from flask import Flask, flash, render_template, redirect, url_for, session, logging, request

from wtforms import Form, StringField, PasswordField, validators, TextAreaField
from passlib.hash import sha256_crypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


##---------------------------------------------------
##                    Connection
##---------------------------------------------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cariman'
db = SQLAlchemy(app)

##---------------------------------------------------
##                      CLASS
##---------------------------------------------------


class User (db.Model):

    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=False, nullable= False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), unique=False, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class RegisterForm(Form):
    name = StringField('Seu nome', validators=[validators.Length(min=3, max=20), validators.optional()])
    username = StringField('Usename', validators=[validators.Length(min=5, max=50), validators.input_required()])
    email  = StringField('E-mail', validators=[validators.Length(min=9, max=100), validators.input_required()])
    password =PasswordField('Senha',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='As senhas não combinam')
    ])
    confirm = PasswordField('Confirme sua senha')

##---------------------------------------------------
##                      ROUTES
##---------------------------------------------------

##Esta rota vem do protocolo da barra de cima à busca
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User(
            name = form.name.data,
            email = form.email.data,
            username = form.username.data,
            password = sha256_crypt.encrypt(str(form.password.data))
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Você foi cadastrado', 'success')

        redirect(url_for('index'))
    return render_template('cadastro.html', form=form)

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 


## Necesário para reduzir os comandos para rodar o app usando (debug=true) e ficar no fim
if __name__ == '__main__':
    app.run(debug=True)