from flask import Flask, render_template, request, redirect, jsonify
from flask_restful import Resource, Api
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://my-user:my-password@db/my-database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone = db.Column(db.String(25))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    admin = db.Column(db.String(10))

