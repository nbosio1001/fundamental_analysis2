from flask import Flask
from Flask-SQLAlchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'postgresql:///nbosio1001:test123@localhost/
    postgres@nbosio1001-ThinkPad-T480:/home/nbosio1001/Documents/python/fundamental_analysis
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Company_Name(db.Model):
    
    __tablename__ = 'Company Financials'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), unique=True)
    ticker_symbol = db.Column(db.String(64), unique=True)
    CIK_number = db.Column(db,Integer, unique=True)

    
    def __repr__(self):
        return '<Ticker Symbol: %r>' % self.ticker_symbol

@app.route('/')
def index():
    return "<h1 style"









from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

db = SQLAlchemy(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Company_Name(db.Model):
    __tablename__ = 'Company Financials'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), unique=True)
    ticker_symbol = db.Column(db.String(64), unique=True)
    CIK_number = db.Column(db,Integer, unique=True)

    
    def __repr__(self):
        return '<Ticker Symbol: %r>' % self.ticker_symbol

