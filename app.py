from flask import Flask, flash, render_template, redirect, url_for, session, logging

from wtforms import Form, StringField, PasswordField, validators, TextAreaField
from passlib.hash import sha256_crypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


##---------------------------------------------------
##                    Connection
##---------------------------------------------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/mydatabase'
db = SQLAlchemy(app)

##---------------------------------------------------
##                      CLASS
##---------------------------------------------------


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column( '', db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

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

@app.route('/singin')
def cadastro():
    return render_template('singin.html')


## Necesário para reduzir os comandos para rodar o app usando (debug=true) e ficar no fim
if __name__ == '__main__':
    app.run(debug=True)