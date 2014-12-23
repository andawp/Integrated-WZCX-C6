# coding=utf-8
__author__ = 'Administrator'
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.normpath(os.path.join(os.getcwd(), 'wzcx2.db'))
db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    cpd = db.Column(db.String(10))
    hm = db.Column(db.String(20), unique=True)
    fdj = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, cpd, hm, fdj, email):
        self.cpd = cpd
        self.hm = hm
        self.fdj = fdj
        self.email = email

    def __repr__(self):
        return 'Car: %r %r' % (unicode(self.cpd), self.hm)

db.drop_all()
db.create_all()
wangp = Car(u'湘', 'A12W02', '29864','wangp@bofo.com.cn')
db.session.add(wangp)
db.session.commit()